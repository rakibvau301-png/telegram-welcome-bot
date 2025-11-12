from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError, Forbidden, BadRequest
from flask import Flask
from threading import Thread
import asyncio
import os
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(_name_)

TOKEN = os.getenv("8000576765:AAFLpb1YTwVTDM_YAbvOdpSXQCc_Z7P50FQ")

app = Flask('')

@app.route('/')
def home():
    return "✅ Bot is running 24/7!"

def run():
    app.run(host='0.0.0.0', port=5000)

def keep_alive():
    t = Thread(target=run)
    t.start()

async def welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.new_chat_members:
        logger.warning("Received update without message or new_chat_members")
        return
    
    for member in update.message.new_chat_members:
        try:
            mention = f'<a href="tg://user?id={member.id}">{member.first_name}</a>'
            msg = (
                f"🌸 আসসালামু আলাইকুম 🌸\n\n"
                f"{mention} 💫 🎯 আপনাকে আমাদের গ্রুপে আন্তরিক স্বাগতম 😍\n\n"
                f"এখান থেকে পাবেন:\n"
                f"⚡ আপডেট, সহায়তা ও দরকারি তথ্য\n"
                f"📌 গ্রুপটি পিন করুন\n\n"
                f"🌟 একসাথে শিখি ও এগিয়ে চলি! 🚀\n"
                f"🔔 সব আপডেট পেতে চ্যানেলে যোগ দিন 👇"
            )
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Join Channel", url="https://t.me/CardArenaOfficial")]
            ])
            
            sent_msg = await update.message.reply_html(msg, reply_markup=keyboard)
            logger.info(f"Welcome message sent to {member.first_name} (ID: {member.id})")
            
            await asyncio.sleep(60)
            
            try:
                await context.bot.delete_message(
                    chat_id=update.effective_chat.id, 
                    message_id=sent_msg.message_id
                )
                logger.info(f"Deleted welcome message for {member.first_name}")
            except Forbidden:
                logger.warning(f"Cannot delete message - bot lacks admin rights in chat {update.effective_chat.id}")
            except BadRequest as e:
                logger.warning(f"Cannot delete message - it may have been already removed: {e}")
            except TelegramError as e:
                logger.error(f"Telegram error while deleting message: {e}")
                
        except TelegramError as e:
            logger.error(f"Failed to send welcome message to {member.first_name}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in welcome_message: {e}", exc_info=True)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Exception while handling an update: {context.error}", exc_info=context.error)

def main():
    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set!")
    
    keep_alive()
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_message))
    app_bot.add_error_handler(error_handler)
    
    logger.info("Bot started successfully! Waiting for new members...")
    app_bot.run_polling()

if _name_ == "_main_":
    main()
