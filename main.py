import os, yfinance as yf
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

TOKEN = os.getenv("BOT_TOKEN")

LIVE = {"EURUSD":"EURUSD=X","GBPUSD":"GBPUSD=X","BTCUSD":"BTC-USD"}
OTC = {"EURUSD_OTC":"EURUSD=X","GBPUSD_OTC":"GBPUSD=X"}

def get_signal(t):
    df = yf.download(t, period="1d", interval="1m", progress=False)
    if len(df) < 50:
        return "WAIT - Data kam hai"
    d = df['Close'].diff()
    g = d.where(d > 0, 0).rolling(14).mean()
    l = -d.where(d < 0, 0).rolling(14).mean()
    rsi = 100 - (100 / (1 + g/l))
    last_rsi = float(rsi.iloc[-1])
    price = float(df['Close'].iloc[-1])
    if last_rsi < 40:
        return f"BUY ⬆️ RSI:{last_rsi:.1f} P:{price:.5f}"
    if last_rsi > 60:
        return f"SELL ⬇️ RSI:{last_rsi:.1f} P:{price:.5f}"
    return f"WAIT RSI:{last_rsi:.1f}"

async def start(update, context):
    kb = [[InlineKeyboardButton("LIVE Market", callback_data="live")],
          [InlineKeyboardButton("OTC Market", callback_data="otc")]]
    await update.message.reply_text("Pukhtun Bull Ready 🔥\nSelect:", reply_markup=InlineKeyboardMarkup(kb))

async def btn(update, context):
    q = update.callback_query
    await q.answer()
    if q.data == "live":
        kb = [[InlineKeyboardButton(k, callback_data=f"L_{v}")] for k,v in LIVE.items()]
        await q.edit_message_text("LIVE Select:", reply_markup=InlineKeyboardMarkup(kb))
    elif q.data == "otc":
        kb = [[InlineKeyboardButton(k, callback_data=f"O_{v}")] for k,v in OTC.items()]
        await q.edit_message_text("OTC Select:", reply_markup=InlineKeyboardMarkup(kb))
    else:
        t = q.data[2:]
        await q.edit_message_text(f"Checking {t}...")
        s = get_signal(t)
        await q.edit_message_text(f"{t} -> {s}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(btn))
    app.run_polling()

if __name__ == "__main__":
    main()
