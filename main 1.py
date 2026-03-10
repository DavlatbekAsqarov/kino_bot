import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# --- 1. SOZLAMALAR ---
TOKEN = "8684510070:AAE8UShLG3AS2mME3ecbJA148lErJ4d9DMA"
ADMIN_ID = 1419545474              # O'zingizning Telegram ID-ingizni yozing (@userinfobot beradi)
OCHIQ_KANAL = "@film_box_uz"      # Majburiy obuna kanali
YAPIQ_BAZA_ID = -1001439899296     # Kinolar turgan yopiq kanal ID-si
INSTAGRAM_LINK = "https://www.instagram.com/filmbox.uz?igsh=ODUzd3JxMGJqaTZ0"

# Foydalanuvchilar bazasi (Oddiy ro'yxat, bot o'chib yonsa tozalanadi)
# Doimiy baza uchun SQLite ishlatsa bo'ladi, lekin hozircha shu ham yetadi
USERS = set()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- 2. KINO BAZASI ---
# "kod": [message_id, "Nomi", "Hajmi", "Reyting"]
KINOLAR = {
    "1": [14, "The Convert", "686.8 Mb", "4.2"],
    "2": [15, "Avatar 2", "1.2 Gb", "4.8"],
}

# --- 3. YORDAMCHI FUNKSIYALAR ---
async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(chat_id=OCHIQ_KANAL, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"Obuna xatosi: {e}")
        return False

# --- 4. START BUYRUQ ---
@dp.message(Command("start"))
async def start_command(message: types.Message):
    USERS.add(message.from_user.id) # Foydalanuvchini bazaga qo'shish
    
    if await check_sub(message.from_user.id):
        await message.answer(
            f"🌟 **Xush kelibsiz, {message.from_user.first_name}!**\n\n"
            "Kino kodini yuboring va tomoshadan bahra oling!"
        )
    else:
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(text="1️⃣ Telegram Kanal", url="https://t.me/film_box_uz"))
        builder.row(types.InlineKeyboardButton(text="2️⃣ Instagram Sahifa", url=INSTAGRAM_LINK))
        builder.row(types.InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="check_all"))
        
        await message.answer(
            "🛑 **To'xtang!** Botdan foydalanish uchun quyidagi sahifalarga obuna bo'lishingiz shart:",
            reply_markup=builder.as_markup(),
            parse_mode="Markdown"
        )

# --- 5. ADMIN PANEL (FAQAT SIZ UCHUN) ---
@dp.message(Command("admin"), F.from_user.id == ADMIN_ID)
async def admin_panel(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="📊 Statistika", callback_data="stat"))
    builder.row(types.InlineKeyboardButton(text="📢 Reklama yuborish", callback_data="send_ads"))
    
    await message.answer("🛠 **Admin Panelga xush kelibsiz!**", reply_markup=builder.as_markup())

# --- 6. KINO YUBORISH MANTIQI ---
@dp.message(F.text)
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    kod = message.text.strip()

    if not await check_sub(user_id):
        return await start_command(message)

    if kod in KINOLAR:
        msg_id, nomi, hajmi, reyting = KINOLAR[kod]
        try:
            await bot.copy_message(
                chat_id=message.chat.id,
                from_chat_id=YAPIQ_BAZA_ID,
                message_id=msg_id,
                caption=f"🎬 **Nomi:** {nomi}\n📂 **Hajmi:** {hajmi}\n🌟 **Reyting:** {reyting}\n\n🎥 @film_box_uz",
                parse_mode="Markdown"
            )
        except Exception as e:
            await message.answer(f"⚠️ Xatolik: {e}")
            await bot.send_message(ADMIN_ID, f"❌ Xato! Kod: {kod}, Sabab: {e}")
    elif not kod.startswith('/'):
        await message.answer("😔 Bunday kodli kino topilmadi. Iltimos, kodni to'g'ri yozganingizni tekshiring.")

# --- 7. CALLBACKLAR (TUGMALAR) ---
@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "check_all":
        if await check_sub(callback.from_user.id):
            await callback.message.edit_text("✅ Rahmat! Endi kino kodini yubora olasiz.")
        else:
            await callback.answer("❌ Obuna bo'lmadingiz!", show_alert=True)
            
    elif callback.data == "stat" and callback.from_user.id == ADMIN_ID:
        await callback.message.answer(f"👥 Bot foydalanuvchilari soni: {len(USERS)} ta")
        
    elif callback.data == "send_ads" and callback.from_user.id == ADMIN_ID:
        await callback.message.answer("Reklama yuborish uchun hozircha kodni biroz mukammallashtirish kerak. (Reply orqali yuborish funksiyasi)")

# --- 8. ISHGA TUSHIRISH ---
async def main():
    print("🚀 Premium Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())