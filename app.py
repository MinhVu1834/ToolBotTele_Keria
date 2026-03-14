import os
from datetime import datetime

import telebot
from telebot import types
from flask import Flask, request

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))

REG_LINK = "https://vsbets.online"

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
server = Flask(__name__)

user_state = {}
debug_get_id_mode = set()


# ================= DEBUG FILE_ID =================

@bot.message_handler(commands=['getid'])
def enable_getid(message):

    chat_id = message.chat.id
    debug_get_id_mode.add(chat_id)

    bot.send_message(
        chat_id,
        "Gửi ảnh để lấy FILE_ID\n\nTắt bằng /stopgetid"
    )


@bot.message_handler(commands=['stopgetid'])
def stop_getid(message):

    chat_id = message.chat.id
    debug_get_id_mode.discard(chat_id)

    bot.send_message(chat_id, "Đã tắt chế độ lấy FILE_ID")


# ================= START =================

@bot.message_handler(commands=['start'])
def start(message):

    chat_id = message.chat.id

    text = (
        "🎉 Chào mừng anh/chị đến với BOT nhận khuyến mãi tự động của VSBet!\n\n"
        "🎁 Cập nhật khuyến mãi nhanh – hỗ trợ 24/7.\n"
        "👉 Anh/chị đã có tài khoản VSBet chưa?"
    )

    markup = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton(
        "✅ ĐÃ CÓ TÀI KHOẢN",
        callback_data="have_account"
    )

    btn2 = types.InlineKeyboardButton(
        "🆕 ĐĂNG KÝ TÀI KHOẢN MỚI",
        url=REG_LINK
    )

    markup.row(btn1)
    markup.row(btn2)

    bot.send_message(
        chat_id,
        text,
        parse_mode="Markdown",
        reply_markup=markup
    )


# ================= HỎI USERNAME =================

def ask_username(chat_id):

    text = (
        "👤 Anh/chị vui lòng gửi *tên tài khoản VSBet* để bot hỗ trợ kiểm tra nhé.\n\n"
        "📌 Ví dụ:\n"
        "`abc123`"
    )

    bot.send_message(chat_id, text, parse_mode="Markdown")

    user_state[chat_id] = "WAITING_USERNAME"


# ================= MENU KHUYẾN MÃI =================

def show_promo_menu(chat_id):

    text = (
        "🎁 *KHUYẾN MÃI VSBet*\n\n"
        "Chọn khuyến mãi muốn tham gia:"
    )

    markup = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton(
        "🔥 Bảo hiểm cược thể thao",
        callback_data="promo_insurance"
    )

    btn2 = types.InlineKeyboardButton(
        "🎁 Nạp đầu 100%",
        callback_data="promo_100"
    )

    btn3 = types.InlineKeyboardButton(
        "🎁 Nạp đầu 30%",
        callback_data="promo_30"
    )

    btn4 = types.InlineKeyboardButton(
        "🎮 Trải nghiệm 58K",
        callback_data="promo_58"
    )

    markup.row(btn1)
    markup.row(btn2)
    markup.row(btn3)
    markup.row(btn4)

    bot.send_message(
        chat_id,
        text,
        parse_mode="Markdown",
        reply_markup=markup
    )


# ================= NÚT SAU KHUYẾN MÃI =================

def show_after_promo_buttons(chat_id):

    markup = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton(
        "📤 Gửi ảnh chuyển khoản để cộng khuyến mãi",
        callback_data="send_receipt"
    )

    btn2 = types.InlineKeyboardButton(
        "📩 Nhắn tin trực tiếp cho admin",
        url=f"https://t.me/{os.getenv('ADMIN_USERNAME','')}"
    )

    markup.row(btn1)
    markup.row(btn2)

    bot.send_message(
        chat_id,
        "Sau khi chuyển khoản, anh/chị gửi ảnh chuyển khoản để bot cộng khuyến mãi nhé.",
        reply_markup=markup
    )


# ================= CALLBACK =================

