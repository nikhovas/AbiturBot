from src.module import Module
from src.models import *


class MessageHandler(Module):
    def handle_raw_message(self, user: User, message: str):
        pass

    def handle_message_with_photos(self, user: User, message: str, attachments_files: list):
        pass

    # what will be in the arguments???
    # def handle_signal_message(self):
    #     pass
