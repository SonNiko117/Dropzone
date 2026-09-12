import os

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    LabeledPrice,
    Update,
    WebAppInfo,
    BotCommand,
    MenuButtonCommands,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    PreCheckoutQueryHandler,
    filters,
)


BOT_TOKEN = os.getenv("BOT_TOKEN")

# Your DROPZONE Mini App URL
GAME_URL = "https://sonniko117.github.io/Dropzone/"

# Your DROPZONE News Channel
NEWS_CHANNEL_URL = "https://t.me/DropzoneGameNews"


# =========================
# /GAME
# =========================

async def game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "🎮 PLAY",
                web_app=WebAppInfo(url=GAME_URL)
            )
        ]
    ]

    await update.message.reply_text(
        "🔥 DROPZONE\n\n"
        "Ready to play?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================
# /NEWS
# =========================

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "📰 DROPZONE NEWS",
                url=NEWS_CHANNEL_URL
            )
        ]
    ]

    await update.message.reply_text(
        "📰 DROPZONE NEWS\n\n"
        "Get the latest updates and announcements here:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================
# /DONATE
# =========================

async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("⭐ 10 Stars", callback_data="donate_10"),
            InlineKeyboardButton("⭐ 50 Stars", callback_data="donate_50"),
        ],
        [
            InlineKeyboardButton("⭐ 100 Stars", callback_data="donate_100"),
            InlineKeyboardButton("⭐ 250 Stars", callback_data="donate_250"),
        ],
        [
            InlineKeyboardButton("⭐ 500 Stars", callback_data="donate_500"),
            InlineKeyboardButton("⭐ 1000 Stars", callback_data="donate_1000"),
        ],
    ]

    await update.message.reply_text(
        "❤️ SUPPORT DROPZONE\n\n"
        "If you enjoy DROPZONE, you can support the project "
        "by sending Telegram Stars.\n\n"
        "Choose an amount:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================
# STAR SELECTION
# =========================

async def donation_selected(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    amount = int(query.data.split("_")[1])

    await context.bot.send_invoice(
        chat_id=query.message.chat_id,
        title="DROPZONE Support",
        description=f"Support DROPZONE with {amount} Telegram Stars.",
        payload=f"dropzone_donation_{amount}",
        currency="XTR",
        prices=[
            LabeledPrice(
                label=f"DROPZONE Support - {amount} Stars",
                amount=amount
            )
        ],
    )


# =========================
# PRE-CHECKOUT
# =========================

async def pre_checkout(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.pre_checkout_query.answer(ok=True)


# =========================
# SUCCESSFUL PAYMENT
# =========================

async def successful_payment(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    payment = update.message.successful_payment

    await update.message.reply_text(
        "❤️ Thank you for supporting DROPZONE!\n\n"
        f"⭐ {payment.total_amount} Stars received successfully.\n\n"
        "Your support means a lot! 🙏🔥"
    )


# =========================
# START BOT
# =========================

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not configured!")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("game", game))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(CommandHandler("donate", donate))

    app.add_handler(
        CallbackQueryHandler(
            donation_selected,
            pattern=r"^donate_\d+$"
        )
    )

    app.add_handler(
        PreCheckoutQueryHandler(pre_checkout)
    )

    app.add_handler(
        MessageHandler(
            filters.SUCCESSFUL_PAYMENT,
            successful_payment
        )
    )

    print("DROPZONE Telegram Bot is running!")

    app.run_polling()


if __name__ == "__main__":
    main()