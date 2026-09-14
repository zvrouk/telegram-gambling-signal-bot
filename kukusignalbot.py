import random
import logging
import asyncio
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, ChatJoinRequest

# ================= CONFIGURATION =================
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Set your bot token
REF_URL = "https://lkyr.cc/6335d9"
CHANNEL_URL = "https://t.me/+WF5cBxNLYy0wMGU0"
CHANNEL_ID = -1002163714024
VERIFY_CHANNEL_ID = -1004417062544  # Private Admin Log Channel
SUPP = "https://t.me/unrichh"
ADMIN_ID = 6674976941
PROMO = "CARTEL100"
# =================================================

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# In-memory user state storage for language preference
user_lang = {}

# ================= DUMMY WEB SERVER FOR RENDER =================
async def handle_ping(request):
    """Keeps Render Free Web Service happy by answering HTTP checks."""
    return web.Response(text="Bot is online and polling!")

async def start_dummy_server():
    """Starts a lightweight web server on port 8080."""
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()

# ================= AUTOMATIC JOIN REQUEST APPROVAL =================
@dp.chat_join_request()
async def auto_approve_join_request(request: ChatJoinRequest):
    """Automatically approves join requests to the channel."""
    try:
        await request.approve()
        user = request.from_user
        logging.info(f"Approved join request for {user.full_name} ({user.id})")
        
        await notify_admin_log(
            f"✅ **Auto-Approved Join Request:** {user.full_name} (@{user.username or 'No_Username'}) [`{user.id}`]"
        )
    except Exception as e:
        logging.error(f"Failed to approve join request: {e}")

