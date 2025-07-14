from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from flask import Flask
import threading

BOT_TOKEN = "7863509137:AAHBuRbtzMAOM_yBbVZASfx-oORubvQYxY8"
ALLOWED_USERS = [7863509137]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ALLOWED_USERS:
        await update.message.reply_text("أهلاً بك في بوت مراقبة العملات الرقمية! اكتب /crypto BTC أو /top.")
    else:
        await update.message.reply_text("غير مصرح لك باستخدام هذا البوت.")

async def crypto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ALLOWED_USERS:
        return
    if len(context.args) != 1:
        await update.message.reply_text("اكتب الأمر بهذا الشكل: /crypto BTC")
        return

    symbol = context.args[0].lower()
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"

    try:
        res = requests.get(url)
        data = res.json()
        price = data[symbol]["usd"]
        await update.message.reply_text(f"سعر {symbol.upper()} الآن: ${price}")
    except:
        await update.message.reply_text("تعذر الحصول على السعر. تأكد من الرمز.")

async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ALLOWED_USERS:
        return
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=5&page=1"
    res = requests.get(url)
    data = res.json()
    msg = "🔝 أعلى 5 عملات:\n"
    for coin in data:
        msg += f"{coin['name']} ({coin['symbol'].upper()}): ${coin['current_price']}\n"
    await update.message.reply_text(msg)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("crypto", crypto))
app.add_handler(CommandHandler("top", top))

def run_flask():
    flask_app = Flask(__name__)
    @flask_app.route('/')
    def index():
        return "Crypto Bot is running!"
    flask_app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_flask).start()
app.run_polling()
