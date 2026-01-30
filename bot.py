import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    LabeledPrice,
    PreCheckoutQuery,
)
from aiogram.enums import ContentType

BOT_TOKEN = os.getenv("BOT_TOKEN")
MAIN_BOT_URL = "https://t.me/leya_tocka_bot"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

GUIDES = {
    "leya": {
        "title": "Лея — бережный ИИ-проводник",
        "description": "Поддержка и внутренняя опора 🤍\nДоступ навсегда",
        "price": 490,
    },
    "elira": {
        "title": "Элира — путь к желаниям",
        "description": "Контакт с желаниями 🌸\nДоступ навсегда",
        "price": 690,
    },
    "amira": {
        "title": "Амира — путь к самоценности",
        "description": "Внутренняя ценность 🌼\nДоступ навсегда",
        "price": 890,
    },
    "nera": {
        "title": "Нера — путь к женской силе",
        "description": "Энергия и проявленность 🔥\nДоступ навсегда",
        "price": 1090,
    },
    "all": {
        "title": "Все проводники — полный доступ",
        "description": "Лея • Элира • Амира • Нера\nНавсегда 🤍",
        "price": 1990,
    },
}

@dp.message(Command("start"))
async def start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌷 Лея — 490 ⭐", callback_data="buy_leya")],
        [InlineKeyboardButton(text="🌸 Элира — 690 ⭐", callback_data="buy_elira")],
        [InlineKeyboardButton(text="🌼 Амира — 890 ⭐", callback_data="buy_amira")],
        [InlineKeyboardButton(text="🔥 Нера — 1090 ⭐", callback_data="buy_nera")],
        [InlineKeyboardButton(text="💎 Все проводники — 1990 ⭐", callback_data="buy_all")],
    ])

    await message.answer(
        "💗 Оплата доступа\n\nВыберите проводника:",
        reply_markup=kb,
    )

@dp.callback_query()
async def handle_buy(callback: types.CallbackQuery):
    if not callback.data.startswith("buy_"):
        return

    key = callback.data.replace("buy_", "")
    guide = GUIDES[key]

    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title=guide["title"],
        description=guide["description"],
        payload=f"{key}_access",
        currency="XTR",
        prices=[LabeledPrice(label="Доступ", amount=guide["price"])],
    )

@dp.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    await query.answer(ok=True)

@dp.message(lambda m: m.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def success(message: types.Message):
    payload = message.successful_payment.invoice_payload
    key = payload.replace("_access", "")

    url = f"{MAIN_BOT_URL}?start={key}"

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Вернуться к проводнику", url=url)]
    ])

    await message.answer(
        "💗 Оплата прошла успешно!\nДоступ активирован.",
        reply_markup=kb,
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
