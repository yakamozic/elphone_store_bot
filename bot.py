import logging
import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("BOT_TOKEN")

DB = "store.db"
conn = sqlite3.connect(DB, check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    price INTEGER
)
""")
conn.commit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🛍 مشاهده محصولات", callback_data="show_products")]]
    await update.message.reply_text("سلام! به فروشگاه *Elphone Store Accessories* خوش اومدی.",
                                    parse_mode="Markdown",
                                    reply_markup=InlineKeyboardMarkup(keyboard))

async def addsample(update: Update, context: ContextTypes.DEFAULT_TYPE):
    c.execute("INSERT INTO products (name, description, price) VALUES (?, ?, ?)",
              ("کابل USB-C سریع", "کابل 1 متری - فست شارژ", 250000))
    conn.commit()
    await update.message.reply_text("✅ محصول نمونه اضافه شد.")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "show_products":
        c.execute("SELECT name, price FROM products")
        rows = c.fetchall()
        if not rows:
            await query.edit_message_text("هیچ محصولی ثبت نشده.")
        else:
            text = "📦 لیست محصولات:\n\n"
            for name, price in rows:
                text += f"{name} — {price} تومان\n"
            await query.edit_message_text(text)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addsample", addsample))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
