// Configuration
const API_KEY = "MK_PROD_FLX4P92EDF"; // Replace with your API Key
const SECRET_KEY = "YOUR_SECRET_KEY"; // Replace with your Secret Key
const BASE_URL = "https://api.monnify.com"; // Use sandbox URL for testing: https://sandbox.monnify.com

// Function to generate Basic Auth token
function generateAuthToken() {
    const token = btoa(`${API_KEY}:${SECRET_KEY}`);
    return `Basic ${token}`;
}

// Function to create a wallet
async function createWallet(walletData) {
    const authToken = generateAuthToken();
    const endpoint = `${BASE_URL}/api/v2/disbursements/wallet`;

    try {
        const response = await fetch(endpoint, {
            method: "POST",
            headers: {
                "Authorization": authToken,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(walletData)
        });

        const data = await response.json();
        if (data.requestSuccessful) {
            return data.responseBody; // Return wallet details
        } else {
            throw new Error(data.responseMessage);
        }
    } catch (error) {
        console.error("Error creating wallet:", error);
        throw error;
    }
}

// Function to debit the wallet
async function debitWallet(debitData) {
    const authToken = generateAuthToken();
    const endpoint = `${BASE_URL}/api/v2/disbursements/single`;

    try {
        const response = await fetch(endpoint, {
            method: "POST",
            headers: {
                "Authorization": authToken,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(debitData)
        });

        const data = await response.json();
        if (data.requestSuccessful) {
            return data.responseBody; // Return debit details
        } else {
            throw new Error(data.responseMessage);
        }
    } catch (error) {
        console.error("Error debiting wallet:", error);
        throw error;
    }
}

// Function to display messages
function showMessage(elementId, text, type = "info") {
    const messageDiv = document.getElementById(elementId);
    messageDiv.textContent = text;
    messageDiv.className = `message ${type === 'error' ? 'error' : 'success'}`;

    // Clear message after 5 seconds
    setTimeout(() => {
        messageDiv.textContent = '';
        messageDiv.className = 'message';
    }, 5000);
}
