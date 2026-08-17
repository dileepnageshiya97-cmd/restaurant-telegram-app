import os
import threading
import asyncio
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def start_telegram_bot():
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    WEB_APP_URL = os.environ.get('WEB_APP_URL')

    if not BOT_TOKEN or not WEB_APP_URL:
        print("⚠️ Environment variables (BOT_TOKEN / WEB_APP_URL) missing hain!")
        return

    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
    from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [InlineKeyboardButton("🍽️ Open Restaurant Menu", web_app=WebAppInfo(url=WEB_APP_URL))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Swagat hai! Menu dekhne ke liye niche button par click karein:", reply_markup=reply_markup)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    bot_app = ApplicationBuilder().token(BOT_TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))

    print("🤖 Telegram Bot background me successfully start ho gaya hai!")
    bot_app.run_polling(stop_signals=None)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    # Gunicorn worker start hone par bot ko thread me run karein
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        bot_thread = threading.Thread(target=start_telegram_bot, daemon=True)
        bot_thread.start()

    return app