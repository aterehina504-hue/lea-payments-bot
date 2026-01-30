import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

BOT_TOKEN = os.getenv("BOT_TOKEN")
MAIN_BOT_URL = "https://t.me/leya_tocka_bot"  # основной бот

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# ---- ДАННЫЕ ПРОВОДНИКОВ ----
GUIDES = {
    "leya": {
        "title": "Лея — бережный ИИ-проводник",
        "description": "Поддержка и внутренняя опора 🤍\nРазовый доступ навсегда",
        "price": 490
    },
    "elira": {
        "title": "Элира — путь к своим желаниям",
        "description": "Контакт с желаниями и собой 🌸\nРазовый доступ навсегда",
        "price": 690
    },
    "amira": {
        "title": "Амира — путь к самоценности",
        "description": "Внутренняя ценность и опора 🌼\nРазовый доступ навсегда",
        "price": 890
    },
    "nera": {
        "title": "Нера — путь к женской силе",
        "description": "Энергия и проявленность 🔥\nРазовый доступ навсегда",
        "price": 1090
    },
    "all": {
        "title": "Все проводники — полный доступ",
        "description": (
            "Лея • Элира • Амира • Нера\n\n"
            "Полный доступ ко всем путям.\n"
            "Навсегда 🤍"
        ),
        "price": 1990
    }
}

# ---- /start ----
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton("🌷 Лея — 490 ⭐", callback_data="buy_leya"),
        InlineKeyboardButton("🌸 Элира — 690 ⭐", callback_data="buy_elira"),
        InlineKeyboardButton("🌼 Амира — 890 ⭐", callback_data="buy_amira"),
        InlineKeyboardButton("🔥 Нера — 1090 ⭐", callback_data="buy_nera"),
        InlineKeyboardButton("💎 Все проводники — 1990 ⭐", callback_data="buy_all"),
    )

    await message.answer(
        "💗 Оплата доступа\n\n"
        "Выберите проводника — оплата проходит прямо в Telegram ⭐",
        reply_markup=keyboard
    )

# ---- ОТПРАВКА INVOICE ----
@dp.callback_query_handler(lambda c: c.data.startswith("buy_"))
async def send_invoice(callback: types.CallbackQuery):
    guide_key = callback.data.replace("buy_", "")
    guide = GUIDES[guide_key]

    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title=guide["title"],
        description=guide["description"],
        payload=f"{guide_key}_access",
        currency="XTR",  # Telegram Stars
        prices=[
            types.LabeledPrice(
                label="Доступ",
                amount=guide["price"]
            )
        ],
    )

# ---- ОБЯЗАТЕЛЬНО ----
@dp.pre_checkout_query_handler(lambda q: True)
async def pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# ---- ПОСЛЕ ОПЛАТЫ ----
@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    payload = message.successful_payment.invoice_payload
    guide_key = payload.replace("_access", "")

    return_url = f"{MAIN_BOT_URL}?start={guide_key}"

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text="🔙 Вернуться к проводнику",
            url=return_url
        )
    )

    await message.answer(
        "💗 Оплата прошла успешно.\n"
        "Доступ активирован.\n\n"
        "Нажмите кнопку ниже, чтобы продолжить путь 🌷",
        reply_markup=keyboard
    )

# ---- ЗАПУСК ----
if __name__ == "__main__":
    executor.start_polling(dp)
