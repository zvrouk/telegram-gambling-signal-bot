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
BOT_TOKEN = os.getenv("BOT_TOKEN")
REF_URL = os.getenv("REF_URL", "https://lkrp.cc/c66085")
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
        "select_traps": "🎮 **SELECT NUMBER OF TRAPS:**\n\nChoose how many traps are set in your 1Win Mines session:",
        "mines_title": (
            "💣 **1WIN MINES SIGNAL GENERATED**\n\n"
            "📊 **Grid Size:** 5x5\n"
            "⚠️ **Traps Selected:** {traps}\n"
            "👁️ **Traps Revealed:** {traps_revealed}\n"
            "🟦 **Hidden Tiles:** {unrevealed}\n\n"
            "Reveal the safe 💎 tiles on 1Win now!"
        ),
        "chicken_title": (
            "🐔 **CHICKEN SUBWAY SIGNAL** 🏃‍♂️💨\n\n"
            "📍 **Step 1:** {s1}\n"
            "📍 **Step 2:** {s2}\n"
            "📍 **Step 3:** {s3}\n"
            "📍 **Step 4:** {s4}\n"
            "📍 **Step 5:** {s5}\n"
            "📍 **Step 6:** {s6}\n"
            "📍 **Step 7:** {s7}\n"
            "📍 **Step 8:** {s8}\n"
            "📍 **Step 9:** {s9}\n"
            "📍 **Step 10:** {s10} 💰\n\n"
            "⚠️ Stick to the exact path for maximum accuracy!"
        ),
        "not_member": (
            "⚠️ **VIP CHANNEL VERIFICATION REQUIRED**\n\n"
            "To access signals, you must join our official Telegram channel first.\n"
            "Click below to request access, then tap **✅ Verify Access**!"
        ),
        "reg_menu": (
            "📝 **1WIN REGISTRATION & PROMO CODE**\n\n"
            "🎁 Use Promo Code: `{promo}` to claim your **500% Deposit Bonus**!\n\n"
            "Choose an option below to register or watch the guide:"
        ),
        "reg_tutorial": (
            "📖 **HOW TO REGISTER & ACTIVATE BONUS**\n\n"
            "1️⃣ Click the **🌐 Official 1Win Link** below.\n"
            "2️⃣ Click on **Registration** on the top right.\n"
            "3️⃣ Fill in your phone number, email, and password.\n"
            "4️⃣ Tap **'Add Promo Code'** and enter: `{promo}`\n"
            "5️⃣ Complete registration and make your first deposit to instantly get your **500% Bonus**! 💰"
        ),
        "btn_mines": "💣 Mines Signal",
        "btn_chicken": "🐔 Chicken Subway",
        "btn_reg": "🔗 Register Account",
        "btn_verify": "✅ Verify Access",
        "btn_supp": "💬 Support",
        "btn_lang": "🌐 Switch Language",
        "btn_reg_link": "🌐 Official 1Win Link",
        "btn_tutorial": "📚 How to Register & Use Promo Code",
        "btn_back": "🔙 Back to Main Menu"
    },
    "sw": {
        "welcome": (
            "🚀 **KARIBU EL CARTEL SIGNALS** 🚀\n\n"
            "Kituo chako kuu cha utabiri wa michezo wenye usahihi wa juu, "
            "vigezo vya juu vya 1Win, na ufikiaji wa kipekee wa VIP.\n\n"
            "🔥 **Tumia Promo Code:** `{promo}` kupata **Bonus ya 500%!**\n\n"
            "Chagua chaguo hapa chini kuendelea:"
        ),
        "select_traps": "🎮 **CHAGUA IDADI YA TRAPS:**\n\nChagua idadi ya traps zilizowekwa kwenye mchezo wako wa 1Win Mines:",
        "mines_title": (
            "💣 **ISHARA YA 1WIN MINES**\n\n"
            "📊 **Ukubwa wa Grid:** 5x5\n"
            "⚠️ **Traps Zilizochaguliwa:** {traps}\n"
            "👁️ **Traps Zilizofunguliwa:** {traps_revealed}\n"
            "🟦 **Vigae Vilivyofichwa:** {unrevealed}\n\n"
            "Fungua vigae salama vya 💎 kwenye 1Win sasa!"
        ),
        "chicken_title": (
            "🐔 **ISHARA YA CHICKEN SUBWAY** 🏃‍♂️💨\n\n"
            "📍 **Hatua ya 1:** {s1}\n"
            "📍 **Hatua ya 2:** {s2}\n"
            "📍 **Hatua ya 3:** {s3}\n"
            "📍 **Hatua ya 4:** {s4}\n"
            "📍 **Hatua ya 5:** {s5}\n"
            "📍 **Hatua ya 6:** {s6}\n"
            "📍 **Hatua ya 7:** {s7}\n"
            "📍 **Hatua ya 8:** {s8}\n"
            "📍 **Hatua ya 9:** {s9}\n"
            "📍 **Hatua ya 10:** {s10} 💰\n\n"
            "⚠️ Fuata njia halisi kwa usahihi wa hali ya juu!"
        ),
        "not_member": (
            "⚠️ **UTHIBITISHO WA CHANNEL YA VIP UNAHITAJIKA**\n\n"
            "Ili kupata ishara, lazima ujiunge na chaneli yetu rasmi ya Telegram kwanza.\n"
            "Bofya hapa chini kuomba kujiunga, kisha ubonyeze **✅ Thibitisha Ufikiaji**!"
        ),
        "reg_menu": (
            "📝 **USAJILI WA 1WIN NA PROMO CODE**\n\n"
            "🎁 Tumia Promo Code: `{promo}` kupata **Bonus ya 500%** ya amana!\n\n"
            "Chagua chaguo hapa chini kujisajili au kusoma mwongozo:"
        ),
        "reg_tutorial": (
            "📖 **JINSI YA KUJISAJILI NA KUTUMIA BONUS**\n\n"
            "1️⃣ Bofya **🌐 Link Rasmi ya 1Win** hapo chini.\n"
            "2️⃣ Bofya **Usajili (Registration)** juu kulia.\n"
            "3️⃣ Weka namba yako ya simu, barua pepe, na neno la siri.\n"
            "4️⃣ Bofya **'Ongeza Promo Code'** na uweke: `{promo}`\n"
            "5️⃣ Kumaliza usajili na uweke amana yako ya kwanza ili kupata **Bonus ya 500%** papo hapo! 💰"
        ),
        "btn_mines": "💣 Ishara ya Mines",
        "btn_chicken": "🐔 Chicken Subway",
        "btn_reg": "🔗 Jisajili Akaunti",
        "btn_verify": "✅ Thibitisha Ufikiaji",
        "btn_supp": "💬 Msaada",
        "btn_lang": "🌐 Badilisha Lugha",
        "btn_reg_link": "🌐 Link Rasmi ya 1Win",
        "btn_tutorial": "📚 Jinsi ya Kujisajili & Kutumia Promo Code",
        "btn_back": "🔙 Rudi Menu Kuu"
    }
}

