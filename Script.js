document.getElementById('start').addEventListener('click', startTrading);
document.getElementById('stop').addEventListener('click', stopTrading);

let tradingActive = false;
let tradingInterval;

const apiBaseUrl = 'https://www.bitget.site/account/newapi'; // Replace with actual exchange API base URL
const apiKey = 'bg_ffcbb26a743c6f3617a03e4edb87aa3f'; // Replace with your API key
const apiSecret = 'e397e3420dbb6a1b48dfef734e6ef8d6aaf29ee44a044d51dd1742a8143c0693'; // Replace with your API secret

function updateStatus(message) {
    document.getElementById('status').innerText = message;
}

function startTrading() {
    if (tradingActive) return;

    tradingActive = true;
    updateStatus('Trading started...');
    tradingInterval = setInterval(trade, 2000); // Check every 5 seconds
}

function stopTrading() {
    if (!tradingActive) return;

    tradingActive = false;
    clearInterval(tradingInterval);
    updateStatus('Trading stopped.');
}

async function trade() {
    const buyPrice = parseFloat(document.getElementById('buyPrice').value);
    const sellPrice = parseFloat(document.getElementById('sellPrice').value);
    const amount = parseFloat(document.getElementById('amount').value);

    try {
        // Fetch current price from API
        const response = await fetch(`${apiBaseUrl}/price`);
        const data = await response.json();
        const currentPrice = parseFloat(data.price);

        if (currentPrice <= buyPrice) {
            // Place a buy order
            await placeOrder('buy', amount);
            updateStatus(`Bought ${amount} at ${currentPrice}`);
        } else if (currentPrice >= sellPrice) {
            // Place a sell order
            await placeOrder('sell', amount);
            updateStatus(`Sold ${amount} at ${currentPrice}`);
        }
    } catch (error) {
        updateStatus(`Error: ${error.message}`);
    }
}

async function placeOrder(type, amount) {
    const response = await fetch(`${apiBaseUrl}/order`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey}`
        },
        body: JSON.stringify({
            type: type,
            amount: amount
        })
    });
    const result = await response.json();
    return result;
}
