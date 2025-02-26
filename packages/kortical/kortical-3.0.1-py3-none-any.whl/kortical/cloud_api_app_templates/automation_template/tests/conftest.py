import pytest
from kortical.app import get_app_config
from module_placeholder.main import create_app

app_config = get_app_config(format='yaml')
target = app_config['target']
target_accuracy = app_config['target_accuracy']


@pytest.fixture(scope='session')
def app():
    app = create_app()
    return app


@pytest.fixture
def calibration_results():
    return {
        target: {
            'automation_overall': {
                'automation': 0.9,
                'accuracy': target_accuracy,
                'for_review': 0.1
            },
            'automation_per_class': {
                'class1': {
                    'automation': 0.9,
                    'accuracy': target_accuracy,
                    'for_review': 0.1
                },
                'class2': {
                    'automation': 0.9,
                    'accuracy': target_accuracy,
                    'for_review': 0.1
                }
            },
            'f1_for_automated_rows': {
                'weighted_average': {
                    'precision': 0.9,
                    'recall': 0.8,
                    'f1_score': 0.8,
                    'count': 1000
                },
                'classes': {
                    'class1': {
                        'precision': 0.9,
                        'recall': 0.8,
                        'f1_score': 0.8,
                        'count': 1000
                    },
                    'class2': {
                        'precision': 0.9,
                        'recall': 0.8,
                        'f1_score': 0.8,
                        'count': 1000
                    }
                }
            },
            'f1_for_all_rows': {
                'weighted_average': {
                    'precision': 0.9,
                    'recall': 0.8,
                    'f1_score': 0.8,
                    'count': 1000
                },
                'classes': {
                    'class1': {
                        'precision': 0.9,
                        'recall': 0.8,
                        'f1_score': 0.8,
                        'count': 1000
                    },
                    'class2': {
                        'precision': 0.9,
                        'recall': 0.8,
                        'f1_score': 0.8,
                        'count': 1000
                    },
                    'not_automated': {
                        'precision': 0.9,
                        'recall': 0.8,
                        'f1_score': 0.8,
                        'count': 1000
                    }
                }
            }
        }
    }
