// templates/views/server.js

const express = require('express');
const axios = require('axios');
const dotenv = require('dotenv');

// Initialize environment variables
dotenv.config();

const app = express();
const port = 3000;

// Retrieve Telegram bot token and chat ID from environment variables
const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const TELEGRAM_CHAT_ID = process.env.TELEGRAM_CHAT_ID;

// Middleware to parse incoming JSON
app.use(express.json());

// Endpoint to handle form submission
app.post('/send-message', async (req, res) => {
    const { name, phone_number, email, address, productName, productPrice, productQuantity, totalPrice } = req.body;

    const message = `
    🛎 New Order Confirmation 🛎

    👤 Name: ${name}
    📞 Phone: ${phone_number}
    📧 Email: ${email}
    🏠 Address: ${address}

    --------------------------------------
    📅 Booking Date: ${new Date().toLocaleString()}  
    --------------------------------------

    📦 Items:
    ${productName} (Quantity: ${productQuantity}, Price: $${productPrice.toFixed(2)})

    💵 Total Price: $${totalPrice.toFixed(2)}

    🎉 Thank you for your support! 🎉
    `;

    try {
        const response = await axios.post(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`, {
            chat_id: TELEGRAM_CHAT_ID,
            text: message,
        });
        res.status(200).send('Message sent successfully!');
    } catch (error) {
        console.error('Error sending message to Telegram:', error.response ? error.response.data : error.message);
        res.status(500).send('Failed to send message.');
    }
});



// Start server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
