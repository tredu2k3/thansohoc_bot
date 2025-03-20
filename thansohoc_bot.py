from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
import os

# Lấy Token từ biến môi trường Railway
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("🚨 Chưa cấu hình TELEGRAM_BOT_TOKEN!")

# Hàm khởi động bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("🔮 Chào mừng bạn đến với Bot Thần Số Học!\n"
                              "📌 Gõ /help để biết cách sử dụng.")

# Hàm trợ giúp
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("📖 Cách sử dụng bot:\n"
                              "🔹 /number [Họ Tên] [Ngày-Tháng-Năm]\n"
                              "Ví dụ: /number Nguyễn Văn A 01-01-1990")

# Hàm xử lý yêu cầu thần số học
def get_numerology(update: Update, context: CallbackContext) -> None:
    try:
        args = context.args
        if len(args) < 2:
            update.message.reply_text("⚠️ Vui lòng nhập đúng định dạng: /number [Họ Tên] [Ngày-Tháng-Năm]")
            return

        name = " ".join(args[:-1])  # Lấy họ tên
        date = args[-1]  # Lấy ngày tháng năm

        # Gọi API thần số học
        api_url = f"https://esgoo.net/api-tsh/{name}/{date}.htm"
        response = requests.get(api_url)
        data = response.json()

        # Kiểm tra lỗi từ API
        if data.get("error") == 1:
            update.message.reply_text(f"❌ {data.get('error_text')}")
        else:
            update.message.reply_text(f"🔮 **Kết quả Thần Số Học:**\n{data.get('data')}")

    except Exception as e:
        update.message.reply_text("⚠️ Có lỗi xảy ra, vui lòng thử lại sau!")
        print(e)

# Cấu hình bot
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("number", get_numerology))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

