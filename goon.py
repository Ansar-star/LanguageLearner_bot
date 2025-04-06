import asyncio
import random
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = ""  

bot = Bot(token=TOKEN)
dp = Dispatcher()


words = {
    "Английский": {
        "apple": "яблоко", "dog": "собака", "car": "машина", "house": "дом",
        "sun": "солнце", "tree": "дерево", "book": "книга", "friend": "друг",
        "school": "школа", "cat": "кот", "food": "еда", "computer": "компьютер",
        "phone": "телефон", "pen": "ручка", "table": "стол", "chair": "стул",
        "window": "окно", "city": "город", "mountain": "гора", "river": "река"
    },
    "Испанский": {
        "manzana": "яблоко", "perro": "собака", "coche": "машина", "casa": "дом",
        "sol": "солнце", "árbol": "дерево", "libro": "книга", "amigo": "друг",
        "escuela": "школа", "gato": "кот", "comida": "еда", "ordenador": "компьютер",
        "teléfono": "телефон", "bolígrafo": "ручка", "mesa": "стол", "silla": "стул",
        "ventana": "окно", "ciudad": "город", "montaña": "гора", "río": "река"
    },
    "Французский": {
        "pomme": "яблоко", "chien": "собака", "voiture": "машина", "maison": "дом",
        "soleil": "солнце", "arbre": "дерево", "livre": "книга", "ami": "друг",
        "école": "школа", "chat": "кот", "nourriture": "еда", "ordinateur": "компьютер",
        "téléphone": "телефон", "stylo": "ручка", "table": "стол", "chaise": "стул",
        "fenêtre": "окно", "ville": "город", "montagne": "гора", "rivière": "река"
    },
}

emoji_words = {
    "Английский": {"🌞": "sun", "🚗": "car", "🐶": "dog", "🏠": "house", "🍏": "apple"},
    "Испанский": {"🌞": "sol", "🚗": "coche", "🐶": "perro", "🏠": "casa", "🍏": "manzana"},
    "Французский": {"🌞": "soleil", "🚗": "voiture", "🐶": "chien", "🏠": "maison", "🍏": "pomme"},
}

sentences = {
    "Английский": [
        ("I am a student", ["I", "am", "a", "student"]),
        ("This is my house", ["This", "is", "my", "house"]),
        ("He has a dog", ["He", "has", "a", "dog"]),
        ("The sun is bright", ["The", "sun", "is", "bright"])
    ],
    "Испанский": [
        ("Yo soy un estudiante", ["Yo", "soy", "un", "estudiante"]),
        ("Esta es mi casa", ["Esta", "es", "mi", "casa"]),
        ("Él tiene un perro", ["Él", "tiene", "un", "perro"]),
        ("El sol es brillante", ["El", "sol", "es", "brillante"])
    ],
    "Французский": [
        ("Je suis un étudiant", ["Je", "suis", "un", "étudiant"]),
        ("Ceci est ma maison", ["Ceci", "est", "ma", "maison"]),
        ("Il a un chien", ["Il", "a", "un", "chien"]),
        ("Le soleil est brillant", ["Le", "soleil", "est", "brillant"])
    ]
}

current_game = {}
user_languages = {}
used_words = {}
used_emoji = {}
sentence_game = {}


language_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=lang)] for lang in words.keys()],
    resize_keyboard=True
)

game_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Играть в слова")],
        [KeyboardButton(text="Квиз")],
        [KeyboardButton(text="Играть в эмодзи")],
        [KeyboardButton(text="Составь предложение")],
        [KeyboardButton(text="Словарь")],
        [KeyboardButton(text="🔄 Сменить язык")]
    ],
    resize_keyboard=True
)

