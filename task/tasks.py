import typing
from task.Task import Task


class InstructTask(Task):
    __standard_role_format = "<|{role}|>"
    __standard_end_format = "<|end|>"
    __standard_message = "{message}"

    __system_message = "You are helpfully assistant."

    def __init__(self,
                 task_name: str,
                 path_to_data: str,
                 user_promt: str,
                 system_promt: typing.Optional[str] = None,
                 system_role='system',
                 user_role='user',
                 assistant_role='assistant',
                 role_format: typing.Optional[str] = None,
                 end_format: typing.Optional[str] = None):

        super().__init__(task_name, path_to_data)

        if role_format is not None:
            self.__standard_role_format = role_format

        if end_format is not None:
            self.__standard_end_format = end_format

        self.__system_role = system_role
        self.__user_role = user_role
        self.__assistant_role = assistant_role

        self.__user_promt = user_promt

        self.__standard_promt_format = (self.__standard_role_format + "\n"
                                        + self.__standard_message
                                        + self.__standard_end_format)

        if system_promt is not None:
            self.__system_promt = system_promt
        self.__user_promt = user_promt

    def __generate_system_promt(self):
        system_promt_format = self.__standard_promt_format
        system_promt = system_promt_format.format(role=self.__system_role, message=self.__system_message)
        return system_promt

    def __generate_user_promt(self, message: str) -> str:
        user_promt = self.__user_promt
        user_promt = user_promt.format(message=message)
        user_promt_format = self.__standard_promt_format
        return user_promt_format.format(role=self.__user_role, message=user_promt)

    def __generate_test_case(self, message: str, zero_shot=True) -> str:
        # TODO: write logic for few-shot testing
        assistant_end = self.__standard_role_format
        assistant_end = assistant_end.format(role=self.__assistant_role)

        system_promt = self.__generate_system_promt()
        user_promt = self.__generate_user_promt(message)
        return (system_promt + '\n' +
                user_promt + '\n' +
                assistant_end + '\n')

    def get_next_test_case(self, zero_shot=True) -> str:
        for i in range(len(self._df)):
            yield self.__generate_test_case(self._df.loc[i, 'message'], zero_shot=True)

    def get_all_test_cases(self, zero_shot=True) -> list[str]:
        test_cases = list(map(self.__generate_test_case, self._df.loc[:, 'message']))
        return test_cases



class LMTask(Task):

    def __init__(self, task_name, path_to_data: str, user_promt):
        super(LMTask, self).__init__(task_name, path_to_data)
        self.__user_promt = user_promt

    def __generate_test_case(self, message, zero_shot=True):
        # TODO: writing logic for few shot testing
        user_promt = self.__user_promt
        return user_promt.format(message=message)

    def get_next_test_case(self, zero_shot=True):
        for i in range(len(self._df)):
            yield self.__generate_test_case(self._df.loc[i, 'message'], zero_shot=True)

    def get_all_test_cases(self, zero_shot=True):
        test_cases = list(map(self.__generate_test_case, self._df.loc[:, 'message']))
        return test_cases




