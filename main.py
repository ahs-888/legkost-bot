import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
BOT_NAME = "Лёгкость..."

def kb_start():
    kb = InlineKeyboardBuilder()
    kb.button(text="Получить доступ", callback_data="get_access")
    kb.button(text="Как это работает", callback_data="how")
    kb.adjust(1)
    return kb.as_markup()

def kb_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="📝 Выписать и позволить", callback_data="w1")
    kb.button(text="😮‍💨 Вдох и позволение", callback_data="b1")
    kb.adjust(1)
    return kb.as_markup()

def kb_next(tag):
    kb = InlineKeyboardBuilder()
    kb.button(text="Дальше", callback_data=tag)
    return kb.as_markup()

START_TEXT = (
    "Если вы устали: 😔\n\n"
    "— от тревожности\n"
    "— внутреннего напряжения, агрессии\n"
    "— страхов\n"
    "— переживания\n"
    "— злости\n"
    "— недовольства собой или миром вокруг.\n\n"
    "Если нет: 😕\n\n"
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



HOW_TEXT = (
    "Это не медицина и не психотерапия.\n\n"
    "Это простой инструмент саморегуляции:\n"
    "не подавлять состояние и не застревать в нём."
)

WRITE = [
    "📝 Остановись на пару минут.\nВозьми заметки или лист.",
    "Выпиши всё, что сейчас внутри.\nНе фильтруй. Просто пиши.",
    "После каждого пункта дописывай:\n«Я позволяю этому быть».",
    "Завершение:\nДай состоянию выйти. Этого достаточно."
]

BREATH = [
    "😮‍💨 Остановись и почувствуй опору.",
    "Сделай глубокий вдох и медленный выдох.\nБез мыслей.",
    "В конце выдоха скажи:\n«Я позволяю».",
    "Повтори 1–3 раза, если нужно."
]

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def start(m: Message):
        await m.answer(
            f"**{BOT_NAME}**\n\n{START_TEXT}",
            parse_mode="Markdown",
            reply_markup=kb_start()
        )

    @dp.callback_query(F.data == "how")
    async def how(c: CallbackQuery):
        await c.message.answer(HOW_TEXT)

    @dp.callback_query(F.data == "get_access")
    async def access(c: CallbackQuery):
        await c.message.answer("Доступ открыт ✅", reply_markup=kb_menu())

    @dp.callback_query(F.data == "w1")
    async def w1(c: CallbackQuery):
        await c.message.answer(WRITE[0], reply_markup=kb_next("w2"))

    @dp.callback_query(F.data == "w2")
    async def w2(c: CallbackQuery):
        await c.message.answer(WRITE[1], reply_markup=kb_next("w3"))

    @dp.callback_query(F.data == "w3")
    async def w3(c: CallbackQuery):
        await c.message.answer(WRITE[2], reply_markup=kb_next("w4"))

    @dp.callback_query(F.data == "w4")
    async def w4(c: CallbackQuery):
        await c.message.answer(WRITE[3], reply_markup=kb_menu())

    @dp.callback_query(F.data == "b1")
    async def b1(c: CallbackQuery):
        await c.message.answer(BREATH[0], reply_markup=kb_next("b2"))

    @dp.callback_query(F.data == "b2")
    async def b2(c: CallbackQuery):
        await c.message.answer(BREATH[1], reply_markup=kb_next("b3"))

    @dp.callback_query(F.data == "b3")
    async def b3(c: CallbackQuery):
        await c.message.answer(BREATH[2], reply_markup=kb_next("b4"))

    @dp.callback_query(F.data == "b4")
    async def b4(c: CallbackQuery):
        await c.message.answer(BREATH[3], reply_markup=kb_menu())

    await dp.start_polling(bot)

asyncio.run(main())
