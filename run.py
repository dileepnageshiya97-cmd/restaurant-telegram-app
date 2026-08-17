import os
import threading
import asyncio
from app import create_app

app = create_app()

def start_bot():
    # Render Dashboard se 'BOT_TOKEN' aur 'WEB_APP_URL' Automatically uthayega
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
    
    print("🤖 Telegram Bot background me start ho gaya hai...")
    bot_app.run_polling(stop_signals=None)

if __name__ == '__main__':
    # Bot ko background thread me start karein
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()
    
    # Render host dynamic PORT provide karta hai
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)