@dp.message()
async def handle_message(message: types.Message):
    user_id = message.chat.id
    user_language = user_languages.get(user_id, "Английский")

    if message.text == "/start" or message.text == "🔄 Сменить язык":
        await message.answer("Привет! Выбери язык обучения:", reply_markup=language_keyboard)

    elif message.text in words.keys():
        user_languages[user_id] = message.text
        used_words[user_id] = set()
        used_emoji[user_id] = set()
        await message.answer(f"Ты выбрал {message.text}. Выбери игру:", reply_markup=game_keyboard)

    elif message.text == "Играть в слова":
        available_words = list(set(words[user_language].keys()) - used_words.get(user_id, set()))
        if available_words:
            word = random.choice(available_words)
            translation = words[user_language][word]
            current_game[user_id] = translation
            used_words[user_id].add(word)
            await message.answer(f"Как переводится слово: {word}?")
        else:
            await message.answer("✅ Все слова были использованы! Начни игру заново.", reply_markup=game_keyboard)
            used_words[user_id] = set()

    elif message.text == "Квиз":
        available_words = list(set(words[user_language].keys()) - used_words.get(user_id, set()))
        if available_words:
            word = random.choice(available_words)
            correct_translation = words[user_language][word]
            used_words[user_id].add(word)
            options = list(words[user_language].values())
            options.remove(correct_translation)
            choices = random.sample(options, min(3, len(options))) + [correct_translation]
            random.shuffle(choices)
            quiz_keyboard = ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=choice)] for choice in choices],
                resize_keyboard=True
            )
            current_game[user_id] = correct_translation
            await message.answer(f"Как переводится слово: {word}?", reply_markup=quiz_keyboard)
        else:
            await message.answer("✅ Все слова были использованы! Начни игру заново.", reply_markup=game_keyboard)
            used_words[user_id] = set()

    elif message.text == "Играть в эмодзи":
        available_emoji = list(set(emoji_words[user_language].keys()) - used_emoji.get(user_id, set()))
        if available_emoji:
            emoji = random.choice(available_emoji)
            translation = emoji_words[user_language][emoji]
            current_game[user_id] = translation
            used_emoji[user_id].add(emoji)
            options = list(emoji_words[user_language].values())
            options.remove(translation)
            choices = random.sample(options, min(3, len(options))) + [translation]
            random.shuffle(choices)
            quiz_keyboard = ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=choice)] for choice in choices],
                resize_keyboard=True
            )
            await message.answer(f"Что означает этот эмодзи? {emoji}", reply_markup=quiz_keyboard)
        else:
            await message.answer("✅ Все эмодзи были использованы! Начни игру заново.", reply_markup=game_keyboard)
            used_emoji[user_id] = set()

    elif message.text == "Составь предложение":
        original, parts = random.choice(sentences[user_language])
        shuffled = parts.copy()
        random.shuffle(shuffled)
        sentence_game[user_id] = {"answer": original, "parts": parts}
        btns = [[KeyboardButton(text=word)] for word in shuffled]
        btns.append([KeyboardButton(text="↩ Назад")])
        await message.answer("Собери предложение из слов:", reply_markup=ReplyKeyboardMarkup(keyboard=btns, resize_keyboard=True))

    elif message.text == "Словарь":
        dictionary = "\n".join([f"{word} - {translation}" for word, translation in words[user_language].items()])
        await message.answer(f"📖 Вот все слова, которые я знаю:\n{dictionary}")

    elif message.text == "↩ Назад":
        await message.answer("Выбери игру:", reply_markup=game_keyboard)

    else:
        correct_translation = current_game.get(user_id)
        if correct_translation:
            if message.text.lower().strip() == correct_translation.lower():
                await message.answer("✅ Верно! Выбери новую игру.", reply_markup=game_keyboard)
                del current_game[user_id]
            else:
                await message.answer("❌ Неправильно! Попробуй ещё раз.")
        elif user_id in sentence_game:
            user_sentence = message.text.strip()
            correct_sentence = sentence_game[user_id]["answer"]
            if user_sentence.lower() == correct_sentence.lower():
                await message.answer("✅ Правильно! Молодец!", reply_markup=game_keyboard)
                del sentence_game[user_id]
            else:
                await message.answer("❌ Неправильно. Попробуй снова или нажми ↩ Назад.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())