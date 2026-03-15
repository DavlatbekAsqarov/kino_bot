import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

# --- 1. SOZLAMALAR ---
API_TOKEN = '8684510070:AAEwhbTztOKG1OgmQGIHBWafVQnVImGdfhU' 
BAZA_KANAL_ID = -1001439899296 

# --- 2. KINOLAR BAZASI ---
KINOLAR = {
    "1": {"nomi": "Sirli qit'a", "sifat": "HD", "davlat": "Noma'lum", "janr": "#Sarguzasht", "yil": "Noma'lum", "msg_id": 14, "file_id": ""},
    "2": {"nomi": "Begona odam va tuman 1976", "sifat": "720p HD", "davlat": "Eron", "janr": "#Drama #Detektiv", "yil": "1976", "msg_id": 21, "file_id": ""},
    "3": {"nomi": "Arvohlar Kemasi", "sifat": "720p HD", "davlat": "Buyuk Britaniya", "janr": "#Ujas #Drama", "yil": "2023", "msg_id": 25, "file_id": ""},
    "4": {"nomi": "Jazolovchi", "sifat": "720p HD", "davlat": "AQSH, Germaniya", "janr": "#Jangari #Triller #Drama #Kriminal", "yil": "2004", "msg_id": 27, "file_id": ""},
    "5": {"nomi": "Kolumbiana", "sifat": "720p HD", "davlat": "Fransiya, Meksika", "janr": "#Jangari #Triller #Drama", "yil": "2011", "msg_id": 29, "file_id": ""},
    "6": {"nomi": "Revolver", "sifat": "720p HD", "davlat": "Buyuk Britaniya, Fransiya", "janr": "#Jangari #Triller #Drama #Kriminal #Detektiv", "yil": "2005", "msg_id": 31, "file_id": ""},
    "7": {"nomi": "Tuyg'u", "sifat": "720p HD", "davlat": "Italiya", "janr": "#Urush #Drama #Melodrama", "yil": "1954", "msg_id": 33, "file_id": ""},
    "8": {"nomi": "G'alati Tomas Odd", "sifat": "720p HD", "davlat": "AQSH, Buyuk Britaniya", "janr": "#Ujas #Triller #Komediya", "yil": "2013", "msg_id": 35, "file_id": ""},
    "9": {"nomi": "13 ta o'q", "sifat": "720p HD", "davlat": "AQSH", "janr": "#Triller #Drama #Kriminal", "yil": "2009", "msg_id": 37, "file_id": ""},
    "10": {"nomi": "Fortuna operatsiyasi", "sifat": "720p HD", "davlat": "AQSH, Xitoy", "janr": " #Jangari #Triller", "yil": "2022", "msg_id": 40, "file_id": ""},
    "11": {"nomi": "Liger", "yil": "2022", "davlat": "Hindiston", "janr": "#Jangari #Drama #Sport", "sifat": "720p HD", "msg_id": 42, "file_id": ""},
    "12": {"nomi": "Odamxo'rlar", "yil": "2021", "davlat": "Fransiya", "janr": "#Ujas #Komediya", "sifat": "720p HD", "msg_id": 44, "file_id": ""},
    "13": {"nomi": "Jonim seni yohud egizaklar", "yil": "2004", "davlat": "O'zbekiston", "janr": "#Melodrama #Komediya", "sifat": "720p HD", "msg_id": 46, "file_id": ""},
    "14": {"nomi": "Osvensim Chempioni", "yil": "2020", "davlat": "Polsha", "janr": "#Biografiya #Urush #Tarixiy", "sifat": "720p HD", "msg_id": 48, "file_id": ""},
    "15": {"nomi": "Jangari futbol", "yil": "2001", "davlat": "GongKong, Xitoy", "janr": "#Jangari #Komediya", "sifat": "720p HD", "msg_id": 50, "file_id": ""},
    "16": {"nomi": "Tinchlikparvar", "yil": "1997", "davlat": "AQSH", "janr": "#Jangari #Triller", "sifat": "720p HD", "msg_id": 52, "file_id": ""},
    "17": {"nomi": "Firibgar", "yil": "1993", "davlat": "Hindiston", "janr": "#Triller #Kriminal", "sifat": "720p HD", "msg_id": 54, "file_id": ""},
    "18": {"nomi": "Qo'ng'iroq", "yil": "2002", "davlat": "AQSH, Yaponiya", "janr": "#Ujas", "sifat": "720p HD", "msg_id": 56, "file_id": ""},
    "19": {"nomi": "Kelajakka qaytib 1", "yil": "1985", "davlat": "AQSH", "janr": "#Fantastika #Sarguzasht", "sifat": "720p HD", "msg_id": 58, "file_id": ""},
    "20": {"nomi": "Kelajakka qaytib 2", "yil": "1989", "davlat": "AQSH", "janr": "#Fantastika #Oilaviy", "sifat": "720p HD", "msg_id": 61, "file_id": ""},
    "21": {"nomi": "Kelajakka qaytib 3", "yil": "1990", "davlat": "AQSH", "janr": "#Vestern #Fantastika", "sifat": "720p HD", "msg_id": 62, "file_id": ""},
    "22": {"nomi": "Arvoh qizning hikoyasi", "yil": "2014", "davlat": "Janubiy Koreya", "janr": "#Ujas #Triller", "sifat": "720p HD", "msg_id": 64, "file_id": ""},
    "23": {"nomi": "Astronavt Farmer", "yil": "2006", "davlat": "AQSH", "janr": "#Drama #Fantastika", "sifat": "720p HD", "msg_id": 67, "file_id": ""},
    "24": {"nomi": "Manfur kimsalar", "yil": "2009", "davlat": "Germaniya, AQSH", "janr": "#Harbiy #Drama", "sifat": "720p HD", "msg_id": 68, "file_id": ""},
    "25": {"nomi": "O'lja ishtiyoqi", "yil": "2024", "davlat": "Fransiya, Belgiya", "janr": "#Triller #Komediya", "sifat": "720p HD", "msg_id": 69, "file_id": ""},
    "26": {"nomi": "Uidji Veronika lanati", "yil": "2017", "davlat": "Ispaniya", "janr": "#Ujas", "sifat": "720p HD", "msg_id": 70, "file_id": ""},
    "27": {"nomi": "Dahshatli masxaraboz 1", "yil": "2016", "davlat": "AQSH", "janr": "#Ujas", "sifat": "720p HD", "msg_id": 71, "file_id": ""},
    "28": {"nomi": "Dahshatli masxaraboz 2", "yil": "2022", "davlat": "AQSH", "janr": "#Ujas", "sifat": "720p HD", "msg_id": 72, "file_id": ""},
    "29": {"nomi": "La'natlangan uy", "yil": "2018", "davlat": "AQSH", "janr": "#Ujas #Drama", "sifat": "720p HD", "msg_id": 73, "file_id": ""},
    "30": {"nomi": "Qoyalarning ko'zlari bor 1", "yil": "2006", "davlat": "AQSH", "janr": "#Ujas #Triller", "sifat": "720p HD", "msg_id": 74, "file_id": ""},
    "31": {"nomi": "Qoyalarning ko'zlari bor 2", "yil": "2007", "davlat": "AQSH", "janr": "#Ujas #Triller", "sifat": "720p HD", "msg_id": 75, "file_id": ""}
}

