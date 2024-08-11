def load_quiz():
    quiz_data = [
    {
        'question': 'Что такое Python?',
        'options': ['Язык программирования', 'Тип данных', 'Музыкальный инструмент', 'Змея на английском'],
        'correct_option': 0
    },
    {
        'question': 'Какой тип данных используется для хранения целых чисел?',
        'options': ['int', 'float', 'str', 'natural'],
        'correct_option': 0
    },
    {
        'question': 'Какая функция выводит текст в консоль или на экран?',
        'options': ['type()', 'print()', 'write()', 'str()'],
        'correct_option': 1
    },
    {
        'question': 'Как выглядит лист?',
        'options': ['[1,2]', '{1,2}', '(1,2)', '[1:2]'],
        'correct_option': 0
    },
    {
        'question': 'Какой тип данных принимет значение: True?',
        'options': ['tuple', 'float', 'str', 'bool'],
        'correct_option': 3
    },
    {
        'question': 'Что означает //?',
        'options': ['комментарий', 'возведение в корень', 'целочисленное деление', 'деление с остатком'],
        'correct_option': 2
    },
    {
        'question': 'Что делает Break?',
        'options': ['ломает систему', 'завершает цикл', 'ставит на паузу', 'тормозит'],
        'correct_option': 1
    },
    {
        'question': 'Как добавить модуль?',
        'options': ['import', 'export', 'teleport', 'port'],
        'correct_option': 0
    },
    {
        'question': 'Какой официальный бот для создания telegram ботов?',
        'options': ['MotherBot', 'FatherBot', 'BotMother', 'BotFather'],
        'correct_option': 3
    },
    {
        'question': 'Какой результат операции: "2" * 3?',
        'options': ['6', '23', '222', 'ошибка'],
        'correct_option': 2
    }
    # Добавьте другие вопросы
]
    return quiz_data
    