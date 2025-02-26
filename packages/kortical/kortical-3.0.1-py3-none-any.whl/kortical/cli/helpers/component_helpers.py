from kortical.api.component_instance import ComponentInstance
from kortical.api.enums import ComponentInstanceState
from kortical.helpers.print_helpers import print_info, print_title, display_list


def display_list_component_instances_urls(component_instances, project, environment):
    if len(component_instances) > 0:
        print_title(f"Component URLs for environment [{environment.name}] in project [{project.name}]:")
        for component_instance in component_instances:
            if component_instance.status in [ComponentInstanceState.CREATING, ComponentInstanceState.RUNNING, ComponentInstanceState.PENDING]:
                print_info(f"{component_instance.type.value}|{component_instance.name}: {component_instance.get_url()}\n")


def display_list_component_instances(project, environment, include_deleted=False):
    component_instances = ComponentInstance.list(project, environment, include_created_by=True, include_deleted=include_deleted)
    print_title(f"Components for environment [{environment.name}] in project [{project.name}]:")
    display_list(component_instances)
    return component_instances
