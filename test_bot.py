import os
import Config
import logging
import threading
import time
import requests
import asyncio
from pyromod import listen
from pyrogram import Client, idle
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid
from flask import Flask, jsonify

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

def autoping():
    """Function to ping the app to keep it alive"""
    while True:
        try:
            # Ping the app itself using the actual Render URL
            response = requests.get("https://stringsession-1c37.onrender.com/ping", timeout=10)
            if response.status_code == 200:
                logger.info(f"Autoping successful: {response.status_code}")
                print(f"Autoping successful: {response.status_code}")
            else:
                logger.warning(f"Autoping response: {response.status_code}")
                print(f"Autoping response: {response.status_code}")
        except Exception as e:
            logger.error(f"Autoping error: {e}")
            print(f"Autoping error: {e}")
        time.sleep(300)  # Ping every 5 minutes

def run_flask():
    """Function to run the Flask app"""
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"Flask app starting on port {port}")
    print(f"Flask app starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)

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

def test_bot():
    """Test the bot locally with Flask and ping"""
    global bot_running, bot_client
    
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            logger.info(f"Starting bot with Flask and ping functionality... (Attempt {retry_count + 1}/{max_retries})")
            print(f"Starting bot with Flask and ping functionality... (Attempt {retry_count + 1}/{max_retries})")
            
            logger.info(f"API_ID: {Config.API_ID}")
            logger.info(f"API_HASH: {Config.API_HASH[:10]}...")
            logger.info(f"BOT_TOKEN: {Config.BOT_TOKEN[:20]}...")
            
            # Clean up old session file if it exists
            session_file = "test_session_new.session"
            if os.path.exists(session_file):
                try:
                    os.remove(session_file)
                    logger.info("Removed old session file")
                    print("Removed old session file")
                except Exception as e:
                    logger.warning(f"Could not remove old session file: {e}")
            
            # Initialize Pyrogram client with a unique session name
            bot_client = Client(
                "test_session_new",
                api_id=Config.API_ID,
                api_hash=Config.API_HASH,
                bot_token=Config.BOT_TOKEN,
                plugins=dict(root="StringSessionBot"),
                # Add time sync settings
                sleep_threshold=30,
            )
            
            logger.info("Bot client initialized, starting...")
            bot_client.start()
            bot_running = True
            
            # Get bot info
            me = bot_client.get_me()
            logger.info(f"@{me.username} Started Successfully!")
            print(f"@{me.username} Started Successfully!")
            print("Bot is running! Press Ctrl+C to stop.")
            
            # Keep the bot running
            idle()
            break  # If we reach here, bot ran successfully
            
        except (ApiIdInvalid, ApiIdPublishedFlood) as e:
            logger.error(f"API Error: {e}")
            print("Your API_ID/API_HASH is not valid.")
            bot_running = False
            break  # Don't retry for API errors
        except AccessTokenInvalid as e:
            logger.error(f"Token Error: {e}")
            print("Your BOT_TOKEN is not valid.")
            bot_running = False
            break  # Don't retry for token errors
        except Exception as e:
            logger.error(f"Bot error: {e}")
            print(f"Bot error: {e}")
            # If it's a time sync error, try to clean up and restart
            if "msg_id too low" in str(e) or "time has to be synchronized" in str(e):
                logger.info("Time sync error detected. Cleaning up session...")
                print("Time sync error detected. Cleaning up session...")
                # Clean up session file
                session_file = "test_session_new.session"
                if os.path.exists(session_file):
                    try:
                        os.remove(session_file)
                        logger.info("Removed corrupted session file")
                        print("Removed corrupted session file")
                    except:
                        pass
                retry_count += 1
                if retry_count < max_retries:
                    logger.info(f"Retrying in 5 seconds... (Attempt {retry_count + 1}/{max_retries})")
                    print(f"Retrying in 5 seconds... (Attempt {retry_count + 1}/{max_retries})")
                    time.sleep(5)
                    continue
            bot_running = False
            break
        finally:
            if bot_client:
                try:
                    bot_client.stop()
                except:
                    pass
            logger.info("Bot stopped.")
            print("Bot stopped.")
    
    if retry_count >= max_retries:
        logger.error("Max retries reached. Bot failed to start.")
        print("Max retries reached. Bot failed to start.")

if __name__ == "__main__":
    logger.info("Starting bot in main thread, Flask and ping in background threads...")
    print("Starting bot in main thread, Flask and ping in background threads...")

    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Start autoping in a separate thread
    ping_thread = threading.Thread(target=autoping, daemon=True)
    ping_thread.start()

    # Run the bot in the main thread (this will block until the bot stops)
    test_bot() 