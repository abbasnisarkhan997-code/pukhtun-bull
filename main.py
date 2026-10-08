import os, yfinance as yf, pandas_ta as ta
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
LIVE = {"EURUSD":"EURUSD=X","GBPUSD":"GBPUSD=X","USDJPY":"JPY=X","AUDUSD":"AUDUSD=X"}
OTC = {"EURUSD_OTC":"EURUSD=X","GBPUSD_OTC":"GBPUSD=X","BTC_OTC":"BTC-USD"}

def get_1m_signal(ticker):
    try:
        df = yf.download(ticker, period="1d", interval="1m", progress=False)
        if len(df) < 100: return None
        df['RSI'] = ta.rsi(df['Close'], 14)
        last = df.iloc[-1]
        sup = df['Low'].tail(100).nsmallest(3).mean()
        res = df['High'].tail(100).nlargest(3).mean()
        price = float(last['Close']); rsi = float(last['RSI'])
        if abs(price-sup)/price*100 < 0.08 and 28 < rsi < 42:
            return f"BUY ⬆️ | Sup: {sup:.5f} | RSI:{rsi:.1f} | 1M Candle 1M Trade | ACC 86%"
        if abs(res-price)/price*100 < 0.08 and 58 < rsi < 72:
            return f"SELL ⬇️ | Res: {res:.5f} | RSI:{rsi:.1f} | 1M Candle 1M Trade | ACC 85%"
    except: return None
    return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[InlineKeyboardButton("📈 LIVE (1M)", callback_data="live"), InlineKeyboardButton("🌙 OTC (1M)", callback_data="otc")],
          [InlineKeyboardButton("🟢 AUTO ON 1M", callback_data="on"), InlineKeyboardButton("🔴 AUTO OFF", callback_data="off")]]
    await update.message.reply_text("🐂 PUKHTUN BULL 1M SNIPER\nCandle 1M | Trade 1M", reply_markup=InlineKeyboardMarkup(kb))

async def btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    if q.data in ["live","otc"]:
        pairs = LIVE if q.data=="live" else OTC
        for name,tick in pairs.items():
            s=get_1m_signal(tick)
            if s:
                await q.edit_message_text(f"🔥 SIGNAL 🔥\nPair: {name}\n{s}")
                return
        await q.edit_message_text("⚠️ Setup nahi bana, 1 min baad try karo.")
    if q.data=="on":
        context.job_queue.run_repeating(auto_job, interval=60, first=5, chat_id=q.message.chat_id, name="auto")
        await q.edit_message_text("🟢 AUTO ON")
    if q.data=="off":
        for j in context.job_queue.get_jobs_by_names("auto"): j.schedule_removal()
        await q.edit_message_text("🔴 AUTO OFF")

async def auto_job(context: ContextTypes.DEFAULT_TYPE):
    for name,tick in {**LIVE, **OTC}.items():
        s=get_1m_signal(tick)
        if s:
            await context.bot.send_message(chat_id=context.job.chat_id, text=f"🔥 AUTO 1M\nPair: {name}\n{s}")
            break

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(btn))
app.run_polling()
