import Config
import logging
from pyromod import listen
from pyrogram import Client, idle
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def test_bot():
    """Test the bot locally"""
    try:
        logger.info("Testing bot locally...")
        logger.info(f"API_ID: {Config.API_ID}")
        logger.info(f"API_HASH: {Config.API_HASH[:10]}...")
        logger.info(f"BOT_TOKEN: {Config.BOT_TOKEN[:20]}...")
        
        # Initialize Pyrogram client with a unique session name
        bot = Client(
            "test_session",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins=dict(root="StringSessionBot"),
        )
        
        logger.info("Bot client initialized, starting...")
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
    test_bot() 