# Helper Function: Escape Special Markdown Characters
def escape_md(text: str) -> str:
    if not text:
        return ""
    for char in ["_", "*", "`", "["]:
        text = text.replace(char, f"\\{char}")
    return text

# Safe Admin Log Notification
async def notify_admin_log(text: str):
    if not VERIFY_CHANNEL_ID:
        return
    try:
        await bot.send_message(chat_id=VERIFY_CHANNEL_ID, text=text, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Failed to send log notification to {VERIFY_CHANNEL_ID}: {e}")

# Helper Function: Check Channel Membership
async def check_channel_member(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ["creator", "administrator", "member"]
    except Exception as e:
        logging.error(f"Error checking channel membership for {user_id}: {e}")
        return False

# Keyboards
def get_lang_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="set_lang_en"),
         InlineKeyboardButton(text="🇰🇪 Swahili", callback_data="set_lang_sw")]
    ])

def get_main_keyboard(lang="en"):
    t = TEXTS[lang]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["btn_mines"], callback_data="game_mines"),
         InlineKeyboardButton(text=t["btn_chicken"], callback_data="game_chicken_subway")],
        [InlineKeyboardButton(text=t["btn_reg"], callback_data="menu_register")],
        [InlineKeyboardButton(text=t["btn_supp"], url=SUPP),
         InlineKeyboardButton(text=t["btn_lang"], callback_data="change_language")]
    ])

