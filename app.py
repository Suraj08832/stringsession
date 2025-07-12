import os
import Config
import logging
import threading
import time
import requests
from flask import Flask, jsonify
from pyromod import listen
from pyrogram import Client, idle
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid

# Configure logging
logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Initialize Flask app
app = Flask(__name__)

# Initialize Pyrogram client
bot = Client(
    ":memory:",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="StringSessionBot"),
)

# Global variable to track bot status
bot_running = False

def run_bot():
    """Function to run the Telegram bot"""
    global bot_running
    try:
        bot.start()
        bot_running = True
        uname = bot.get_me().username
        print(f"@{uname} Started Successfully!")
        idle()
    except (ApiIdInvalid, ApiIdPublishedFlood):
        print("Your API_ID/API_HASH is not valid.")
        bot_running = False
    except AccessTokenInvalid:
        print("Your BOT_TOKEN is not valid.")
        bot_running = False
    except Exception as e:
        print(f"Bot error: {e}")
        bot_running = False
    finally:
        bot.stop()
        print("Bot stopped. Alvida!")

def autoping():
    """Function to ping the app to keep it alive"""
    while True:
        try:
            # Ping the app itself
            response = requests.get("https://your-app-name.onrender.com/", timeout=10)
            print(f"Autoping response: {response.status_code}")
        except Exception as e:
            print(f"Autoping error: {e}")
        time.sleep(300)  # Ping every 5 minutes

@app.route('/')
def home():
    """Home route for health check"""
    return jsonify({
        "status": "Bot is running!",
        "bot_status": "Running" if bot_running else "Stopped",
        "message": "String Session Bot is active"
    })

@app.route('/ping')
def ping():
    """Ping route for autoping"""
    return jsonify({"status": "pong"})

@app.route('/status')
def status():
    """Status route to check bot status"""
    return jsonify({
        "bot_running": bot_running,
        "status": "online"
    })

if __name__ == "__main__":
    # Start bot in a separate thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Start autoping in a separate thread
    ping_thread = threading.Thread(target=autoping, daemon=True)
    ping_thread.start()
    
    # Run Flask app
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080))) 