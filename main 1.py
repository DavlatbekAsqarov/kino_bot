import os
import telebot
from telebot import types
from dotenv import load_dotenv

# 1. SOZLAMALAR
load_dotenv()
TOKEN = os.getenv("8684510070:AAE8UShLG3AS2mME3ecbJA148lErJ4d9DMA")
ADMIN_ID = 1419545474  # <--- O'ZINGIZNING ID RAQAMINGIZNI YOZING
KANAL_ID = "@film_box_uz" # <--- TELEGRAM KANALINGIZ
INSTA_LINK = "https://www.instagram.com/filmbox.uz?igsh=ODUzd3JxMGJqaTZ0" # <--- INSTAGRAM LINK

bot = telebot.TeleBot(TOKEN)

# --- 2. KINO BAZASI ---
# "kod": [message_id, "Nomi", "Hajmi", "Reyting"]
KINOLAR = {
    "1": [14, "Sirli qit'a", "686.8 Mb", "4.2"],
    "2": [15, "Avatar 2", "1.2 Gb", "4.8"],
users = set() # Foydalanuvchilar sonini hisoblash uchun

# --- FUNKSIYALAR ---

def is_subscribed(user_id):
    """Telegram kanalga obunani tekshirish"""
    try:
        status = bot.get_chat_member(KANAL_ID, user_id).status
        return status in ['creator', 'administrator', 'member']
    except:
        return True # Xato bo'lsa bot to'xtab qolmasligi uchun

def sub_markup():
    """Majburiy obuna tugmalari"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("1️⃣ Telegram Kanalimiz", url=f"https://t.me/{KANAL_ID.replace('@', '')}"),
        types.InlineKeyboardButton("2️⃣ Instagram Profilimiz", url=INSTA_LINK),
        types.InlineKeyboardButton("✅ Tekshirish", callback_data="check_sub")
    )
    return markup

def main_menu():
    """Asosiy menyu"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔍 Kino qidirish", "📊 Statistika")
    markup.add("👨‍💻 Admin bilan aloqa")
    return markup

# --- HANDLERLAR ---

@bot.message_handler(commands=['start'])
def start(message):
    users.add(message.from_user.id)
    if is_subscribed(message.from_user.id):
        bot.send_message(
            message.chat.id, 
            f"Salom {message.from_user.first_name}! Kino kodini yuboring:", 
            reply_markup=main_menu()
        )
    else:
        bot.send_message(
            message.chat.id, 
            "🛑 **Botdan foydalanish uchun quyidagilarga obuna bo'lishingiz shart!**", 
            reply_markup=sub_markup(),
            parse_mode="Markdown"
        )

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_status(call):
    if is_subscribed(call.from_user.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "✅ Tabriklaymiz! Endi kino kodini yuborishingiz mumkin.", reply_markup=main_menu())
    else:
        bot.answer_callback_query(call.id, "❌ Siz hali obuna bo'lmadingiz!", show_alert=True)
        # Siz aytgandek, yana qaytadan yo'naltirish:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(
            call.message.chat.id, 
            "⚠️ **Shartlar bajarilmadi!**\nIltimos, obuna bo'lib so'ng 'Tekshirish'ni bosing.", 
            reply_markup=sub_markup(),
            parse_mode="Markdown"
        )

# --- KINO QIDIRISH ---

@bot.message_handler(func=lambda message: not message.text.startswith('/'))
def handle_text(message):
    # Har safar obunani tekshirish
    if not is_subscribed(message.from_user.id):
        return start(message)

    code = message.text
    if code in movies:
        m = movies[code]
        btn = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("📽 Ko'rish", url=m['link']))
        bot.send_message(message.chat.id, f"🎬 **Kino:** {m['nom']}\n🆔 **Kod:** {code}", reply_markup=btn, parse_mode="Markdown")
    elif code == "🔍 Kino qidirish":
        bot.send_message(message.chat.id, "Kino kodini kiriting:")
    elif code == "📊 Statistika":
        bot.send_message(message.chat.id, f"📊 Bazada: {len(movies)} ta kino bor.\n👥 Foydalanuvchilar: {len(users)} ta")
    else:
        bot.send_message(message.chat.id, "❌ Bunday kodli kino topilmadi.")

# --- ADMIN PANEL ---

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id == ADMIN_ID:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("➕ Kino qo'shish", "📢 Reklama yuborish", "🏠 Chiqish")
        bot.send_message(message.chat.id, "Admin paneliga xush kelibsiz!", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "➕ Kino qo'shish")
def add_movie_start(message):
    if message.from_user.id == ADMIN_ID:
        msg = bot.send_message(message.chat.id, "Format: `kod|nomi|link` \n(Masalan: `105|Forsaj|https://..`)")
        bot.register_next_step_handler(msg, add_movie_save)

def add_movie_save(message):
    try:
        c, n, l = message.text.split('|')
        movies[c] = {"nom": n, "link": l}
        bot.send_message(message.chat.id, f"✅ Qo'shildi: {n}")
    except:
        bot.send_message(message.chat.id, "❌ Xato! Qayta urinib ko'ring.")

@bot.message_handler(func=lambda message: message.text == "📢 Reklama yuborish")
def send_ad_start(message):
    if message.from_user.id == ADMIN_ID:
        msg = bot.send_message(message.chat.id, "Reklama xabarini yuboring (matn):")
        bot.register_next_step_handler(msg, send_ad_all)

def send_ad_all(message):
    count = 0
    for user in users:
        try:
            bot.send_message(user, message.text)
            count += 1
        except:
            pass
    bot.send_message(ADMIN_ID, f"✅ Reklama {count} ta odamga yetib bordi.")

if __name__ == "__main__":
    bot.infinity_polling()