# ================= LOCALIZATION TEXTS =================
TEXTS = {
    "en": {
        "welcome": "🌐 **SELECT YOUR LANGUAGE / CHAGUA LUGHA YAKO**",
        "sub_required": (
            "🔒 **VIP CHANNEL ACCESS REQUIRED**\n\n"
            "To use El Cartel Signals, you must join our official channel first:\n"
            "1. Click **📢 Join VIP Channel** below.\n"
            "2. Click **✅ Verify VIP Access** to proceed."
        ),
        "register_prompt": (
            "✅ **CHANNEL VERIFIED!**\n\n"
            "⚠️ **FINAL STEP:** You must create an official 1Win account to receive active signals.\n\n"
            "1️⃣ Click **🔗 Register Account** below.\n"
            "2️⃣ Use Promo Code: `{promo}` to get a **500% Deposit Bonus**!\n"
            "3️⃣ Read the tutorial if you need help on registration or deposits."
        ),
        "main_menu": (
            "🚀 **EL CARTEL SIGNALS MAIN MENU** 🚀\n\n"
            "Select a game below to generate your high-accuracy prediction or view tutorials:"
        ),
        "tutorial_title": (
            "📖 **1WIN COMPLETE TUTORIAL**\n\n"
            "**1. How to Register an Account:**\n"
            "• Click the **🔗 Register Account** button.\n"
            "• Fill in your details (Phone number & Currency).\n"
            "• Enter Promo Code: `{promo}` under the Promo Code field.\n\n"
            "**2. How to Deposit:**\n"
            "• Open the 1Win deposit section.\n"
            "• Choose M-Pesa or your preferred payment method.\n"
            "• Enter deposit amount and confirm the STK Push on your phone.\n\n"
            "**3. How to Activate Promo Code:**\n"
            "• Entering promo code `{promo}` during registration or on deposit automatically activates your 500% bonus funds!\n\n"
            "💡 *Once registered, you can start requesting signal predictions!*"
        ),
        "mines_title": "💣 **MINES SIGNAL GENERATED (80% REVEALED)** 💣\n\n{grid}\n\n📌 **Legend:**\n💎 = Safe Tile | 💣 = Mine Danger | ⬛ = Hidden Tile\n👉 **Instructions:** Open the safe 💎 positions in your game session!",
        "chicken_title": (
            "🐔 **CHICKEN SUBWAY SIGNAL (5 STEPS)** 🐔\n\n"
            "🛤️ **Step 1:** Track 1: `x{s1_1}` | Track 2: `x{s1_2}` | Track 3: `x{s1_3}`\n"
            "➡️ **Pick:** **{r1}**\n\n"
            "🛤️ **Step 2:** Track 1: `x{s2_1}` | Track 2: `x{s2_2}` | Track 3: `x{s2_3}`\n"
            "➡️ **Pick:** **{r2}**\n\n"
            "🛤️ **Step 3:** Track 1: `x{s3_1}` | Track 2: `x{s3_2}` | Track 3: `x{s3_3}`\n"
            "➡️ **Pick:** **{r3}**\n\n"
            "🛤️ **Step 4:** Track 1: `x{s4_1}` | Track 2: `x{s4_2}` | Track 3: `x{s4_3}`\n"
            "➡️ **Pick:** **{r4}**\n\n"
            "🛤️ **Step 5 (Max Risk):** Track 1: `x{s5_1}` | Track 2: `x{s5_2}` | Track 3: `x{s5_3}`\n\n"
            "💰 **Recommended Strategy:** Cash out after **Step 3 or 4** to secure profit."
        ),
        "promo_info": "🎁 **EXCLUSIVE PROMO CODE** 🎁\n\nCode: `{promo}`\n\nApply code `{promo}` on 1Win for a 500% deposit bonus!",
        "btn_join": "📢 Join VIP Channel",
        "btn_verify": "✅ Verify VIP Access",
        "btn_register": "🔗 Register Account (Official)",
        "btn_tutorial": "📖 1Win Tutorial",
        "btn_proceed": "🚀 Proceed to Predictions",
        "btn_mines": "💣 Mines",
        "btn_chicken": "🐔 Chicken Subway",
        "btn_promo": "🎁 Promo Code",
        "btn_lang": "🌐 Change Language",
        "btn_support": "💬 Support",
        "btn_menu": "🔙 Main Menu"
    },
    "sw": {
        "welcome": "🌐 **CHAGUA LUGHA YAKO / SELECT YOUR LANGUAGE**",
        "sub_required": (
            "🔒 **INAHITAJI KUGUJIUNGA NA CHANNEL YA VIP**\n\n"
            "Ili kutumia El Cartel Signals, lazima ujiunge na channel yetu kwanza:\n"
            "1. Bonyeza **📢 Jiunge na Channel** hapa chini.\n"
            "2. Bonyeza **✅ Hakiki Usajili** kuendelea."
        ),
        "register_prompt": (
            "✅ **CHANNEL IMEHAKIKISHWA!**\n\n"
            "⚠️ **HATUA YA MWISHO:** Lazima utengeneze akaunti mpya ya 1Win ili kupata ishara za uhakika.\n\n"
            "1️⃣ Bonyeza **🔗 Sajili Akaunti** hapa chini.\n"
            "2️⃣ Tumia Promo Code: `{promo}` kupata **Bonus ya 500%**!\n"
            "3️⃣ Soma mwongozo ukihitaji msaada wa kusajili au kuweka pesa."
        ),
        "main_menu": (
            "🚀 **EL CARTEL SIGNALS MAIN MENU** 🚀\n\n"
            "Chagua mchezo hapa chini kupata utabiri au usome mwongozo:"
        ),
        "tutorial_title": (
            "📖 **MWONGOZO KAMILI WA 1WIN**\n\n"
            "**1. Jinsi ya Kusajili Akaunti:**\n"
            "• Bonyeza kitufe cha **🔗 Sajili Akaunti**.\n"
            "• Jaza maelezo yako (Nambari ya simu na Sarafu).\n"
            "• Weka Promo Code: `{promo}` kwenye sehemu ya Promo Code.\n\n"
            "**2. Jinsi ya Kuweka Pesa (Deposit):**\n"
            "• Fungua sehemu ya Deposit kwenye 1Win.\n"
            "• Chagua M-Pesa au njia unayopendelea.\n"
            "• Weka kiasi na uthibitishe M-Pesa PIN kwenye simu yako.\n\n"
            "**3. Jinsi ya Kutumia Promo Code:**\n"
            "• Unapoweka promo code `{promo}` wakati wa usajili au deposit, unapokea bonus ya 500% papo hapo!\n\n"
            "💡 *Ukimaliza kusajili, unaweza kuanza kupokea signals!*"
        ),
        "mines_title": "💣 **SIGNAL YA MINES (80% IMEONESHWAN):** 💣\n\n{grid}\n\n📌 **Maelezo:**\n💎 = Salama | 💣 = Bomu / Hatari | ⬛ = Imefichwa\n👉 **Maagizo:** Fungua sehemu zenye 💎 kwenye mchezo wako!",
        "chicken_title": (
            "🐔 **SIGNAL YA CHICKEN SUBWAY (HATUA 5)** 🐔\n\n"
            "🛤️ **Hatua 1:** Njia 1: `x{s1_1}` | Njia 2: `x{s1_2}` | Njia 3: `x{s1_3}`\n"
            "➡️ **Chagua:** **{r1}**\n\n"
            "🛤️ **Hatua 2:** Njia 1: `x{s2_1}` | Njia 2: `x{s2_2}` | Njia 3: `x{s2_3}`\n"
            "➡️ **Chagua:** **{r2}**\n\n"
            "🛤️ **Hatua 3:** Njia 1: `x{s3_1}` | Njia 2: `x{s3_2}` | Njia 3: `x{s3_3}`\n"
            "➡️ **Chagua:** **{r3}**\n\n"
            "🛤️ **Hatua 4:** Njia 1: `x{s4_1}` | Njia 2: `x{s4_2}` | Njia 3: `x{s4_3}`\n"
            "➡️ **Chagua:** **{r4}**\n\n"
            "🛤️ **Hatua 5 (Hatari Kubwa):** Njia 1: `x{s5_1}` | Njia 2: `x{s5_2}` | Njia 3: `x{s5_3}`\n\n"
            "💰 **Mbinu:** Toa pesa baada ya **Hatua ya 3 au 4** ili kulinda faida."
        ),
        "promo_info": "🎁 **PROMO CODE YA PEKEE** 🎁\n\nKodi: `{promo}`\n\nTumia kodi `{promo}` kwenye 1Win ili upate bonus ya 500% ya deposit!",
        "btn_join": "📢 Jiunge na Channel",
        "btn_verify": "✅ Hakiki Usajili",
        "btn_register": "🔗 Sajili Akaunti (Rasmi)",
        "btn_tutorial": "📖 Mwongozo wa 1Win",
        "btn_proceed": "🚀 Endelea kwenye Signals",
        "btn_mines": "💣 Mines",
        "btn_chicken": "🐔 Chicken Subway",
        "btn_promo": "🎁 Promo Code",
        "btn_lang": "🌐 Badilisha Lugha",
        "btn_support": "💬 Msaada",
        "btn_menu": "🔙 Main Menu"
    }
}

