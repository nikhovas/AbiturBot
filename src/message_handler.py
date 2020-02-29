from src.module import Module, Kernel
from src.models import *
from typing import Dict, List
from src.signals import *
from src.app_config import RawFiles


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
            data: str = open(RawFiles.PHYS_TECH_SCHOOLS_INFO_FILE, "r").read()
            self.kernel.messenger.send_message_with_photos(user, str, [])
        elif class_type == RatingInCompetition:
            place: int = self.kernel.database.get_place_in_competition(user, signal.direction)
            answer: str = "Вы находитесь на {} месте".format(place)
            self.kernel.messenger.send_message_with_photos(user, answer, [])
        elif class_type == GetCompetitionInfo:
            students_list: List[CompetitionInfo] = self.kernel.database.get_full_competition_list(signal.direction)
            answer = ""
            for i in students_list:
                answer += "{} {} {} {}\n".format(i.user.surname, i.user.name, i.user.father_name, i.score)
            self.kernel.messenger.send_message_with_photos(user, answer, [])


