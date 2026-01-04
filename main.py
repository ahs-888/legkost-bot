import os
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    FSInputFile,
    InputMediaPhoto,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN пуст. Проверь .env")

BOT_NAME = "Лёгкость…"


# ===================== ТЕКСТЫ (НЕ ТРОГАЕМ) =====================

START_TEXT = (
    "Если вы устали: 😔\n\n"
    "— от тревожности\n"
    "— внутреннего напряжения, агрессии\n"
    "— страхов\n"
    "— переживания\n"
    "— злости\n"
    "— недовольства собой или миром\n"
    "вокруг.\n\n"
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
    "С 2009 года — а это уже 17 лет — я\n"
    "занимаюсь эзотерикой ✨\n\n"
    "Что меня сподвигло на это?!\n"
    "Хороший вопрос.\n"
    "В первую очередь — поиск ответов\n"
    "на то,\n"
    "что такое жизнь и кто есть я\n"
    "за пределами этого тела,\n"
    "здесь, на Земле 🤷‍♂️🌍\n\n"
    "Пришёл ли я к этому?\n"
    "Да, более чем.\n\n"
    "За это время я прошёл огромное\n"
    "количество практик и техник:\n"
    "от медитаций, космоэнергетики,\n"
    "таро, магии\n"
    "и множества других направлений —\n"
    "везде, где можно было хоть как-то\n"
    "приблизиться\n"
    "к этим ответам 🔎\n\n"
    "И, конечно же, были вещи,\n"
    "которые оказались абсолютно\n"
    "нерабочими,\n"
    "какие-то уводили совсем не в ту\n"
    "сторону\n"
    "и были пустой тратой времени.\n\n"
    "Но были и те,\n"
    "которые оказались очень\n"
    "эффективными\n"
    "и реально помогающими в жизни\n"
    "🌱\n\n"
    "И как раз то, что действительно\n"
    "работает,\n"
    "я и предлагаю вам.\n\n"
    "То, что помогает гарантированно,\n"
    "на 100% сделать жизнь легче\n"
    "и вернуть лёгкость 😊"
)




# ===================== ФАЙЛЫ (ФОТО) =====================

ABOUT_PHOTO_PATH = "IMG_5147.jpeg"

EXERCISE_PHOTOS = [
    "IMG_5017.png",
    "IMG_5018.png",
    "IMG_5019.png",
]


# ===================== КНОПКИ =====================

def kb_start():
    kb = InlineKeyboardBuilder()
    kb.button(text="👋 Обо мне", callback_data="about")
    kb.button(text="Попробовать практику🌿", callback_data="get_access")
    kb.adjust(1)
    return kb.as_markup()


def kb_about_end():
    kb = InlineKeyboardBuilder()
    kb.button(text="Попробовать практику🌿", callback_data="get_access")
    kb.button(text="🏠 В начало", callback_data="home")
    kb.adjust(1)
    return kb.as_markup()


def kb_pay_149():
    kb = InlineKeyboardBuilder()
    kb.button(text="☕ Попробовать за 149 ₽", callback_data="pay_149")
    kb.button(text="🏠 В начало", callback_data="home")
    kb.adjust(1)
    return kb.as_markup()


def kb_back_home():
    kb = InlineKeyboardBuilder()
    kb.button(text="🏠 В начало", callback_data="home")
    kb.adjust(1)
    return kb.as_markup()


# ===================== HELPERS =====================

async def send_exercises_album(message: Message):
    """
    Отправка альбома фото:
    - Без Markdown
    - Сначала альбом, затем отдельное сообщение с кнопкой
    """
    media = []
    for path in EXERCISE_PHOTOS:
        try:
            media.append(InputMediaPhoto(media=FSInputFile(path)))
        except Exception:
            # если файла нет — пропускаем
            pass

    if media:
        await message.answer_media_group(media)

    await message.answer(reply_markup=kb_back_home())



# ===================== BOT =====================

async def main():
    bot = Bot(token=BOT_TOKEN)  # parse_mode НЕ ставим
    dp = Dispatcher()

    # /start
    @dp.message(CommandStart())
    async def start(m: Message):
        await m.answer(f"{BOT_NAME}\n\n{START_TEXT}", reply_markup=kb_start())

    # В начало
    @dp.callback_query(F.data == "home")
    async def home(c: CallbackQuery):
        await c.message.answer(f"{BOT_NAME}\n\n{START_TEXT}", reply_markup=kb_start())
        await c.answer()

    # Получить доступ → экран перед оплатой
    @dp.callback_query(F.data == "get_access")
    async def get_access(c: CallbackQuery):
        await c.message.answer(PAY_TEXT, reply_markup=kb_pay_149())
        await c.answer()

    # "Оплата" (пока имитация): открываем упражнения
    @dp.callback_query(F.data == "pay_149")
    async def pay_149(c: CallbackQuery):
        # 1) Сообщение как на скрине
        await c.message.answer("✅ Упражнения практики открыты.")
        # 2) Фото альбомом
        await send_exercises_album(c.message)
        await c.answer()

    # Обо мне (фото + текст)
    @dp.callback_query(F.data == "about")
    async def about(c: CallbackQuery):
        try:
            photo = FSInputFile(ABOUT_PHOTO_PATH)
            await c.message.answer_photo(
                photo=photo,
                caption=ABOUT_TEXT,
                reply_markup=kb_about_end()
            )
        except Exception:
            # если фото не нашлось — отправим просто текст
            await c.message.answer(ABOUT_TEXT, reply_markup=kb_about_end())

        await c.answer()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