async def set_bot_commands():
    """Sets the native Telegram command menu button."""
    commands = [
        BotCommand(command="start", description="🚀 Main Signal Menu / Menyu Kuu")
    ]
    await bot.set_my_commands(commands)

async def check_subscription(user_id: int) -> bool:
    """Verifies if the user is a member of the public VIP channel."""
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in ["left", "kicked"]:
            return False
        return True
    except Exception as e:
        logging.error(f"Error checking membership for {CHANNEL_ID}: {e}")
        return False

async def notify_admin_log(text: str):
    """Sends activity notifications to your private log channel."""
    try:
        await bot.send_message(chat_id=VERIFY_CHANNEL_ID, text=text, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Failed to send log notification to {VERIFY_CHANNEL_ID}: {e}")

# ================= KEYBOARD BUILDERS =================
def get_lang_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇬🇧 English", callback_data="set_lang_en"),
                InlineKeyboardButton(text="🇰🇪 Swahili", callback_data="set_lang_sw")
            ]
        ]
    )

def get_sub_keyboard(lang="en"):
    t = TEXTS[lang]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t["btn_join"], url=CHANNEL_URL)],
            [InlineKeyboardButton(text=t["btn_verify"], callback_data="check_sub")],
            [InlineKeyboardButton(text=t["btn_support"], url=SUPP)]
        ]
    )

def get_registration_keyboard(lang="en"):
    t = TEXTS[lang]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t["btn_register"], url=REF_URL)],
            [InlineKeyboardButton(text=t["btn_tutorial"], callback_data="show_tutorial")],
            [InlineKeyboardButton(text=t["btn_proceed"], callback_data="main_menu")],
            [InlineKeyboardButton(text=t["btn_support"], url=SUPP)]
        ]
    )

def get_main_keyboard(lang="en"):
    t = TEXTS[lang]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t["btn_mines"], callback_data="game_mines"),
                InlineKeyboardButton(text=t["btn_chicken"], callback_data="game_chicken_subway")
            ],
            [
                InlineKeyboardButton(text=t["btn_register"], url=REF_URL),
                InlineKeyboardButton(text=t["btn_tutorial"], callback_data="show_tutorial")
            ],
            [
                InlineKeyboardButton(text=t["btn_promo"], callback_data="show_promo"),
                InlineKeyboardButton(text=t["btn_lang"], callback_data="change_lang")
            ],
            [InlineKeyboardButton(text=t["btn_support"], url=SUPP)]
        ]
    )

def get_back_keyboard(lang="en"):
    t = TEXTS[lang]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t["btn_menu"], callback_data="main_menu")]
        ]
    )

