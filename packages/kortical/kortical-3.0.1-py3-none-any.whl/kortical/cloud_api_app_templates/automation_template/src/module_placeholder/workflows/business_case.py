from kortical.app import get_app_config

app_config = get_app_config(format='yaml')
target = app_config['target']
target_accuracy = app_config['target_accuracy']
target_accuracy_tolerance = 0.03        # 3%


# A simple example where the business metric is the automation rate.
def calculate(calibration_results, print_results=False):
    automation_rate = calibration_results[target]['automation_overall']['automation']
    if print_results:
        print(f"Automation Rate {automation_rate * 100:.2f}%")
    return automation_rate


def should_publish(challenger_calibration_results, champion_calibration_results):
    target = list(challenger_calibration_results.keys())[0]

    challenger_accuracy = challenger_calibration_results[target]['automation_overall']['accuracy']
    target_accuracy_delta = abs(challenger_accuracy - target_accuracy)

    # Check if the challenger accuracy is close enough to the target accuracy
    if challenger_accuracy < target_accuracy and target_accuracy_delta > target_accuracy_tolerance:
        return False, f"The accuracy for the challenger model accuracy [{challenger_accuracy:.3f}] was not within " \
                      f"the tolerance [{target_accuracy_tolerance}] of the target accuracy [{target_accuracy}]."

    challenger_automation_rate = calculate(challenger_calibration_results)

    # If there is no champion and the target accuracy is met publish the challenger
    if champion_calibration_results is None:
        return True, f"There is no current champion. Publishing the model is recommended. " \
                     f"The challenger accuracy [{challenger_accuracy:.3f}], the difference to the target " \
                     f"is [{target_accuracy_delta:.3f}]. The automation rate is [{challenger_automation_rate:.2f}]."

    champion_automation_rate = calculate(champion_calibration_results)
    automation_rate_change = challenger_automation_rate - champion_automation_rate

    # determine if the automation rate is a meaningful amount better if not return False
    if challenger_automation_rate < champion_automation_rate:
        return False, f"The challenger model does not meaningfully improve the automation rate [{automation_rate_change:.3f}]."

    return True, f"The challenger automation rate is [{challenger_automation_rate:.2f}], " \
                 f"the target accuracy difference [{target_accuracy_delta:.3f}] is acceptable and " \
                 f"the automation rate is improved by [{automation_rate_change:.2f}]."
