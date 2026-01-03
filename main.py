import os
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN пуст. Добавь BOT_TOKEN в переменные Railway / .env")

BOT_NAME = "Лёгкость..."

# ===================== ТЕКСТЫ (НЕ ТРОГАТЬ) =====================

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

# ===================== ФАЙЛЫ (ФОТО) =====================

# Фото "Обо мне"
ABOUT_PHOTO_PATH = "IMG_5147.jpeg"

# Фото упражнений (ты их уже загрузил в репозиторий рядом с main.py)
EXERCISE_PHOTOS = [
    "IMG_5017.png",
    "IMG_5018.png",
    "IMG_5019.png",
]

# Режим оплаты:
# 0 = сразу показываем упражнения (удобно для теста)
# 1 = показываем заглушку ACCESS_TEXT (позже подключишь оплату)
PAYWALL_ENABLED = os.getenv("PAYWALL_ENABLED", "0") == "1"


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


def kb_back_home():
    kb = InlineKeyboardBuilder()
    kb.button(text="🏠 В начало", callback_data="home")
    kb.adjust(1)
    return kb.as_markup()


# ===================== ХЕЛПЕРЫ =====================

async def send_exercises(c: CallbackQuery):
    """
    Отправляем упражнения как фото (без текста, без лишних кнопок).
    После — даём кнопку "В начало".
    """
    # Проверка наличия файлов (чтобы сразу понять, если имя не совпало)
    missing = [p for p in EXERCISE_PHOTOS if not os.path.exists(p)]
    if missing:
        await c.message.answer(
            "❌ Не нашёл файлы упражнений в проекте:\n"
            + "\n".join(missing)
            + "\n\nПроверь названия файлов в репозитории и в коде (EXERCISE_PHOTOS).",
            reply_markup=kb_back_home()
        )
        return

    media = [InputMediaPhoto(media=FSInputFile(path)) for path in EXERCISE_PHOTOS]
    await c.message.answer_media_group(media=media)
    await c.message.answer("✅ Упражнения открыты.", reply_markup=kb_back_home())


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

    # Получить доступ
    @dp.callback_query(F.data == "get_access")
    async def access(c: CallbackQuery):
        # Позже здесь будет проверка оплаты.
        # Пока: если PAYWALL_ENABLED=1 -> заглушка, иначе -> сразу фото-упражнения.
        if PAYWALL_ENABLED:
            await c.message.answer(
                ACCESS_TEXT,
                parse_mode="Markdown",
                reply_markup=kb_back_home()
            )
        else:
            await send_exercises(c)

        await c.answer()

    # Обо мне (в конце — кнопка "Получить доступ")
    @dp.callback_query(F.data == "about")
    async def about(c: CallbackQuery):
        try:
            if os.path.exists(ABOUT_PHOTO_PATH):
                photo = FSInputFile(ABOUT_PHOTO_PATH)
                await c.message.answer_photo(
                    photo=photo,
                    caption=ABOUT_TEXT,
                    parse_mode="Markdown",
                    reply_markup=kb_about_end()
                )
            else:
                # Если фото не нашли — просто текст
                await c.message.answer(
                    ABOUT_TEXT,
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

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
