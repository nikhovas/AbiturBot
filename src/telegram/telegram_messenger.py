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

questions_cache = dict()


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
        await bot.send_message(msg.from_user.id, "Выберите действие", reply_markup=keyboards.markup_main)
        await utils.MainUser.main.set()

        user_id = await _kernel.database.get_user_by_phone(msg.contact['phone_number'])
        await _kernel.database.set_chat_id_for_user(user_id, msg.from_user.id)

    @dispatcher.message_handler(lambda msg: msg.text and msg.text == 'Задать вопрос о поступлении',
                                state=utils.MainUser.main)
    async def ask_question(msg: types.Message, state: FSMContext):
        await bot.send_message(msg.from_user.id, "Введите ваш вопрос", reply_markup=ReplyKeyboardRemove)

    # TODO работа с вопросами от Димаса

    @dispatcher.message_handler(lambda msg: msg.text and msg.text == 'Информация о конкурсе',
                                state=utils.MainUser.main)
    async def comp_info_but_send(msg: types.Message, state: FSMContext):

        user_id = await _kernel.database.get_user_by_chat_id(msg.from_user.id)
        competitions = await _kernel.database.get_all_user_competitions(user_id)

        text = ""
        for i in competitions:
            text += i.get_description()

        text += 'Выберите направление для просмотра рейтинга:'
        sent_msg = await bot.send_message(msg.from_user.id, text,
                                          reply_markup=keyboards.get_competition_keyboard(competitions),
                                          parse_mode='markdown')
        await utils.MainUser.show_comp_info.set()

    @dispatcher.callback_query_handler(lambda call: len(call.data.split()) == 3, state=utils.MainUser.show_comp_info)
    async def do(call: types.CallbackQuery, state: FSMContext):
        data = map(int, call.data.split())
        relative_list = await _kernel.database.get_relative_list(*data)
        await bot.edit_message_text(relative_list.de_json(), call.from_user.id, call.message.message_id,
                                    reply_markup=keyboards.back, parse_mode='markdown')

    @dispatcher.callback_query_handler(lambda call: call.data == 'BACK', state=utils.MainUser.show_comp_info)
    async def do(call: types.CallbackQuery, state: FSMContext):
        user_id = await _kernel.database.get_user_by_chat_id(call.from_user.id)
        competitions = await _kernel.database.get_all_user_competitions(user_id)

        text = ""
        for i in competitions:
            text += i.get_description()

        text += 'Выберите направление для просмотра рейтинга:'
        sent_msg = await bot.edit_message_text(text, call.from_user.id, call.message.message_id,
                                               reply_markup=keyboards.get_competition_keyboard(competitions),
                                               parse_mode='markdown')

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
        if await _kernel.database.is_user_admin_by_chat_id(msg.from_user.id):
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

    @dispatcher.callback_query_handler(lambda call: call.data == 'DELETE_QUESTION',
                                       state=utils.AdmAskQuestions.asking)
    async def del_question_admin(call: types.CallbackQuery, state: FSMContext):
        question = await queue.get()
        await bot.edit_message_text(question.text, call.from_user.id, call.message.message_id,
                                    reply_markup=keyboards.get_questions_keyboard(question.chat_id))

    @dispatcher.callback_query_handler(lambda call: call.data.startswith('ASK_QUESTION'),
                                       state=utils.AdmAskQuestions.asking)
    async def del_question_admin(call: types.CallbackQuery, state: FSMContext):
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.send_message(call.from_user.id, "Введите ответ на вопрос")

        async with state.proxy() as data:
            data['chat_id'] = call.data.split()[1]
            data['question'] = call.message.text
        await utils.AdmAskQuestions.get_answer.set()

    @dispatcher.message_handler(content_types=['text'], state=utils.AdmAskQuestions.get_answer)
    async def get_message(msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['text'] = msg.text

        await bot.send_message(msg.from_user.id, msg.text,
                               reply_markup=keyboards.asking_settings)

        await utils.AdmAskQuestions.check_text.set()

    @dispatcher.callback_query_handler(lambda call: call.data == 'CHANGE_TEXT', state=utils.AdmAskQuestions.check_text)
    async def change_asking_text(call: types.CallbackQuery, state: FSMContext):
        await bot.edit_message_text("Введите новый текст", call.from_user.id,
                                    call.message.message_id)

    @dispatcher.message_handler(content_types=['text'], state=utils.AdmAskQuestions.check_text)
    async def get_new_text_for_ask(msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['text'] = msg.text

        await bot.send_message(msg.from_user.id, msg.text,
                               reply_markup=keyboards.asking_settings)

    @dispatcher.callback_query_handler(lambda call: call.data == 'MAIL', state=utils.AdmAskQuestions.check_text)
    async def send_asking_text(call: types.CallbackQuery, state: FSMContext):
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.send_message(call.from_user.id, "Ответ отправлен. Сохранить ответ на вопрос?",
                               reply_markup=keyboards.add_to_cash)
        await utils.AdmAskQuestions.send.set()
        async with state.proxy() as data:
            await bot.send_message(data['chat_id'],
                                   'Ответ на вопрос: \"{}\" \n\n {}'.format(data['question'], data['text']))

    @dispatcher.callback_query_handler(lambda call: call.data == 'ADD_TO_CASH', state=utils.AdmAskQuestions.send)
    async def send_ask_to_cash(call: types.CallbackQuery, state: FSMContext):
        await bot.edit_message_text("Ответ добавлен в кэш. Продолжить отвечать на вопросы?", call.from_user.id,
                                    call.message.message_id, reply_markup=keyboards.continue_answer)
        async with state.proxy() as data:
            questions_cache[data['question']] = data['text']
        await utils.AdmAskQuestions.continue_answer.set()

    @dispatcher.callback_query_handler(lambda call: call.data == 'DONT_ADD_TO_CASH', state=utils.AdmAskQuestions.send)
    async def dont_send_ask_to_cash(call: types.CallbackQuery, state: FSMContext):
        await bot.edit_message_text("Ответ не добавлен в кэш. Продолжить отвечать на вопросы?", call.from_user.id,
                                    call.message.message_id, reply_markup=keyboards.continue_answer)

        await utils.AdmAskQuestions.continue_answer.set()

    @dispatcher.callback_query_handler(lambda call: call.data == 'CONTINUE_ANSWER',
                                       state=utils.AdmAskQuestions.continue_answer)
    async def continue_answering(call: types.CallbackQuery, state: FSMContext):
        if queue.empty():
            await bot.edit_message_text("Вопросов от абитуриентов нет.", call.from_user.id, call.message.message_id)
            await state.finish()
        else:
            question = await queue.get()
            await bot.edit_message_text(question.text, call.from_user.id, call.message.message_id,
                                        reply_markup=keyboards.get_questions_keyboard(question.chat_id))
            await utils.AdmAskQuestions.asking.set()

    @dispatcher.callback_query_handler(lambda call: call.data == 'STOP_ANSWER',
                                       state=utils.AdmAskQuestions.continue_answer)
    async def stop_answering(call: types.CallbackQuery, state: FSMContext):
        await bot.delete_message(call.from_user.id, call.message.message_id)

        await state.finish()