bot = Bot(token=API_TOKEN.strip())
dp = Dispatcher()

# Render veb-serveri
async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("👋 Salom, Hazrati oliylari!\nKino kodini yuboring.")

@dp.message()
async def handle_message(message: types.Message):
    if message.video:
        file_id = message.video.file_id
        return await message.answer(f"🎞 File ID:\n`{file_id}`", parse_mode="Markdown")

    kod = message.text.strip()
    
    if kod in KINOLAR:
        k = KINOLAR[kod]
        txt = (
            f"🎬 Nomi: {k['nomi']}\n"
            f"💽 Sifati: {k.get('sifat', '720p HD')}\n"
            f"🌎 Davlati: {k.get('davlat', 'Noma\'lum')}\n"
            f"🎭 Janri: {k.get('janr', 'Noma\'lum')}\n"
            f"🇺🇿 Tili: O'zbek tilida\n"
            f"📅 Yili: {k.get('yil', 'Noma\'lum')} yil\n\n"
            f"🍿 @filmboxuzkanal" 
        )

        try:
            await bot.copy_message(chat_id=message.chat.id, from_chat_id=BAZA_KANAL_ID, message_id=k['msg_id'], caption=txt, parse_mode="Markdown")
        except Exception as e:
            await message.answer(f"❌ Xato: {e}")
    elif not kod.startswith('/'):
        await message.answer("😔 Kino topilmadi.")

async def main():
    asyncio.create_task(start_web_server())
    await bot.delete_webhook(drop_pending_updates=True)
    print("--- 🚀 BOT ISHLAYABDI ---")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
