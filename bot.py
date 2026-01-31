from aiohttp import web
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
from dotenv import load_dotenv

# ======================
# ENV
# ======================
load_dotenv()
BOT_TOKEN = os.getenv("PAYMENT_BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("PAYMENT_BOT_TOKEN is not set")

MAIN_BOT_USERNAME = "leya_tocka_bot"  # без @

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ======================
# PRODUCTS
# ======================
PRODUCTS = {
    "leya": {
        "title": "Лея — бережный ИИ-проводник",
        "description": "Поддержка и внутренняя опора 🤍\nДоступ 7 дней",
        "price": 290,
    },
    "elira": {
        "title": "Элира — путь к желаниям",
        "description": "Контакт с желаниями 🌸\nДоступ 7 дней",
        "price": 590,
    },
    "amira": {
        "title": "Амира — путь к самоценности",
        "description": "Внутренняя ценность 🌼\nДоступ 7 дней",
        "price": 390,
    },
    "nera": {
        "title": "Нера — путь к женской силе",
        "description": "Энергия и проявленность 🔥\nДоступ 7 дней",
        "price": 790,
    },
}

# ======================
# START
# ======================
@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"{p['title']} — {p['price']} ⭐", callback_data=f"buy_{k}")]
        for k, p in PRODUCTS.items()
    ])

    await message.answer(
        "💗 Оплата доступа\n\n"
        "Выберите проводника — оплата проходит прямо в Telegram ⭐",
        reply_markup=keyboard
    )

# ======================
# INVOICE
# ======================
@dp.callback_query(lambda c: c.data.startswith("buy_"))
async def buy(callback: types.CallbackQuery):
    key = callback.data.replace("buy_", "")
    product = PRODUCTS.get(key)

    if not product:
        await callback.answer("Товар не найден", show_alert=True)
        return

    await callback.answer()

    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title=product["title"],
        description=product["description"],
        payload=f"{key}_access",
        provider_token="",  # ⭐ Telegram Stars
        currency="XTR",
        prices=[LabeledPrice(label="Доступ", amount=product["price"])],
    )

# ======================
# PRE-CHECKOUT
# ======================
@dp.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    await query.answer(ok=True)

# ======================
# SUCCESS
# ======================
@dp.message(lambda m: m.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def success(message: types.Message):
    payload = message.successful_payment.invoice_payload
    guide_key = payload.replace("_access", "")

    url = f"https://t.me/{MAIN_BOT_USERNAME}?start={guide_key}"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Вернуться к проводнику", url=url)]
    ])

    await message.answer(
        "💗 Оплата прошла успешно.\n"
        "Доступ активирован.\n\n"
        "Нажмите кнопку ниже, чтобы продолжить путь 🌷",
        reply_markup=keyboard
    )

async def healthcheck(request):
    return web.Response(text="OK")

async def start_webserver():
    app = web.Application()
    app.router.add_get("/", healthcheck)

    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# ======================
# MAIN
# ======================
async def main():
    await bot.delete_webhook(drop_pending_updates=True)

async def main():
    await start_webserver()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

