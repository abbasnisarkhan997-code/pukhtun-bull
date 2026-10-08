const express = require('express');
const TelegramBot = require('node-telegram-bot-api');
const app = express();
const PORT = process.env.PORT || 10000;
const token = process.env.BOT_TOKEN;
const bot = new TelegramBot(token, {polling: true});
console.log("Pukhtun Bull Started");

bot.onText(/\/start/, (msg)=>{
 bot.sendMessage(msg.chat.id, `🔥 *Pukhtun Bull Bot* 🔥\n\nWelcome Abbas! Bot Online ✅\n\n/start - Start\n/signal - Signal\n\n🐂 Da Pukhtun Bull Taiyar Dy!`,{parse_mode:'Markdown'})
});

bot.onText(/\/signal/, (msg)=>{
 let pairs=["EUR/USD","GBP/USD","USD/JPY"];
 let p=pairs[Math.floor(Math.random()*pairs.length)];
 let d=Math.random()>0.5?"🔼 CALL UP":"🔽 PUT DOWN";
 bot.sendMessage(msg.chat.id, `📊 SIGNAL\nPair: ${p}\nDir: ${d}\nTime: ${new Date().toLocaleTimeString()}\nExpiry: 1Min`,{parse_mode:'Markdown'})
});

app.get('/', (req,res)=>{res.send('Bot Live ✅')});
app.listen(PORT, ()=>console.log("Running"));
