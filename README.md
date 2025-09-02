# 🚀 CryptoSpreadX

**Real-time Crypto Arbitrage Detector with Telegram Alerts**

---

## 📌 Overview

CryptoSpreadX is a Python-based project that monitors price differences (arbitrage opportunities) across multiple exchanges for different coins.
Whenever a profitable spread is detected, it **sends instant notifications to Telegram**.

Supported coins:

* **BTC, ETH, DOGE, PEPE, XRP, AVAX, GALA, POL, DOT, SHIB**

---

## ⚡ Features

✅ Real-time price fetching from multiple exchanges
✅ Arbitrage detection logic
✅ Telegram bot integration for instant alerts
✅ Extendable to more coins and exchanges
✅ Clean modular code (utils/api.py, utils/calc.py, main.py, bot.py)

---

## 🛠️ Tech Stack

* **Python 3.11+**
* `requests` → API calls
* `pandas` → data handling
* `python-telegram-bot` → Telegram integration
* `asyncio` → async event loop

---

## 📂 Project Structure

```
CryptoSpreadX/
│── main.py              # Main app logic
│── bot.py               # Telegram bot handler
│── requirements.txt     # Python dependencies
│── README.md            # This file
│
├── utils/
│   ├── api.py           # API requests to exchanges
│   ├── calc.py          # Arbitrage detection & calculations
│
└── .gitignore           # Ignore venv/cache files
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/CryptoSpreadX.git
cd CryptoSpreadX
```

### 2️⃣ Create a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate # Mac/Linux
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Setup Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Create a bot → get your **BOT TOKEN**
3. Add your **Chat ID** (you can use `@userinfobot` to find it)
4. Save them in your code as environment variables or directly in `bot.py`

---

## ▶️ Running the Project

Run the main script:

```bash
python main.py
```

You’ll start receiving Telegram alerts for arbitrage opportunities 🚨.

---

## 🛠️ Future Improvements

* Add more exchanges (Kraken, KuCoin, OKX)
* Web dashboard with live charts (Flask/Django + React)
* Auto-trading integration with APIs

---

⚡ **Made with caffeine and code by \Hrutik Gangarde**

---
