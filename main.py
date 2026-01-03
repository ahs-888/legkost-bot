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


# ===================== ТЕКСТЫ (НЕ ТРОГАТЬ) =====================
# ВАЖНО: Вставь сюда свои START_TEXT / ABOUT_TEXT / PAY_TEXT ровно как у тебя в файле.
# НИ ОДНОГО символа не меняй.

START_TEXT = (
    # <-- ВСТАВЬ ТУТ СВОЙ START_TEXT ИЗ main.py 1-в-1
)

ABOUT_TEXT = (
    # <-- ВСТАВЬ ТУТ СВОЙ ABOUT_TEXT ИЗ main.py 1-в-1
)

PAY_TEXT = (
    # <-- ВСТАВЬ ТУТ СВОЙ PAY_TEXT ИЗ main.py 1-в-1 (если он у тебя есть)
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
    kb.button(text="🌿 Попробовать практики", callback_data="try_practice")
    kb.adjust(1)
    return kb.as_markup()


def kb_about_end():
    kb = InlineKeyboardBuilder()
    kb.button(text="🌿 Попробовать практики", callback_data="try_practice")
    kb.button(text="🏡 В начало", callback_data="home")
    kb.adjust(1)
    return kb.as_markup()


def kb_pay_149():
    kb = InlineKeyboardBuilder()
    kb.button(text="☕ Попробовать за 149 ₽", callback_data="pay_149")
    kb.button(text="🏡 В начало", callback_data="home")
    kb.adjust(1)
    return kb.as_markup()


def kb_back_home():
    kb = InlineKeyboardBuilder()
    kb.button(text="🏡 В начало", callback_data="home")
    kb.adjust(1)
    return kb.as_markup()


# ===================== HELPERS =====================

async def send_exercises_album(message: Message):
    """
    - Отправляем альбом фото (если файлы найдены)
    - Затем отдельное сообщение с кнопкой "В начало"
    """
    media: list[InputMediaPhoto] = []

    for path in EXERCISE_PHOTOS:
        try:
            media.append(InputMediaPhoto(media=FSInputFile(path)))
        except Exception:
            pass

    if media:
        await message.answer_media_group(media)

    await message.answer("🏡 В начало", reply_markup=kb_back_home())


# ===================== BOT =====================

async def main():
    # parse_mode намеренно НЕ задаём, чтобы ничего не ломалось из-за разметки
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def start(m: Message):
        await m.answer(f"{BOT_NAME}\n\n{START_TEXT}", reply_markup=kb_start())

    @dp.callback_query(F.data == "home")
    async def home(c: CallbackQuery):
        await c.message.answer(f"{BOT_NAME}\n\n{START_TEXT}", reply_markup=kb_start())
        await c.answer()

    @dp.callback_query(F.data == "try_practice")
    async def try_practice(c: CallbackQuery):
        # Показываем экран перед "оплатой"
        await c.message.answer(PAY_TEXT, reply_markup=kb_pay_149())
        await c.answer()

    @dp.callback_query(F.data == "pay_149")
    async def pay_149(c: CallbackQuery):
        # 1) Сообщение как в твоём примере
        await c.message.answer("✅ Упражнения практики открыты.")
        # 2) Фото альбомом
        await send_exercises_album(c.message)
        await c.answer()

    @dp.callback_query(F.data == "about")
    async def about(c: CallbackQuery):
        try:
            await c.message.answer_photo(
                photo=FSInputFile(ABOUT_PHOTO_PATH),
                caption=ABOUT_TEXT,
                reply_markup=kb_about_end(),
            )
        except Exception:
            await c.message.answer(ABOUT_TEXT, reply_markup=kb_about_end())

        await c.answer()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
