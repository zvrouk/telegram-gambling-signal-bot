import asyncio
import os
import random
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Setup Logging
logging.basicConfig(level=logging.INFO)

# Config / Environment Variables
BOT_TOKEN = os.getenv("BOT_TOKEN", "8752011014:AAFD5AkO84Tqy75FbCXwPdsvOLiNJ5hjOiQ")
REF_URL = os.getenv("REF_URL", "https://lkyr.cc/6335d9")
CHANNEL_URL = os.getenv("CHANNEL_URL", "https://t.me/+WF5cBxNLYy0wMGU0")
CHANNEL_ID = os.getenv("CHANNEL_ID", "-1002163714024")
VERIFY_CHANNEL_ID = os.getenv("VERIFY_CHANNEL_ID", "-1004417062544")
SUPP = os.getenv("SUPP", "https://t.me/unrichh")
ADMIN_ID = os.getenv("ADMIN_ID", "6674976941")
PROMO = os.getenv("PROMO", "CARTEL100")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Memory Storage for User Language
user_lang = {}

# Dictionary of Multilingual Texts
TEXTS = {
    "en": {
        "welcome": (
            "🚀 **WELCOME TO EL CARTEL SIGNALS** 🚀\n\n"
            "Your ultimate hub for daily high-accuracy gaming predictions, "
            "maximum 1Win multipliers, and exclusive VIP access.\n\n"
            "🔥 **Use Promo Code:** `{promo}` for a **500% Deposit Bonus!**\n\n"
            "Select an option below to continue:"
        ),
        "mines_title": "💣 **1WIN MINES SIGNAL GENERATED**\n\nAccuracy: **80%**\nGrid Size: **5x5**\n\nReveal the safe tiles on 1Win now!",
        "chicken_title": (
            "🐔 **CHICKEN SUBWAY SIGNAL**\n\n"
            "📍 **Step 1:** Odds ({s1_1}, {s1_2}, {s1_3}) ➡️ **Pick {r1}**\n"
            "📍 **Step 2:** Odds ({s2_1}, {s2_2}, {s2_3}) ➡️ **Pick {r2}**\n"
            "📍 **Step 3:** Odds ({s3_1}, {s3_2}, {s3_3}) ➡️ **Pick {r3}**\n"
            "📍 **Step 4:** Odds ({s4_1}, {s4_2}, {s4_3}) ➡️ **Pick {r4}**\n"
            "📍 **Step 5:** Odds ({s5_1}, {s5_2}, {s5_3}) ➡️ **Cash Out!**\n\n"
            "⚠️ Stick to the exact path for maximum accuracy!"
        ),
        "register_text": (
            "📌 **HOW TO REGISTER & GET 500% BONUS**\n\n"
            "1. Click the link below to open 1Win.\n"
            "2. Fill in your details.\n"
            "3. Use Promo Code: `{promo}`\n"
            "4. Make your deposit and start winning!"
        ),
        "btn_mines": "💣 Mines Signal",
        "btn_chicken": "🐔 Chicken Subway",
        "btn_reg": "🔗 Register Account",
        "btn_verify": "✅ Verify Access",
        "btn_supp": "💬 Support",
        "btn_lang": "🌐 Switch Language"
    },
    "sw": {
        "welcome": (
            "🚀 **KARIBU EL CARTEL SIGNALS** 🚀\n\n"
            "Kituo chako kuu cha utabiri wa michezo wenye usahihi wa juu, "
            "vigezo vya juu vya 1Win, na ufikiaji wa kipekee wa VIP.\n\n"
            "🔥 **Tumia Promo Code:** `{promo}` kupata **Bonus ya 500%!**\n\n"
            "Chagua chaguo hapa chini kuendelea:"
        ),
        "mines_title": "💣 **ISHARA YA 1WIN MINES**\n\nUsahihi: **80%**\nUkubwa wa Grid: **5x5**\n\nFungua vigae salama kwenye 1Win sasa!",
        "chicken_title": (
            "🐔 **ISHARA YA CHICKEN SUBWAY**\n\n"
            "📍 **Hatua ya 1:** Odds ({s1_1}, {s1_2}, {s1_3}) ➡️ **Chagua {r1}**\n"
            "📍 **Hatua ya 2:** Odds ({s2_1}, {s2_2}, {s2_3}) ➡️ **Chagua {r2}**\n"
            "📍 **Hatua ya 3:** Odds ({s3_1}, {s3_2}, {s3_3}) ➡️ **Chagua {r3}**\n"
            "📍 **Hatua ya 4:** Odds ({s4_1}, {s4_2}, {s4_3}) ➡️ **Chagua {r4}**\n"
            "📍 **Hatua ya 5:** Odds ({s5_1}, {s5_2}, {s5_3}) ➡️ **Chukua Pesa!**\n\n"
            "⚠️ Fuata njia halisi kwa usahihi wa hali ya juu!"
        ),
        "register_text": (
            "📌 **JINSI YA KUJISAJILI NA KUPATA BONUS YA 500%**\n\n"
            "1. Bofya kiungo hapa chini kufungua 1Win.\n"
            "2. Jaza maelezo yako.\n"
            "3. Tumia Promo Code: `{promo}`\n"
            "4. Weka akiba yako na uanze kushinda!"
        ),
        "btn_mines": "💣 Ishara ya Mines",
        "btn_chicken": "🐔 Chicken Subway",
        "btn_reg": "🔗 Jisajili Akaunti",
        "btn_verify": "✅ Thibitisha Ufikiaji",
        "btn_supp": "💬 Msaada",
        "btn_lang": "🌐 Badilisha Lugha"
    }
}

