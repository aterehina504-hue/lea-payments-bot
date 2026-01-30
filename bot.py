import os
import asyncio
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    LabeledPrice,
    PreCheckoutQuery,
)
from aiogram.enums import ContentType


# ====== НАСТРОЙКИ ======
BOT_TOKEN = os.getenv("BOT_TOKEN")  # токен платёжного бота
MAIN_BOT_URL = "https://t.me/leya_tocka_bot"  # основной бот

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# ====== ПРОВОДНИКИ ======
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


# ====== /start ======
@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌷 Лея — 490 ⭐", callback_data="buy_leya")],
        [InlineKeyboardButton(text="🌸 Элира — 690 ⭐", callback_data="buy_elira")],
        [InlineKeyboardButton(text="🌼 Амира — 890 ⭐", callback_data="buy_amira")],
        [InlineKeyboardButton(text="🔥 Нера — 1090 ⭐", callback_data="buy_nera")],
        [InlineKeyboardButton(text="💎 Все проводники — 1990 ⭐", callback_data="buy_all")],
    ])

    await message.answer(
        "💗 Оплата доступа\n\n"
        "Выберите проводника — оплата проходит прямо в Telegram ⭐",
        reply_markup=keyboard,
    )


# ====== СОЗДАНИЕ СЧЁТА ======
@dp.callback_query()
async def send_invoice(callback: types.CallbackQuery):
    if not callback.data.startswith("buy_"):
        return

    await callback.answer()  # чтобы не было "часиков"

    key = callback.data.replace("buy_", "")
    guide = GUIDES[key]

    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title=guide["title"],
        description=guide["description"],
        payload=f"{key}_access",
        provider_token="",          # 🔥 ОБЯЗАТЕЛЬНО
        currency="XTR",             # Telegram Stars
        prices=[
            LabeledPrice(
                label="Доступ",
                amount=guide["price"]
            )
        ],
    )

# ====== ПОДТВЕРЖДЕНИЕ ОПЛАТЫ ======
@dp.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    await query.answer(ok=True)


# ====== ПОСЛЕ ОПЛАТЫ ======
@dp.message(lambda m: m.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    payload = message.successful_payment.invoice_payload
    guide_key = payload.replace("_access", "")

    return_url = f"{MAIN_BOT_URL}?start={guide_key}"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Вернуться к проводнику", url=return_url)]
    ])

    await message.answer(
        "💗 Оплата прошла успешно.\n"
        "Доступ активирован.\n\n"
        "Нажмите кнопку ниже, чтобы продолжить путь 🌷",
        reply_markup=keyboard,
    )


# ====== ФИКТИВНЫЙ HTTP-СЕРВЕР ДЛЯ RENDER FREE ======
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")


def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), DummyHandler)
    server.serve_forever()


# ====== ЗАПУСК ======
async def main():
    threading.Thread(target=run_dummy_server, daemon=True).start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())



