
import os, yfinance as yf
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import pandas as pd

TOKEN = os.getenv("BOT_TOKEN")
LIVE = {"EURUSD":"EURUSD=X","GBPUSD":"GBPUSD=X","USDJPY":"JPY=X","BTCUSD":"BTC-USD","GOLD":"GC=F"}
OTC = {"EURUSD_OTC":"EURUSD=X","GBPUSD_OTC":"GBPUSD=X","USDJPY_OTC":"JPY=X","BTC_OTC":"BTC-USD"}

def get_1m_signal(ticker):
    try:
        df = yf.download(ticker, period="1d", interval="1m", progress=False)
        if len(df) < 100: return None
        # RSI Manual
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        last = df.iloc[-1]
        sup = df['Low'].tail(100).nsmallest(3).mean()
        res = df['High'].tail(100).nlargest(3).mean()
        price = float(last['Close']); rsi = float(last['RSI'])
        if abs(price-sup)/price*100 < 0.08 and rsi < 45:
            return f"BUY ⬆️ | Sup: {sup:.5f} | RSI:{rsi:.1f} | Price:{price:.5f}"
        if abs(res-price)/price*100 < 0.08 and rsi > 55:
            return f"SELL ⬇️ | Res: {res:.5f} | RSI:{rsi:.1f} | Price:{price:.5f}"
        return f"WAIT | RSI:{rsi:.1f} | Price:{price:.5f}"
    except Exception as e:
        return f"Error: {e}"

async def start(update, context):
    kb = [[InlineKeyboardButton("LIVE Market", callback_data="live"), InlineKeyboardButton("OTC Market", callback_data="otc")]]
    await update.message.reply_text("Welcome Abbas! Pukhtun Bull Ready 🔥\nSelect Market:", reply_markup=InlineKeyboardMarkup(kb))

async def btn(update, context):
    q = update.callback_query; await q.answer()
    if q.data == "live":
        kb = [[InlineKeyboardButton(k, callback_data=f"L_{v}")] for k,v in LIVE.items()]
        await q.edit_message_text("Select LIVE Pair:", reply_markup=InlineKeyboardMarkup(kb))
    elif q.data == "otc":
        kb = [[InlineKeyboardButton(k, callback_data=f"O_{v}")] for k,v in OTC.items()]
        await q.edit_message_text("Select OTC Pair:", reply_markup=InlineKeyboardMarkup(kb))
    elif q.data.startswith("L_") or q.data.startswith("O_"):
        ticker = q.data[2:]
        await q.edit_message_text(f"Analyzing {ticker}...")
        sig = get_1m_signal(ticker)
        await q.edit_message_text(f"{ticker} -> {sig}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(btn))
    app.run_polling()

if __name__ == "__main__":
    main()
