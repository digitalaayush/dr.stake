from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import re
import asyncio

# Predefined seed format (64-character hexadecimal)
SEED_PATTERN = r"^[a-f0-9]{64}$"

# Mini-App URL
MINI_APP_URL = "https://drstake.surge.sh/"

# 🔑 Single Master Access Key
MASTER_KEY = "89g6kk55rs87demo"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗠𝗘𝗦𝗔𝗚𝗘"""
    await update.message.reply_text(
        "WELCOME TO Dr .Stake (Free BOT)\n\n"
        "𝗖𝗟𝗜𝗖𝗞 𝗧𝗛𝗘 𝗕𝗨𝗧𝗧𝗢𝗡 𝗕𝗘𝗟𝗢𝗪 𝗧𝗢 𝗚𝗘𝗧 𝗦𝗧𝗔𝗥𝗧𝗘𝗗:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⏰𝗦𝗧𝗔𝗥𝗧", callback_data="begin_process")]
        ])
    )

async def begin_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """💣𝗦𝗘𝗟𝗘𝗖𝗧 𝗡𝗨𝗠𝗕𝗘𝗥 𝗢𝗙 𝗠𝗜𝗡𝗘𝗦⬇️"""
    query = update.callback_query
    await query.answer()
    await query.message.delete()
    await query.message.reply_text(
        "💣𝗦𝗘𝗟𝗘𝗖𝗧 𝗡𝗨𝗠𝗕𝗘𝗥 𝗢𝗙 𝗠𝗜𝗡𝗘𝗦⬇️:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("1 [𝗩𝗜𝗣]💣", callback_data="mines_1")],
            [InlineKeyboardButton("2 [𝗩𝗜𝗣]💣", callback_data="mines_2")]
        ])
    )

async def select_mines(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """𝗬𝗢𝗨 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗠𝗜𝗡𝗘𝗦"""
    query = update.callback_query
    await query.answer()
    selected_mines = query.data.split("_")[1]

    if selected_mines not in ["1", "2"]:
        await query.message.reply_text("❌ Invalid selection. Please choose 1 or 2 mines only.")
        return

    await query.message.reply_text(
        f"𝗬𝗢𝗨 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 {selected_mines} [𝗩𝗜𝗣]💣\n\n"
        "𝗖𝗟𝗜𝗖𝗞 𝗧𝗛𝗘 𝗕𝗨𝗧𝗧𝗢𝗡 𝗕𝗘𝗟𝗢𝗪 𝗧𝗢 𝗖𝗢𝗡𝗧𝗜𝗡𝗨𝗘👇:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀𝗦𝗧𝗔𝗥𝗧", callback_data="start_process")]
        ])
    )

async def process_start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """𝗣𝗥𝗢𝗩𝗜𝗗𝗘 𝗬𝗢𝗨𝗥 𝗦𝗘𝗥𝗩𝗘𝗥 𝗦𝗘𝗘𝗗"""
    query = update.callback_query
    await query.answer()
    await query.message.reply_photo(
        photo="https://i.imgur.com/r6nv6qp.jpg",
        caption="𝗙𝗜𝗡𝗗 𝗬𝗢𝗨𝗥 (𝗔𝗖𝗧𝗜𝗩𝗘 𝗦𝗘𝗥𝗩𝗘𝗥 𝗦𝗘𝗘𝗗) 𝗮𝗻𝗱 𝗣𝗔𝗦𝗧𝗘 𝗜𝗧 𝗛𝗘𝗥𝗘: ⬇️⬇️",
        parse_mode="Markdown"
    )
    context.user_data['waiting_for_seed'] = True

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """𝗛𝗔𝗡𝗗𝗟𝗘 𝗦𝗘𝗘𝗗 + 𝗠𝗔𝗦𝗧𝗘𝗥 𝗞𝗘𝗬"""
    if context.user_data.get('waiting_for_seed'):
        server_seed = update.message.text.strip()
        analyzing_message = await update.message.reply_text("🔍 ANALYZING...")

        await asyncio.sleep(2)
        if re.match(SEED_PATTERN, server_seed):
            await analyzing_message.edit_text(
                "✅ SEED VERIFIED\n\n🔑 ENTER MASTER KEY:",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔑 ENTER MASTER KEY", callback_data="enter_access_key")]
                ])
            )
        else:
            await analyzing_message.edit_text("🚨 INVALID SERVER SEED. TRY AGAIN. /start")
        context.user_data['waiting_for_seed'] = False

    elif context.user_data.get('awaiting_key'):
        key_entered = update.message.text.strip()
        context.user_data['awaiting_key'] = False

        if key_entered == MASTER_KEY:
            anim_msg = await update.message.reply_text("🔍 VERIFYING MASTER KEY...")
            await asyncio.sleep(2)
            await anim_msg.edit_text(
                "✅ MASTER KEY VERIFIED!\n\n🚀 OPENING MINI APP...",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🚀 OPEN MINI APP", web_app=WebAppInfo(url=MINI_APP_URL))]
                ])
            )
        else:
            await update.message.reply_text("❌ INVALID MASTER KEY. TRY AGAIN.\n\n🔑 ENTER MASTER KEY:")

async def access_key_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask for master key"""
    query = update.callback_query
    await query.answer()
    if query.data == "enter_access_key":
        msg = await query.message.edit_text("🔑 PLEASE ENTER YOUR MASTER KEY HERE👇")
        context.user_data["awaiting_key"] = True
        asyncio.create_task(wait_for_key_timeout(query.message.chat_id, msg.message_id, context))

async def wait_for_key_timeout(chat_id, message_id, context: ContextTypes.DEFAULT_TYPE):
    """Timeout if no key entered"""
    await asyncio.sleep(15)
    if context.user_data.get("awaiting_key"):
        try:
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="🔑 PLEASE ENTER YOUR MASTER KEY HERE👇",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔑 ENTER MASTER KEY", callback_data="enter_access_key")]
                ])
            )
        except Exception as e:
            print(e)

def main():
    application = ApplicationBuilder().token("8477862139:AAGDfVLrhj3zPCP9Hxkt3EzF9dHAlmQLcFU").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(begin_process, pattern="^begin_process$"))
    application.add_handler(CallbackQueryHandler(select_mines, pattern="^mines_"))
    application.add_handler(CallbackQueryHandler(process_start_callback, pattern="^start_process$"))
    application.add_handler(CallbackQueryHandler(access_key_options, pattern="^enter_access_key$"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()
