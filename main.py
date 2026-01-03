import os
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN пуст. Добавь BOT_TOKEN в переменные Railway / .env")

BOT_NAME = "Лёгкость"

# ===================== ТЕКСТЫ =====================

START_TEXT = (
    "Если вы устали: 😔\n\n"
    "— от тревожности\n"
    "— внутреннего напряжения, агрессии\n"
    "— страхов\n"
    "— переживания\n"
    "— злости\n"
    "— недовольства собой или миром вокруг.\n\n"
    "Если нет: 🙁\n\n"
    "— покоя и лёгкости внутри.\n\n"
    "Если вам просто хочется вернуть\n"
    "красоту в жизни —\n\n"
    "тогда это для вас.\n\n"
    "Есть проверенный способ\n"
    "всё это отпустить 😊\n\n"
    "💡 Всего два упражнения,\n"
    "которые точно работают\n"
    "у всех без исключения.\n\n"
    "Проверено."
)

ABOUT_TEXT = (
    "Обо мне\n\n"
    "С 2009 года — а это уже 17 лет — я занимаюсь эзотерикой ✨\n\n"
    "Что меня сподвигло на это?!\n"
    "Хороший вопрос.\n"
    "В первую очередь — поиск ответов на то,\n"
    "что такое жизнь и кто есть я\n"
    "за пределами этого тела,\n"
    "здесь, на Земле 🤷‍♂️🌍\n\n"
    "Пришёл ли я к этому?\n"
    "Да, более чем.\n\n"
    "За это время я прошёл огромное количество практик и техник:\n"
    "от медитаций, космоэнергетики, таро, магии\n"
    "и множества других направлений —\n"
    "везде, где можно было хоть как-то приблизиться\n"
    "к этим ответам 🔍\n\n"
    "И, конечно же, были вещи,\n"
    "которые оказались абсолютно нерабочими,\n"
    "какие-то уводили совсем не в ту сторону\n"
    "и были пустой тратой времени.\n\n"
    "Но были и те,\n"
    "которые оказались очень эффективными\n"
    "и реально помогающими в жизни 🌱\n\n"
    "И как раз то, что действительно работает,\n"
    "я и предлагаю вам.\n\n"
    "То, что помогает гарантированно,\n"
    "на 100% сделать жизнь легче\n"
    "и вернуть лёгкость 😊"
)


ACCESS_TEXT = (
    "🔒 Доступ будет открыт совсем скоро.\n"
    "Спасибо за доверие 🤍"
)

# Два упражнения (можешь править тексты как хочешь)
WRITE = [
    "✍️ Остановись на пару минут.\n\n"
    "Выпиши всё, что сейчас внутри.\n"
    "Не редактируй, просто выгружай.\n\n"
    "После каждого пункта дописывай:\n"
    "«Я позволяю этому быть»\n\n"
    "Дай состоянию выйти.\n"
    "Если хочется — зевни, потянись, выдохни.\n\n"
    "Готово ✅\n\n"
    "Если хочешь — повтори ещё раз с тем, что осталось."
]

BREATH = [
    "😮‍💨 Остановись и почувствуй опору.\n\n"
    "Сделай глубокий вдох и медленный выдох.\n\n"
    "В конце выдоха скажи:\n"
    "«Я позволяю этому быть»\n\n"
    "Повтори 1–3 раза, если нужно.\n\n"
    "Готово ✅\n\n"
    "Можно возвращаться к этому в любой момент."
]

# !!! Поменяй на реальное имя файла, которое лежит в репозитории рядом с main.py
ABOUT_PHOTO_PATH = "IMG_5147.jpeg"


# ===================== КНОПКИ =====================

def kb_start():
    kb = InlineKeyboardBuilder()
    kb.button(text="👋 Обо мне", callback_data="about")
    kb.button(text="Получить доступ", callback_data="get_access")
    kb.adjust(1)
    return kb.as_markup()


def kb_about_end():
    kb = InlineKeyboardBuilder()
    kb.button(text="Получить доступ", callback_data="get_access")
    kb.adjust(1)
    return kb.as_markup()


def kb_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="✍️ Выписать и позволить", callback_data="write")
    kb.button(text="😮‍💨 Вдох и позволение", callback_data="breath")
    kb.button(text="🏠 В начало", callback_data="home")
    kb.adjust(1)
    return kb.as_markup()


def kb_back_home():
    kb = InlineKeyboardBuilder()
    kb.button(text="🏠 В начало", callback_data="home")
    kb.adjust(1)
    return kb.as_markup()


# ===================== БОТ =====================

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # /start
    @dp.message(CommandStart())
    async def start(m: Message):
        await m.answer(
            f"*{BOT_NAME}*\n\n{START_TEXT}",
            parse_mode="Markdown",
            reply_markup=kb_start()
        )

    # В начало
    @dp.callback_query(F.data == "home")
    async def home(c: CallbackQuery):
        await c.message.answer(
            f"*{BOT_NAME}*\n\n{START_TEXT}",
            parse_mode="Markdown",
            reply_markup=kb_start()
        )
        await c.answer()

    # Получить доступ (важно: callback_data == "get_access" везде одинаковый)
    @dp.callback_query(F.data == "get_access")
    async def access(c: CallbackQuery):
        await c.message.answer(
            ACCESS_TEXT,
            parse_mode="Markdown",
            reply_markup=kb_back_home()
        )
        await c.answer()

    # Обо мне (в конце — дублирующая кнопка "Получить доступ")
    @dp.callback_query(F.data == "about")
    async def about(c: CallbackQuery):
        try:
            photo = FSInputFile(ABOUT_PHOTO_PATH)
            await c.message.answer_photo(
                photo=photo,
                caption=ABOUT_TEXT,
                parse_mode="Markdown",
                reply_markup=kb_about_end()
            )
        except Exception:
            await c.message.answer(
                ABOUT_TEXT,
                parse_mode="Markdown",
                reply_markup=kb_about_end()
            )

        await c.answer()

    # Упражнение 1
    @dp.callback_query(F.data == "write")
    async def write(c: CallbackQuery):
        await c.message.answer("\n\n".join(WRITE), reply_markup=kb_menu())
        await c.answer()

    # Упражнение 2
    @dp.callback_query(F.data == "breath")
    async def breath(c: CallbackQuery):
        await c.message.answer("\n\n".join(BREATH), reply_markup=kb_menu())
        await c.answer()

    # (необязательно) Команда /menu если захочешь
    @dp.message(F.text == "/menu")
    async def menu_cmd(m: Message):
        await m.answer("Выбери упражнение:", reply_markup=kb_menu())

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
