
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import  ReplyKeyboardBuilder
from aiogram import F
from quiz_file import load_quiz
from quiz_functions import create_table, get_question, get_quiz_index, get_user_answers_options, get_user_score, update_quiz_index


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Замените "YOUR_BOT_TOKEN" на токен, который вы получили от BotFather
API_TOKEN = 'YOUR_BOT_TOKEN'

# Объект бота
bot = Bot(token=API_TOKEN)
# Диспетчер
dp = Dispatcher()


# Зададим имя базы данных
DB_NAME = 'quiz_bot.db'

# Структура квиза, функция из файла.
quiz_data = load_quiz()


async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    await update_quiz_index(user_id, current_question_index, DB_NAME)
    await get_question(message, user_id, quiz_data, DB_NAME)


@dp.callback_query(F.data.startswith("right_answer"))
async def right_answer(callback: types.CallbackQuery):

    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    await callback.message.answer(f"Ваш ответ: {callback.data[13:]}")
    await callback.message.answer("Верно!")
    current_question_index = await get_quiz_index(callback.from_user.id, DB_NAME)
    score = await get_user_score(callback.from_user.id, DB_NAME)
    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    score = score + 1
    user_option = int(callback.data[12:13])
    await update_quiz_index(callback.from_user.id, current_question_index, DB_NAME, score, user_option)


    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id, quiz_data, DB_NAME)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")
        user_id = callback.from_user.id
        user_answers_options = await get_user_answers_options(user_id, DB_NAME)
        user_answers_options = user_answers_options[0].split()
        score = await get_user_score(user_id, DB_NAME)
        score = await get_user_score(user_id, DB_NAME)
        len_answers =len(user_answers_options)
        len_questions = len(quiz_data)
        await callback.message.answer(f"Вы ответили на {len_answers} вопросов из {len_questions}. Правильных ответов: {score}")


@dp.callback_query(F.data.startswith("wrong_answer"))
async def wrong_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    # Получение текущего вопроса из словаря состояний пользователя
    current_question_index = await get_quiz_index(callback.from_user.id, DB_NAME)
    correct_option = quiz_data[current_question_index]['correct_option']
    # Получение правильного ответа
    correct_answer = quiz_data[current_question_index]['options'][correct_option]
    score = await get_user_score(callback.from_user.id, DB_NAME)
    user_option = int(callback.data[12:13])

    await callback.message.answer(f"Ваш ответ: {callback.data[13:]}")
    await callback.message.answer(f"Неправильно. Правильный ответ: {correct_answer}")

    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index, DB_NAME, score, user_option)


    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id, quiz_data, DB_NAME)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")
        user_id = callback.from_user.id
        user_answers_options = await get_user_answers_options(user_id, DB_NAME)
        user_answers_options = user_answers_options[0].split()
        score = await get_user_score(user_id, DB_NAME)
        score = await get_user_score(user_id, DB_NAME)
        len_answers =len(user_answers_options)
        len_questions = len(quiz_data)
        await callback.message.answer(f"Вы ответили на {len_answers} вопросов из {len_questions}. Правильных ответов: {score}")


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))


# Хэндлер на вывод ответов
@dp.message(Command("result"))
async def cmd_result(message: types.Message):

    user_id = message.from_user.id
    user_answers_options = await get_user_answers_options(user_id, DB_NAME)
    user_answers_options = user_answers_options[0].split()
    # загружаем из бд количество правильных ответов
    score = await get_user_score(user_id, DB_NAME)
    # Записываем текст ответов пользователя
   # user_answers_text = ""
    len_answers =len(user_answers_options)
    len_questions = len(quiz_data)
  #  for i in range(0, len_answers):
  #      i_answer_text = quiz_data[i]['options'][user_answers_options]
   #     user_answers_text = user_answers_text + ', ' + i_answer_text
    
    await message.answer(f"Вы ответили на {len_answers} вопросов из {len_questions}. Правильных ответов: {score}")




# Хэндлер на команду /quiz
@dp.message(F.text=="Начать игру")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):

    await message.answer(f"Давайте начнем квиз!")
    await new_quiz(message)


# Запуск процесса поллинга новых апдейтов
async def main():

    # Запускаем создание таблицы базы данных
    await create_table(DB_NAME)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
