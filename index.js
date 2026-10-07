const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.send('Pukhtun Bull is Running! 🐂🚀');
});

app.get('/bull', (req, res) => {
  res.json({
    name: "Pukhtun Bull",
    status: "Strong",
    power: "100%",
    message: "Da Pukhtun Bull Taiyar De!"
  });
});

app.listen(PORT, () => {
  console.log(`Pukhtun Bull running on port ${PORT}`);
});
