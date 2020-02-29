from src.module import Module, Kernel
from src.models import *
from typing import Dict
from src.signals import *


class MessageHandler(Module):
    def __init__(self, kernel: Kernel):
        super().__init__(kernel)
        self.users_with_operator: Dict[User, User] = {}

    def handle_message(self, user: User, message: str, attachments_files: list):
        if user in self.users_with_operator:
            self.kernel.messenger.send_message_with_photos(self.users_with_operator[user], message, attachments_files)
        else:
            self.kernel.messages_parser.handle_message(str)

    def handle_signal_message(self, user: User, signal: Signal):
        class_type = signal.__class__
        if class_type == GetPhysTechSchoolsInfo:
            pass
        elif class_type == RatingInCompetition:
            pass
