
from dataclasses import dataclass

from kortical.api.model import Model
from kortical.api.project import Project
from kortical.api.worker_group import WorkerGroup
from kortical.cli._cmd_registry import command
from kortical.cli.helpers.kortical_config_helpers import get_full_kortical_config

from kortical.helpers.print_helpers import print_info, print_success, print_title, display_list


@dataclass
class ModelUsage:
    id: int
    name: str
    status: str


@dataclass
class ProjectUsage:
    id: int
    name: str
    usage: str
    num_apps_models_live: int


@dataclass
class WorkerUsage:
    id: int
    name: str
    type: str
    num_workers: int


@dataclass
class SystemUsage:
    name: str
    value: str


@command('usage')
def command_app(args):
    """
Lists usage information.

Definitions:

Project             A framework for the deployment and management of apps + models on Kortical. Projects are
                    comprised of multiple environments, and environments may contain several components.
Environment         A collection of deployed apps + models on Kortical. Environments are chained together within a project,
                    where the contents of one environment are promoted to the next. The default list of environments
                    is Integration --> UAT --> Production.
Challenger          A new environment; this is usually cloned from one of the main environments e.g to implement bug
                    fixes for apps, or monitor the performance of an improved model.
App                 A term used to refer to a codebase/application hosted on Kortical. The codebase may be created from
                    one of the templates provided, and the app is added to Kortical for the first time when you deploy
                    to any environment within a project.
Model               An algorithm that has been trained on a dataset to predict one or more target columns. In Kortical,
                    this term also refers to a workspace in which a collection of candidate models are trained, of which
                    the best one will be deployed to a project + environment.
Worker Group        A set of computers of a given specification (e.g number of cores, RAM, GPU). You can configure various tasks, projects
                    and environments to run on a specific worker group. For example, you might want to dedicate one worker group for
                    training models and another for a Production environment, so performance by one is not affected by the other.

usage:
    kortical usage list

commands:
    list                    Returns a list projects and the usage in those projects. As well as the worker groups.
    """

    if args['list']:
        print_title("Usage by Model:")
        models = Model.list()
        model_data = []
        for model in models:
            if model.status != 'Deactivated':
                model_data.append(ModelUsage(model.id, model.name, model.status))
        display_list(model_data)

        print_title("Usage by Project:")
        print_info("""NB: That for the purposes of usage it's the number of replicas of apps and models that are counted. Not the number of apps and models.
As each replica is a live instance of an app or model serving requests.""")
        projects = Project.list()
        project_data = []
        for project in projects:
            usage = []
            num_apps_models_project = 0
            environments = project.list_environments()
            challenger_environments = []
            for environment in environments:
                challenger_environments += environment.list_challengers()

            for environment in environments + challenger_environments:
                components = environment.list_component_instances()
                num_apps_models_environment = 0
                for component in components:
                    kortical_config = get_full_kortical_config(component)
                    num_replicas = kortical_config['replicas']
                    num_apps_models_environment += num_replicas
                    num_apps_models_project += num_replicas
                usage.append(f"Environment [{environment.name}]\n[{len(components)}] apps / models\n[{num_apps_models_environment}] live app / model replicas.")
            usage_string = "\n\n".join(usage)
            project_data.append(ProjectUsage(project.id, project.name, usage_string, num_apps_models_project))
        display_list(project_data)

        print_title("Usage by WorkerGroup:")
        worker_groups = WorkerGroup.list()
        worker_group_data = []
        worker_group_type_map = {
            '4-CPU-26GB-RAM': 'Standard',
            '8-CPU-52GB-RAM': 'Large',
            '8-CPU-64GB-RAM-AMD': 'Large',
        }
        for worker_group in worker_groups:
            worker_group_data.append(WorkerUsage(worker_group.id, worker_group.name, worker_group_type_map.get(worker_group.worker_type, 'Custom'), worker_group.required_size))
        display_list(worker_group_data)

        print_title('\nUsage Summary:')
        usage_summary_start = f"\nThere are [{len(model_data)}] active models with prediction / explanation endpoints."
        total_replicas = sum([project.num_apps_models_live for project in project_data])
        usage_summary_start += f"\n\nThere are [{len(projects)}] projects with a total of [{total_replicas}] apps / model instances serving requests across all environments."
        usage_summary_end = f"\nThis makes a total of [{total_replicas + len(model_data)}] live predicting app / models."
        for worker_type in set(worker_group_type_map.values()):
            num_system_workers = sum([x.num_workers for x in worker_group_data if x.name == 'system' and x.type == worker_type])
            num_workers = sum([x.num_workers for x in worker_group_data if x.type == worker_type])
            if num_system_workers == 0:
                usage_summary_end += f"\n\nThere are [{num_workers}] {worker_type} workers."
            else:
                usage_summary_end += f"\n\nThere are [{num_workers}] {worker_type} workers. [{num_system_workers}] of which are system workers."

        print_info(usage_summary_start)
        print_success(usage_summary_end)

        info = """
To delete a project, run `kortical project delete <project-name-or-id>`.

To delete an environment, run `kortical environment delete <environment-name-or-id>`.

To delete a component (app/model), run `kortical component delete <component-name-or-id>`.

To change the number of replicas for a component, run `kortical component set-replicas <component-name-or-id> <num-replicas>`.

To change the number of replicas for an environment, run `kortical kortical-config set replicas <num-replicas>`.

To resize a worker group, run `kortical worker resize <worker-group-name-or-id> <size>`.
"""
        print_title('\nTips:')
        print_info(info)