# Helper: Notify Admin Log Channel
async def notify_admin_log(text: str):
    try:
        await bot.send_message(chat_id=VERIFY_CHANNEL_ID, text=text, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Failed to send log notification to {VERIFY_CHANNEL_ID}: {e}")

# Keyboards
def get_lang_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="set_lang_en"),
         InlineKeyboardButton(text="🇰🇪 Swahili", callback_data="set_lang_sw")]
    ])

def get_main_keyboard(lang="en"):
    t = TEXTS[lang]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["btn_mines"], callback_query_data="game_mines"),
         InlineKeyboardButton(text=t["btn_chicken"], callback_query_data="game_chicken_subway")],
        [InlineKeyboardButton(text=t["btn_reg"], url=REF_URL),
         InlineKeyboardButton(text=t["btn_verify"], url=CHANNEL_URL)],
        [InlineKeyboardButton(text=t["btn_supp"], url=SUPP),
         InlineKeyboardButton(text=t["btn_lang"], callback_query_data="change_language")]
    ])

# Set Bot Commands Menu
async def set_bot_commands():
    commands = [
        types.BotCommand(command="start", description="Start or Restart the Bot"),
        types.BotCommand(command="language", description="Change Language / Badilisha Lugha")
    ]
    await bot.set_my_commands(commands)

# Handlers
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    user = message.from_user
    if user.id not in user_lang:
        await message.answer(
            "🌐 **Select Your Language / Chagua Lugha Yako:**",
            reply_markup=get_lang_keyboard(),
            parse_mode="Markdown"
        )
    else:
        lang = user_lang[user.id]
        t = TEXTS[lang]
        await message.answer(
            t["welcome"].format(promo=PROMO),
            reply_markup=get_main_keyboard(lang),
            parse_mode="Markdown"
        )

@dp.callback_query(F.data.startswith("set_lang_"))
async def set_language_handler(callback: types.CallbackQuery):
    await callback.answer()
    lang = callback.data.split("_")[2]
    user = callback.from_user
    user_lang[user.id] = lang
    t = TEXTS[lang]
    
    await notify_admin_log(f"👤 **New User Set Language:** {user.full_name} (`{user.id}`) ➡️ `{lang.upper()}`")
    await callback.message.edit_text(
        t["welcome"].format(promo=PROMO),
        reply_markup=get_main_keyboard(lang),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "change_language")