@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    chat_id = call.message.chat.id
    data = call.data

    if data == "have_account":
        ask_username(chat_id)

    elif data == "promo_insurance":

        text = (
            "🔥 *BẢO HIỂM CƯỢC THỂ THAO*\n\n"
            "Nếu cược trận đầu bị thua\n"
            "VSBet hoàn lại *100% tiền cược*\n\n"
            "Cược 1 vòng có thể rút tiền."
        )

        bot.send_photo(
            chat_id,
            "AgACAgUAAxkBAAMPabRFMV_jUcW8H6nbpIboTdQDrc4AAuYMaxuO3KFVz1ekH9nh6aIBAAMCAAN5AAM6BA",
            caption=text,
            parse_mode="Markdown"
        )

        show_after_promo_buttons(chat_id)

    elif data == "promo_100":

        text = (
            "🎁 *KHUYẾN MÃI NẠP 100%*\n\n"
            "Nạp bao nhiêu tặng bấy nhiêu\n\n"
            "Ví dụ:\n"
            "1M → 2M\n"
            "5M → 10M\n\n"
            "Yêu cầu 15 vòng cược"
        )

        bot.send_photo(
            chat_id,
            "AgACAgUAAxkBAAMTabRFPSjOLUa8fJBj1sYXbfO_PkYAAugMaxuO3KFVxujV5sDoYdABAAMCAAN4AAM6BA",
            caption=text,
            parse_mode="Markdown"
        )

        show_after_promo_buttons(chat_id)

    elif data == "promo_30":

        text = (
            "🎁 *KHUYẾN MÃI NẠP 30%*\n\n"
            "100K - 2M → thưởng 30%\n"
            "2M - 50M → thưởng 20%\n\n"
            "Yêu cầu 5 vòng cược"
        )

        bot.send_photo(
            chat_id,
            "AgACAgUAAxkBAAMRabRFOD_zgPryawY6oYOJjfh_WfEAAucMaxuO3KFV3hRrVh-Pyq4BAAMCAAN5AAM6BA",
            caption=text,
            parse_mode="Markdown"
        )

        show_after_promo_buttons(chat_id)

    elif data == "promo_58":

        text = (
            "🎮 *TRẢI NGHIỆM 58K*\n\n"
            "Tặng 58K miễn phí\n\n"
            "Đạt 358K có thể rút\n"
            "Không cần vòng cược"
        )

        bot.send_message(chat_id, text, parse_mode="Markdown")

        show_after_promo_buttons(chat_id)

    elif data == "send_receipt":

        bot.send_message(
            chat_id,
            "Anh/chị chuyển khoản xong gửi *ảnh chuyển khoản* để em cộng khuyến mãi nhé.",
            parse_mode="Markdown"
        )

        user_state[chat_id] = "WAITING_RECEIPT"


# ================= TEXT =================

@bot.message_handler(content_types=['text'])
def handle_text(message):

    chat_id = message.chat.id
    text = message.text.strip()

    if user_state.get(chat_id) == "WAITING_USERNAME":

        username = text
        tg_username = f"@{message.from_user.username}" if message.from_user.username else "Không có"

        admin_text = (
            "👤 KHÁCH GỬI USERNAME\n\n"
            f"👤 Telegram: {tg_username}\n"
            f"🎮 Username: {username}\n"
            f"🆔 ChatID: {chat_id}"
        )

        if ADMIN_CHAT_ID:
            bot.send_message(ADMIN_CHAT_ID, admin_text)

        show_promo_menu(chat_id)


# ================= MEDIA =================

@bot.message_handler(content_types=['photo', 'document'])
def handle_media(message):

    chat_id = message.chat.id

    if user_state.get(chat_id) != "WAITING_RECEIPT":
        return

    if message.photo:
        file_id = message.photo[-1].file_id
    else:
        file_id = message.document.file_id

    time_str = datetime.now().strftime("%H:%M %d/%m/%Y")

    tg_username = f"@{message.from_user.username}" if message.from_user.username else "Không có"

    bot.send_photo(
        ADMIN_CHAT_ID,
        file_id,
        caption=(
            "💰 KHÁCH GỬI CHUYỂN KHOẢN\n\n"
            f"👤 Telegram: {tg_username}\n"
            f"🆔 ChatID: {chat_id}\n"
            f"⏰ Thời gian: {time_str}"
        )
    )

    bot.send_message(
        chat_id,
        "✅ Đã nhận ảnh chuyển khoản\nCSKH đang xử lý cho mình."
    )

    user_state[chat_id] = None


# ================= WEBHOOK =================

@server.route('/webhook', methods=['POST'])
def webhook():

    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)

    bot.process_new_updates([update])

    return "OK", 200


@server.route('/')
def home():
    return "VSBet Bot Running"


if __name__ == "__main__":

    bot.remove_webhook()

    bot.set_webhook(
        url=os.getenv("WEBHOOK_URL")
    )

    server.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000))
    )