def get_traps_keyboard(lang="en"):
    t = TEXTS[lang]
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="1 Trap 💣", callback_data="mines_trap_1"),
            InlineKeyboardButton(text="3 Traps 💣", callback_data="mines_trap_3")
        ],
        [
            InlineKeyboardButton(text="5 Traps 💣", callback_data="mines_trap_5"),
            InlineKeyboardButton(text="7 Traps 💣", callback_data="mines_trap_7")
        ],
        [InlineKeyboardButton(text=t["btn_back"], callback_data="back_to_main")]
    ])

def get_register_keyboard(lang="en"):
    t = TEXTS[lang]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["btn_reg_link"], url=REF_URL)],
        [InlineKeyboardButton(text=t["btn_tutorial"], callback_data="show_tutorial")],
        [InlineKeyboardButton(text=t["btn_back"], callback_data="back_to_main")]
    ])

def get_not_joined_keyboard(lang="en"):
    t = TEXTS[lang]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Join VIP Channel", url=CHANNEL_URL)],
        [InlineKeyboardButton(text=t["btn_verify"], callback_data="check_verify")]
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
    """Step 1: Always force language selection on /start"""
    await message.answer(
        "🌐 **Select Your Language / Chagua Lugha Yako:**",
        reply_markup=get_lang_keyboard(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data.startswith("set_lang_"))
async def set_language_handler(callback: types.CallbackQuery):
    """Step 2: Save language preference, then check channel verification immediately."""
    await callback.answer()
    lang = callback.data.split("_")[2]
    user = callback.from_user
    user_lang[user.id] = lang
    t = TEXTS[lang]
    
    safe_name = escape_md(user.full_name)
    asyncio.create_task(
        notify_admin_log(f"👤 **User Selected Language:** {safe_name} (`{user.id}`) ➡️ `{lang.upper()}`")
    )
    
    # Check Channel Membership right after selecting language
    is_member = await check_channel_member(user.id)
    if is_member:
        await callback.message.edit_text(
            t["welcome"].format(promo=PROMO),
            reply_markup=get_main_keyboard(lang),
            parse_mode="Markdown"
        )
    else:
        await callback.message.edit_text(
            t["not_member"],
            reply_markup=get_not_joined_keyboard(lang),
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

@dp.callback_query(F.data == "check_verify")
async def check_verify_handler(callback: types.CallbackQuery):
    user = callback.from_user
    lang = user_lang.get(user.id, "en")
    t = TEXTS[lang]

    is_member = await check_channel_member(user.id)
    if is_member:
        await callback.answer("✅ Verification successful!", show_alert=True)
        await callback.message.edit_text(
            t["welcome"].format(promo=PROMO),
            reply_markup=get_main_keyboard(lang),
            parse_mode="Markdown"
        )
    else:
        await callback.answer("❌ You haven't joined the channel yet!", show_alert=True)

@dp.callback_query(F.data == "menu_register")
async def register_menu_handler(callback: types.CallbackQuery):
    await callback.answer()
    user = callback.from_user
    lang = user_lang.get(user.id, "en")
    t = TEXTS[lang]

    await callback.message.edit_text(
        t["reg_menu"].format(promo=PROMO),
        reply_markup=get_register_keyboard(lang),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "show_tutorial")
async def tutorial_handler(callback: types.CallbackQuery):
    await callback.answer()
    user = callback.from_user
    lang = user_lang.get(user.id, "en")
    t = TEXTS[lang]

    await callback.message.edit_text(
        t["reg_tutorial"].format(promo=PROMO),
        reply_markup=get_register_keyboard(lang),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "back_to_main")
async def back_to_main_handler(callback: types.CallbackQuery):
    await callback.answer()
    user = callback.from_user
    lang = user_lang.get(user.id, "en")
    t = TEXTS[lang]

    await callback.message.edit_text(
        t["welcome"].format(promo=PROMO),
        reply_markup=get_main_keyboard(lang),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "game_mines")
async def mines_select_traps(callback: types.CallbackQuery):
    """Prompts user to select the number of traps (1, 3, 5, or 7)."""
    user = callback.from_user
    lang = user_lang.get(user.id, "en")
    t = TEXTS[lang]

    is_member = await check_channel_member(user.id)
    if not is_member:
        await callback.answer()
        await callback.message.edit_text(
            t["not_member"],
            reply_markup=get_not_joined_keyboard(lang),
            parse_mode="Markdown"
        )
        return

    await callback.answer()
    await callback.message.edit_text(
        t["select_traps"],
        reply_markup=get_traps_keyboard(lang),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data.startswith("mines_trap_"))
async def mines_generate_signal(callback: types.CallbackQuery):
    """Generates the grid based on selected traps with precise constraints."""
    user = callback.from_user
    lang = user_lang.get(user.id, "en")
    t = TEXTS[lang]

    is_member = await check_channel_member(user.id)
    if not is_member:
        await callback.answer()
        await callback.message.edit_text(
            t["not_member"],
            reply_markup=get_not_joined_keyboard(lang),
            parse_mode="Markdown"
        )
        return

    await callback.answer()

    traps = int(callback.data.split("_")[2])

    # Rule Definition: (revealed_traps, unrevealed_tiles)
    if traps == 1:
        revealed_traps = 0
        unrevealed_count = random.randint(3, 7)
    elif traps == 3:
        revealed_traps = random.randint(1, 2)
        unrevealed_count = random.randint(5, 9)
    elif traps == 5:
        revealed_traps = random.randint(1, 3)
        unrevealed_count = random.randint(7, 11)
    elif traps == 7:
        revealed_traps = random.randint(1, 5)
        unrevealed_count = random.randint(9, 13)
    else:
        revealed_traps = 1
        unrevealed_count = 5

    # 5x5 Grid total = 25 tiles
    # Revealed Safe Tiles (💎) filling the rest
    safe_tiles_count = 25 - revealed_traps - unrevealed_count

    grid_pool = (
        ["💣"] * revealed_traps +
        ["🟦"] * unrevealed_count +
        ["💎"] * safe_tiles_count
    )
    random.shuffle(grid_pool)

    grid_str = "\n".join([" ".join(grid_pool[i:i+5]) for i in range(0, 25, 5)])

    header = t["mines_title"].format(
        traps=traps,
        traps_revealed=revealed_traps,
        unrevealed=unrevealed_count
    )
    response_text = f"{header}\n\n{grid_str}"

    safe_name = escape_md(user.full_name)
    asyncio.create_task(
        notify_admin_log(f"💣 **Signal (Mines - {traps} Traps):** {safe_name} (`{user.id}`)")
    )

    await callback.message.edit_text(
        response_text,
        parse_mode="Markdown",
        reply_markup=get_traps_keyboard(lang)
    )

@dp.callback_query(F.data == "game_chicken_subway")
async def chicken_subway_handler(callback: types.CallbackQuery):
    user = callback.from_user
    lang = user_lang.get(user.id, "en")
    t = TEXTS[lang]

    is_member = await check_channel_member(user.id)
    if not is_member:
        await callback.answer()
        await callback.message.edit_text(
            t["not_member"],
            reply_markup=get_not_joined_keyboard(lang),
            parse_mode="Markdown"
        )
        return

    await callback.answer()

    # Generate 10 steps, each containing 1 green circle and 2 red circles shuffled randomly
    steps = []
    for _ in range(10):
        circles = ["🟢", "🔴", "🔴"]
        random.shuffle(circles)
        steps.append(" ".join(circles))

    response_text = t["chicken_title"].format(
        s1=steps[0], s2=steps[1], s3=steps[2], s4=steps[3], s5=steps[4],
        s6=steps[5], s7=steps[6], s8=steps[7], s9=steps[8], s10=steps[9]
    )

    safe_name = escape_md(user.full_name)
    asyncio.create_task(
        notify_admin_log(f"🐔 **Signal (Chicken Subway):** {safe_name} (`{user.id}`)")
    )
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
        safe_name = escape_md(user.full_name)
        asyncio.create_task(
            notify_admin_log(f"⚡ **Auto-Approved Join Request:** {safe_name} (`{user.id}`)")
        )
    except Exception as e:
        logging.error(f"Failed to approve join request: {e}")

# Dummy Server for Render Uptime
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
    await start_dummy_server()
    
    try:
        await dp.start_polling(
            bot, 
            allowed_updates=["message", "callback_query", "chat_join_request"]
        )
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())