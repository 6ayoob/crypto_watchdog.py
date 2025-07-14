from flask import Flask
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

BOT_TOKEN = "7863509137:AAHBuRbtzMAOM_yBbVZASfx-oORubvQYxY8"
ALLOWED_USERS = [7863509137]

app = Flask(__name__)

@app.route("/")
def home():
    return "Crypto Watchdog is running!"

async def crypto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ALLOWED_USERS:[7863509137]
        await update.message.reply_text("Access denied.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /crypto bitcoin")
        return

    coin = context.args[0].lower()
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"

    try:
        response = requests.get(url).json()
        price = response[coin]["usd"]
        await update.message.reply_text(f"{coin.capitalize()} price: ${price}")
    except:
        await update.message.reply_text("Invalid coin or error fetching data.")

if __name__ == "__main__":
    bot_app = ApplicationBuilder().token(BOT_TOKEN).build()
    bot_app.add_handler(CommandHandler("crypto", crypto))
    bot_app.run_polling()
    app.run(host="0.0.0.0", port=10000)
