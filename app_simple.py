import os
import logging
import threading
import time
import requests
from flask import Flask, jsonify
from pyromod import listen
from pyrogram import Client, idle, filters
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Global variable to track bot status
bot_running = False
bot_client = None
bot_thread = None

def run_bot():
    """Function to run the Telegram bot"""
    global bot_running, bot_client
    try:
        logger.info("Starting Telegram bot...")
        print("Starting Telegram bot...")
        
        # Bot credentials
        API_ID = 28053244
        API_HASH = "a7d745be7c8ba465750bfad1e7abc075"
        BOT_TOKEN = "7744856670:AAFJt9j0SnB4nD0nZkInYXGb6njSBfLWuWs"
        
        logger.info(f"Using API_ID: {API_ID}")
        logger.info(f"Using API_HASH: {API_HASH[:10]}...")
        logger.info(f"Using BOT_TOKEN: {BOT_TOKEN[:20]}...")
        
        logger.info("Initializing Pyrogram client...")
        print("Initializing Pyrogram client...")
        
        # Initialize Pyrogram client with time sync
        bot_client = Client(
            "render_bot_session_new",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="StringSessionBot"),
            sleep_threshold=30,
        )
        
        # Add a simple test handler
        @bot_client.on_message(filters.command("test"))
        async def test_handler(client, message):
            await message.reply("Bot is working! 🎉")
            logger.info(f"Test message received from {message.from_user.id}")
            print(f"Test message received from {message.from_user.id}")
        
        logger.info("Bot client initialized, starting...")
        print("Bot client initialized, starting...")
        
        # Start the bot
        logger.info("Calling bot_client.start()...")
        print("Calling bot_client.start()...")
        bot_client.start()
        
        logger.info("Bot started successfully, getting bot info...")
        print("Bot started successfully, getting bot info...")
        bot_running = True
        
        # Get bot info
        me = bot_client.get_me()
        logger.info(f"@{me.username} Started Successfully!")
        print(f"@{me.username} Started Successfully!")
        
        logger.info("Starting idle loop...")
        print("Starting idle loop...")
        
        # Keep the bot running with idle
        idle()
        
    except (ApiIdInvalid, ApiIdPublishedFlood) as e:
        logger.error(f"API Error: {e}")
        print("Your API_ID/API_HASH is not valid.")
        bot_running = False
    except AccessTokenInvalid as e:
        logger.error(f"Token Error: {e}")
        print("Your BOT_TOKEN is not valid.")
        bot_running = False
    except ImportError as e:
        logger.error(f"Import Error: {e}")
        print(f"Import Error: {e}")
        bot_running = False
    except Exception as e:
        logger.error(f"Bot error: {e}")
        print(f"Bot error: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        print(f"Full traceback: {traceback.format_exc()}")
        bot_running = False
    finally:
        if bot_client:
            try:
                bot_client.stop()
            except:
                pass
        logger.info("Bot stopped.")
        print("Bot stopped. Alvida!")

def autoping():
    """Function to ping the app to keep it alive"""
    while True:
        try:
            # Ping the app itself using the actual Render URL
            response = requests.get("https://stringsession-7ut7.onrender.com/", timeout=10)
            logger.info(f"Autoping response: {response.status_code}")
            print(f"Autoping response: {response.status_code}")
        except Exception as e:
            logger.error(f"Autoping error: {e}")
            print(f"Autoping error: {e}")
        time.sleep(300)  # Ping every 5 minutes

@app.route('/')
def home():
    """Home route for health check"""
    return jsonify({
        "status": "Bot is running!",
        "bot_status": "Running" if bot_running else "Stopped",
        "message": "String Session Bot is active",
        "timestamp": time.time()
    })

@app.route('/ping')
def ping():
    """Ping route for autoping"""
    return jsonify({"status": "pong", "timestamp": time.time()})

@app.route('/status')
def status():
    """Status route to check bot status"""
    return jsonify({
        "bot_running": bot_running,
        "status": "online",
        "timestamp": time.time()
    })

@app.route('/start-bot')
def start_bot():
    """Manual endpoint to start the bot"""
    global bot_running, bot_thread
    if not bot_running:
        bot_thread = threading.Thread(target=run_bot, daemon=True)
        bot_thread.start()
        return jsonify({"message": "Bot starting...", "status": "starting"})
    else:
        return jsonify({"message": "Bot is already running", "status": "running"})

@app.route('/stop-bot')
def stop_bot():
    """Manual endpoint to stop the bot"""
    global bot_running
    if bot_running:
        bot_running = False
        return jsonify({"message": "Bot stopping...", "status": "stopping"})
    else:
        return jsonify({"message": "Bot is not running", "status": "stopped"})

if __name__ == "__main__":
    logger.info("Starting Flask app with bot...")
    print("Starting Flask app with bot...")
    
    # Start bot in a separate thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Start autoping in a separate thread
    ping_thread = threading.Thread(target=autoping, daemon=True)
    ping_thread.start()
    
    # Run Flask app
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"Flask app starting on port {port}")
    print(f"Flask app starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False) 