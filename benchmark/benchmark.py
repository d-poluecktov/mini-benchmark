from functools import wraps

import pandas as pd


class Benchmark:

    def __init__(self, tasks, path_to_save, zero_shot=True):
        self.__tasks = tasks
        self.__path_to_save = path_to_save
        self.__zero_shot = zero_shot

    def __test_task(self, func, task, zero_shot=True) -> list[str]:
        # TODO: writing logic for few shot testing
        test_cases = task.get_all_test_cases(zero_shot=zero_shot)

        model_results = list()
        for test_case in test_cases:
            model_results.append(func(test_case))

        return model_results

    def __call__(self, func):

        for task in self.__tasks:
            task_result = self.__test_task(func, task)
            messages = task.df.loc[:, "message"].tolist()

            res_df = pd.DataFrame({"message": messages, "result": task_result})
            res_df.to_csv(self.__path_to_save + task.task_name + ".csv", index=False)