async def change_lang_handler(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "🌐 **Select Your Language / Chagua Lugha Yako:**",
        reply_markup=get_lang_keyboard(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "game_mines")
async def mines_handler(callback: types.CallbackQuery):
    await callback.answer()
    user = callback.from_user
    lang = user_lang.get(user.id, "en")
    t = TEXTS[lang]

    # Generate 5x5 Mines Grid (80% Safe Tiles Revealed)
    grid = ["💎" if random.random() < 0.8 else "💣" for _ in range(25)]
    grid_str = "\n".join([" ".join(grid[i:i+5]) for i in range(0, 25, 5)])

    response_text = f"{t['mines_title']}\n\n{grid_str}"
    
    await notify_admin_log(f"💣 **Signal (Mines):** {user.full_name} [`{user.id}`]")
    await callback.message.edit_text(
        response_text,
        parse_mode="Markdown",
        reply_markup=get_main_keyboard(lang)
    )

@dp.callback_query(F.data == "game_chicken_subway")
async def chicken_subway_handler(callback: types.CallbackQuery):
    await callback.answer()
    user = callback.from_user
    lang = user_lang.get(user.id, "en")
    t = TEXTS[lang]

    s1 = [round(random.uniform(1.10, 1.25), 2), round(random.uniform(1.30, 1.50), 2), round(random.uniform(1.60, 2.00), 2)]
    s2 = [round(random.uniform(1.40, 1.80), 2), round(random.uniform(1.90, 2.40), 2), round(random.uniform(2.50, 3.20), 2)]
    s3 = [round(random.uniform(2.20, 2.80), 2), round(random.uniform(3.00, 4.20), 2), round(random.uniform(4.50, 6.00), 2)]
    s4 = [round(random.uniform(3.50, 4.80), 2), round(random.uniform(5.20, 7.00), 2), round(random.uniform(7.50, 10.00), 2)]
    s5 = [round(random.uniform(6.00, 8.50), 2), round(random.uniform(9.00, 12.50), 2), round(random.uniform(13.00, 20.00), 2)]

    trk = "Track" if lang == "en" else "Njia"
    r1 = random.choice([f"{trk} 1 (x{s1[0]})", f"{trk} 2 (x{s1[1]})"])
    r2 = random.choice([f"{trk} 1 (x{s2[0]})", f"{trk} 2 (x{s2[1]})"])
    r3 = random.choice([f"{trk} 1 (x{s3[0]})", f"{trk} 2 (x{s3[1]})"])
    r4 = random.choice([f"{trk} 1 (x{s4[0]})", f"{trk} 2 (x{s4[1]})"])

    response_text = t["chicken_title"].format(
        s1_1=s1[0], s1_2=s1[1], s1_3=s1[2], r1=r1,
        s2_1=s2[0], s2_2=s2[1], s2_3=s2[2], r2=r2,
        s3_1=s3[0], s3_2=s3[1], s3_3=s3[2], r3=r3,
        s4_1=s4[0], s4_2=s4[1], s4_3=s4[2], r4=r4,
        s5_1=s5[0], s5_2=s5[1], s5_3=s5[2]
    )

    await notify_admin_log(f"🐔 **Signal (Chicken Subway):** {user.full_name} [`{user.id}`]")
    await callback.message.edit_text(
        response_text,
        parse_mode="Markdown",
        reply_markup=get_main_keyboard(lang)
    )

@dp.chat_join_request()
async def auto_approve_join_request(chat_join_request: types.ChatJoinRequest):
    try:
        await chat_join_request.approve()
        user = chat_join_request.from_user
        await notify_admin_log(f"⚡ **Auto-Approved Join Request:** {user.full_name} [`{user.id}`]")
    except Exception as e:
        logging.error(f"Failed to approve join request: {e}")

# Dummy Server for Render Web Service Uptime
async def handle_ping(request):
    return web.Response(text="Bot is running smoothly!")

async def start_dummy_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    app.router.add_get("/health", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# Main Entry Point
async def main():
    await set_bot_commands()
    await start_dummy_server()  # Starts the server for Render health checks
    
    try:
        await dp.start_polling(
            bot, 
            allowed_updates=["message", "callback_query", "chat_join_request"]
        )
    finally:
        # Clean up aiohttp client session on shutdown
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())