# ================= BOT HANDLERS =================
@dp.message(Command("start"))
async def start_command(message: types.Message):
    user = message.from_user
    await notify_admin_log(
        f"🤖 **Bot Started:** {user.full_name} (@{user.username or 'No_Username'}) [`{user.id}`]"
    )
    
    await message.answer(
        TEXTS["en"]["welcome"],
        reply_markup=get_lang_keyboard()
    )

@dp.callback_query(F.data.startswith("set_lang_"))
async def set_language_callback(callback: types.CallbackQuery):
    lang = callback.data.split("_")[-1]
    user_lang[callback.from_user.id] = lang
    await callback.answer()

    is_subbed = await check_subscription(callback.from_user.id)
    t = TEXTS[lang]

    if not is_subbed:
        await callback.message.edit_text(
            t["sub_required"],
            parse_mode="Markdown",
            reply_markup=get_sub_keyboard(lang)
        )
    else:
        await callback.message.edit_text(
            t["register_prompt"].format(promo=PROMO),
            parse_mode="Markdown",
            reply_markup=get_registration_keyboard(lang)
        )

@dp.callback_query(F.data == "change_lang")
async def change_lang_callback(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        TEXTS["en"]["welcome"],
        reply_markup=get_lang_keyboard()
    )

@dp.callback_query(F.data == "check_sub")
async def verify_sub_callback(callback: types.CallbackQuery):
    user = callback.from_user
    lang = user_lang.get(user.id, "en")
    t = TEXTS[lang]
    
    is_subbed = await check_subscription(user.id)
    if is_subbed:
        await callback.answer("✅ Verified!", show_alert=True)
        await notify_admin_log(
            f"✅ **Access Verified:** {user.full_name} (@{user.username or 'No_Username'}) [`{user.id}`]"
        )
        await callback.message.edit_text(
            t["register_prompt"].format(promo=PROMO),
            parse_mode="Markdown",
            reply_markup=get_registration_keyboard(lang)
        )
    else:
        await callback.answer(
            "❌ VIP Channel not joined!" if lang == "en" else "❌ Hujajiunga na VIP Channel!",
            show_alert=True
        )

@dp.callback_query(F.data == "show_tutorial")
async def tutorial_callback(callback: types.CallbackQuery):
    await callback.answer()
    lang = user_lang.get(callback.from_user.id, "en")
    t = TEXTS[lang]
    
    await callback.message.edit_text(
        t["tutorial_title"].format(promo=PROMO),
        parse_mode="Markdown",
        reply_markup=get_back_keyboard(lang)
    )

@dp.callback_query(F.data == "main_menu")
async def main_menu_callback(callback: types.CallbackQuery):
    await callback.answer()
    lang = user_lang.get(callback.from_user.id, "en")
    t = TEXTS[lang]
    
    await callback.message.edit_text(
        t["main_menu"],
        parse_mode="Markdown",
        reply_markup=get_main_keyboard(lang)
    )

@dp.callback_query(F.data == "show_promo")
async def promo_callback(callback: types.CallbackQuery):
    await callback.answer()
    lang = user_lang.get(callback.from_user.id, "en")
    t = TEXTS[lang]
    
    await callback.message.edit_text(
        t["promo_info"].format(promo=PROMO),
        parse_mode="Markdown",
        reply_markup=get_back_keyboard(lang)
    )

@dp.callback_query(F.data == "game_mines")
async def mines_handler(callback: types.CallbackQuery):
    await callback.answer()
    user = callback.from_user
    lang = user_lang.get(user.id, "en")
    t = TEXTS[lang]

    grid = [["⬛" for _ in range(5)] for _ in range(5)]
    revealed = random.sample(range(25), 20)
    diamonds, mines = revealed[:16], revealed[16:]

    for pos in diamonds:
        grid[pos // 5][pos % 5] = "💎"
    for pos in mines:
        grid[pos // 5][pos % 5] = "💣"

    matrix_str = "\n".join(["".join(row) for row in grid])
    response_text = t["mines_title"].format(grid=matrix_str)

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
        s5_1=s5[0], s5_2=s5[1], s5_3=s5[2]
    )

    await notify_admin_log(f"🐔 **Signal (Chicken Subway):** {user.full_name} [`{user.id}`]")
    await callback.message.edit_text(
        response_text,
        parse_mode="Markdown",
        reply_markup=get_main_keyboard(lang)
    )

async def main():
    await set_bot_commands()
    await start_dummy_server()  # Starts the server to fulfill Render's health checks
    await dp.start_polling(bot, allowed_updates=["message", "callback_query", "chat_join_request"])

if __name__ == "__main__":
    asyncio.run(main())