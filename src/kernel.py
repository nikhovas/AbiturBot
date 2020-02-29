from src.database import Database
from src.messenger import Messenger
from src.message_handler import MessageHandler
from src.operator_controller import OperatorController
from src.messages_parser import MessagesParser

from src import app_config


class Kernel:
    def __init__(self):
        self.database: Database = app_config.USING_MODULES['database'](self)
        self.messenger: Messenger = app_config.USING_MODULES['messenger'](self)

        self.message_handler: MessageHandler = MessageHandler(self)
        self.operator_controller: OperatorController = OperatorController(self)
        self.messages_parser: MessagesParser = MessagesParser(self)
