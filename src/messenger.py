from src.models import *
from src.module import Module


class Messenger(Module):
    # allows exceptions
    # !!! use temp files (system directory /tmp) for temporary photos storing
    async def send_message_with_photos(self, user: User, message: str, attachments_files: list):
        pass
