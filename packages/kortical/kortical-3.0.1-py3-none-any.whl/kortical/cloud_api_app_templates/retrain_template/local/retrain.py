from module_placeholder.workflows.train import train_workflow


class CeleryTaskMock:
    @staticmethod
    def update_state(state):
        print(state)


if __name__ == '__main__':
    train_workflow.execute(data={}, progress_report_function=lambda x: print(x))
