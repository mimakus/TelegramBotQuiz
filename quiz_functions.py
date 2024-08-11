import aiosqlite
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from quiz_file import load_quiz


def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()

    for i in range(0,len(answer_options)):
        option = answer_options[i]
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data="right_answer"+ str(i) + option if option == right_answer else "wrong_answer"+ str(i) + option)
        )

    builder.adjust(1)
    return builder.as_markup()


async def create_table(DB_NAME):
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Создаем таблицу
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
        # Создаем таблицу
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_answers (user_id INTEGER PRIMARY KEY, answers TEXT, score INTEGER)''')
        # Сохраняем изменения
        await db.commit()



async def get_question(message, user_id, quiz_data, DB_NAME):
    # Получение текущего вопроса из словаря состояний пользователя
    current_question_index = await get_quiz_index(user_id, DB_NAME)
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)

    
async def get_quiz_index(user_id, DB_NAME):
     # Подключаемся к базе данных
     async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0
            

async def get_user_answers_options(user_id, DB_NAME): 
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT answers FROM quiz_answers WHERE user_id = (?)', (user_id, )) as cursor:
            answers = await cursor.fetchone()
            return answers
        

async def get_user_score(user_id, DB_NAME):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT score FROM quiz_answers WHERE user_id = (?)', (user_id, )) as cursor:
            score = await cursor.fetchone()
            return score[0]


async def update_quiz_index(user_id, index, DB_NAME, score = 0, option = None,):
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        answers = await get_user_answers_options(user_id, DB_NAME)
        if option is not None:
            if answers is not None:
                 ans = answers[0]
                 ans = str(ans) + ' ' + str(option)
            else:
                ans = str(option)
        else:
            ans = ''

        await db.execute('INSERT OR REPLACE INTO quiz_answers (user_id, answers, score) VALUES (?, ?, ?)', (user_id, ans, score))
        # Сохраняем изменения
        await db.commit()

