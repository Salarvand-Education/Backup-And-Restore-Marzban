import os
import zipfile
import shutil
import time
import schedule
import logging
from dotenv import load_dotenv
from telegram import Update, InputFile, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

# مسیرهای پوشه‌های marzban
MARZBAN_SRC1 = '/opt/marzban/'
MARZBAN_SRC2 = '/var/lib/marzban/'
MARZBAN_SRC3 = '/var/lib/marzban/xray-core/xray'
BACKUP_DIR = '/tmp'

backup_interval = 1  # فاصله زمانی اولیه بکاپ‌گیری به دقیقه

logging.basicConfig(level=logging.INFO)

def backup_marzban():
    timestamp = time.strftime("%Y%m%d%H%M%S")
    backup_name = f"backup_{timestamp}.zip"
    backup_path = os.path.join(BACKUP_DIR, backup_name)

    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(MARZBAN_SRC1):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start='/')
                zipf.write(file_path, arcname=arcname)
        for root, dirs, files in os.walk(MARZBAN_SRC2):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start='/')
                zipf.write(file_path, arcname=arcname)
        for root, dirs, files in os.walk(MARZBAN_SRC3):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start='/')
                zipf.write(file_path, arcname=arcname)
    
    return backup_path

def restore_marzban(backup_path):
    logging.info(f"Starting restore from {backup_path}")
    if not os.path.exists(backup_path):
        logging.error("Backup file does not exist.")
        return False

    try:
        if os.path.exists(MARZBAN_SRC1):
            shutil.rmtree(MARZBAN_SRC1)
        if os.path.exists(MARZBAN_SRC2):
            shutil.rmtree(MARZBAN_SRC2)
        if os.path.exists(MARZBAN_SRC3):
            shutil.rmtree(MARZBAN_SRC3)
        
        os.makedirs(MARZBAN_SRC1)
        os.makedirs(MARZBAN_SRC2)
        os.makedirs(MARZBAN_SRC3)

        with zipfile.ZipFile(backup_path, 'r') as zipf:
            zipf.extractall('/')

        logging.info("Files extracted successfully. Restarting Marzban...")
        os.system('marzban restart')

        return True
    except Exception as e:
        logging.error(f"Error during restore: {str(e)}")
        return False

def start(update: Update, context) -> None:
    update.message.reply_text('سلام! از دستور /backup برای گرفتن بکاپ و از /restore برای ریستور استفاده کنید.')

def backup_command(update: Update, context) -> None:
    backup_path = backup_marzban()
    with open(backup_path, 'rb') as f:
        update.message.reply_document(document=InputFile(f, filename=os.path.basename(backup_path)))
    os.remove(backup_path)

def restore_command(update: Update, context) -> None:
    update.message.reply_text('لطفا فایل بکاپ را ارسال کنید.')

def handle_document(update: Update, context) -> None:
    document = update.message.document
    file = context.bot.get_file(document.file_id)
    backup_path = os.path.join('/tmp', document.file_name)
    file.download(backup_path)
    
    if restore_marzban(backup_path):
        update.message.reply_text('بکاپ با موفقیت ریستور شد و Marzban ری‌استارت شد!')
    else:
        update.message.reply_text('خطا در ریستور بکاپ یا ری‌استارت Marzban.')
    os.remove(backup_path)

def send_backup(bot: Bot) -> None:
    logging.info("Sending backup...")
    backup_path = backup_marzban()
    with open(backup_path, 'rb') as f:
        bot.send_document(chat_id=ADMIN_CHAT_ID, document=InputFile(f, filename=os.path.basename(backup_path)))
    os.remove(backup_path)
    logging.info("Backup sent.")

def schedule_jobs(bot: Bot):
    schedule.clear()  # حذف همه زمان‌بندی‌های قبلی
    schedule.every(backup_interval).minutes.do(lambda: send_backup(bot))
    logging.info(f"Scheduled backup every {backup_interval} minutes.")

def set_interval(update: Update, context) -> None:
    global backup_interval
    try:
        new_interval = int(context.args[0])
        backup_interval = new_interval
        schedule_jobs(context.bot)  # به‌روزرسانی زمان‌بندی‌ها
        update.message.reply_text(f'فاصله زمانی بکاپ‌گیری به {backup_interval} دقیقه تغییر یافت.')
        logging.info(f"Backup interval set to {backup_interval} minutes.")
    except (IndexError, ValueError):
        update.message.reply_text('لطفاً یک عدد معتبر وارد کنید.')

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

def main() -> None:
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("backup", backup_command))
    dispatcher.add_handler(CommandHandler("restore", restore_command))
    dispatcher.add_handler(CommandHandler("setinterval", set_interval))  # فرمان جدید برای تنظیم فاصله زمانی
    dispatcher.add_handler(MessageHandler(Filters.document, handle_document))

    schedule_jobs(updater.bot)
    
    # اجرای run_schedule به عنوان یک تسک
    import threading
    threading.Thread(target=run_schedule, daemon=True).start()
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
