import logging
from pyromod import listen
from pyrogram import Client, idle
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    """Main function to run the bot"""
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
        
        # Initialize Pyrogram client
        bot = Client(
            "render_bot_session_new",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="StringSessionBot"),
        )
        
        logger.info("Bot client initialized, starting...")
        print("Bot client initialized, starting...")
        
        # Start the bot
        bot.start()
        
        # Get bot info
        me = bot.get_me()
        logger.info(f"@{me.username} Started Successfully!")
        print(f"@{me.username} Started Successfully!")
        print("Bot is running! Press Ctrl+C to stop.")
        
        # Keep the bot running
        idle()
        
    except (ApiIdInvalid, ApiIdPublishedFlood) as e:
        logger.error(f"API Error: {e}")
        print("Your API_ID/API_HASH is not valid.")
    except AccessTokenInvalid as e:
        logger.error(f"Token Error: {e}")
        print("Your BOT_TOKEN is not valid.")
    except Exception as e:
        logger.error(f"Bot error: {e}")
        print(f"Bot error: {e}")
    finally:
        if 'bot' in locals():
            try:
                bot.stop()
            except:
                pass
        logger.info("Bot stopped.")
        print("Bot stopped.")

if __name__ == "__main__":
    main() 