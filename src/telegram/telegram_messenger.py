from asyncio.queues import Queue

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils import executor

from src.messenger import Messenger
from . import keyboards
from . import utils
from .utils import QuestionInfo

bot = Bot(token='909308261:AAHJmfqOW2D5-epx5XePYHRuVuEgVML4Odw')
dispatcher = Dispatcher(bot, storage=MemoryStorage())
_kernel = None
queue = Queue(loop=dispatcher.loop)
queue.put_nowait(QuestionInfo("question 1", 167813686))
queue.put_nowait(QuestionInfo("question 2", 167813686))
queue.put_nowait(QuestionInfo("question 3", 167813686))
queue.put_nowait(QuestionInfo("question 4", 167813686))
queue.put_nowait(QuestionInfo("question 5", 167813686))
queue.put_nowait(QuestionInfo("question 6", 167813686))
queue.put_nowait(QuestionInfo("question 7", 167813686))
queue.put_nowait(QuestionInfo("question 8", 167813686))
queue.put_nowait(QuestionInfo("question 9", 167813686))


class TelegramMessenger(Messenger):
    def __init__(self, kernel):
        self.kernel = kernel
        super().__init__()

        global _kernel
        _kernel = kernel

    def start_pooling(self):
        executor.start_polling(dispatcher)

    @dispatcher.message_handler(commands=['start'])
    async def process_start_command(msg: types.Message):
        await bot.send_message(msg.from_user.id, "Добро пожаловать! Отправьте свой номер телефона.",
                               reply_markup=keyboards.markup_request)

    @dispatcher.message_handler(content_types=['contact'])
    async def process_get_contact(msg: types.Message):
        await bot.send_message(msg.from_user.id, "Ваш номер телефона {}.".format(msg.contact['phone_number']),
                               reply_markup=ReplyKeyboardRemove())

        user_id = await _kernel.database.get_user_by_phone(msg.contact['phone_number'])
        await _kernel.database.set_chat_id_for_user(user_id, msg.from_user.id)

        await bot.send_message(msg.from_user.id, "Выберите действие", reply_markup=keyboards.markup_main)
        await utils.MainUser.main.set()

    @dispatcher.message_handler(lambda msg: msg.text and msg.text == 'Задать вопрос о поступлении',
                                state=utils.MainUser.main)
    async def ask_question(msg: types.Message, state: FSMContext):
        await bot.send_message(msg.from_user.id, "Введите ваш вопрос", reply_markup=ReplyKeyboardRemove)

    # TODO работа с вопросами от Димаса

    @dispatcher.message_handler(lambda msg: msg.text and msg.text == 'Информация о конкурсе',
                                state=utils.MainUser.main)
    async def comp_info_but_send(msg: types.Message, state: FSMContext):
        pass

    # Админка
    # Рассылка
    @dispatcher.message_handler(commands=['mailing'])
    async def process_admin_mailing(msg: types.Message):
        user_id = await _kernel.database.get_user_by_chat_id(msg.from_user.id)
        if await _kernel.database.is_user_admin(user_id):
            await bot.send_message(msg.from_user.id, "Введите текст рассылки.")
            await utils.AdmMailing.mailing_text.set()

    @dispatcher.message_handler(content_types=['text'], state=utils.AdmMailing.mailing_text)
    async def get_mailing_text(msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['text'] = msg.text

        await bot.send_message(msg.from_user.id, msg.text,
                               reply_markup=keyboards.mailing_settings)

        await utils.AdmMailing.check_text.set()

    @dispatcher.callback_query_handler(lambda call: call.data == 'CHANGE_TEXT', state=utils.AdmMailing.check_text)
    async def change_mailing_text(call: types.CallbackQuery, state: FSMContext):
        await bot.edit_message_text("Введите новый текст", call.from_user.id,
                                    call.message.message_id)

    @dispatcher.message_handler(content_types=['text'], state=utils.AdmMailing.check_text)
    async def get_new_text(msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['text'] = msg.text

        await bot.send_message(msg.from_user.id, msg.text,
                               reply_markup=keyboards.mailing_settings)

    @dispatcher.callback_query_handler(lambda call: call.data == 'MAIL', state=utils.AdmMailing.check_text)
    async def send_mailing_text(call: types.CallbackQuery, state: FSMContext):
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.send_message(call.from_user.id, "Сообщение разослано.")
        async with state.proxy() as data:
            for i in await _kernel.database.get_all_chat_ids():
                await bot.send_message(i, data['text'])

        await state.finish()

    # ответы на вопросы
    @dispatcher.message_handler(commands=['answer'])
    async def process_answer_admin_question(msg: types.Message):
        user_id = await _kernel.database.get_user_by_chat_id(msg.from_user.id)
        if await _kernel.database.is_user_admin(user_id):
            if queue.empty():
                await bot.send_message(msg.from_user.id, "Вопросов от абитуриентов нет.")
            else:
                question = await queue.get()
                await bot.send_message(msg.from_user.id, question.text,
                                       reply_markup=keyboards.get_questions_keyboard(question.chat_id))
                await utils.AdmAskQuestions.asking.set()

    @dispatcher.callback_query_handler(lambda call: call.data.startswith('NEXT_QUESTION'),
                                       state=utils.AdmAskQuestions.asking)
    async def send_next_question(call: types.CallbackQuery, state: FSMContext):
        question_chat_id = call.data.split()[1]
        await queue.put(QuestionInfo(call.message.text, question_chat_id))
        question = await queue.get()
        await bot.edit_message_text(question.text, call.from_user.id, call.message.message_id,
                                    reply_markup=keyboards.get_questions_keyboard(question.chat_id))
