from abc import ABC, abstractmethod
import pandas as pd


class Task(ABC):

    def __init__(self, task_name: str, path_to_data: str):
        self.task_name = task_name
        self._df = pd.read_csv(path_to_data)
        if 'Unnamed: 0' in self._df.columns:
            self._df.drop(columns=['Unnamed: 0'], inplace=True)
        self._df.reset_index(drop=True, inplace=True)

    @abstractmethod
    def get_next_test_case(self, zero_shot=True):
        pass

    @abstractmethod
    def get_all_test_cases(self, zero_shot=True):
        pass

    @property
    def df(self) -> pd.DataFrame:
        return self._df


