# from src.module import Module, Kernel
# from src.models import *
# from typing import Dict
# from src.signals import *
#
#
# class MessagesParser(Module):
#     def __init__(self, kernel: Kernel):
#         super().__init__(kernel)
#
#     def handle_message(self, message: str) -> Signal:
#         pass


from src.models import *
from typing import Dict
from src.signals import *


# there will lutiy Dima's code


class MessagesParser:
    class QuestionAnswerStructure:
        def __init__(self, question: str, answer: str):
            self.question = question
            self.answer = answer
            self.processed_question = None
            self.processed_answer = None

    # maybe it is better to place it here
    users_questions_and_answers: list = []

    def __init__(self, kernel):
        self.kernel = kernel

    def handle_message(self, message: str):
        pass
