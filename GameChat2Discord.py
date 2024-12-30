import discord
from discord.ext import commands
import pytesseract
import pyautogui
import PIL.ImageGrab
import numpy as np
import time
import asyncio
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('ScreenChatBridge')

# Bot Configuration
DISCORD_TOKEN = 'your_discord_token_here'
DISCORD_CHANNEL_ID = 123456789  # Replace with your channel ID

# Screen region to monitor (left, top, right, bottom)
# You'll need to adjust these coordinates for your screen
CHAT_REGION = (100, 100, 400, 600)  

# Game window configuration
CHAT_INPUT_CLICK_POS = (200, 580)  # Position to click before typing
TYPING_DELAY = 0.05  # Delay between keystrokes

class ChatBridgeBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
        
        # Store last seen text to detect changes
        self.last_text = ''
        self.monitoring = False
        self.chat_channel = None
        
    async def setup_hook(self):
        # Start the screen monitoring loop
        self.bg_task = self.loop.create_task(self.monitor_screen())
        
    def get_screen_text(self) -> str:
        """Capture and OCR the specified screen region"""
        try:
            # Capture the specified region of the screen
            screenshot = PIL.ImageGrab.grab(bbox=CHAT_REGION)
            
            # Convert to grayscale for better OCR
            screenshot = screenshot.convert('L')
            
            # Use Tesseract to extract text
            text = pytesseract.image_to_string(screenshot)
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error capturing screen: {e}")
            return ''
            
    async def monitor_screen(self):
        """Continuously monitor screen for changes"""
        await self.wait_until_ready()
        self.chat_channel = self.get_channel(DISCORD_CHANNEL_ID)
        
        if not self.chat_channel:
            logger.error("Could not find specified Discord channel!")
            return
            
        self.monitoring = True
        
        while self.monitoring:
            try:
                current_text = self.get_screen_text()
                
                # If text has changed
                if current_text and current_text != self.last_text:
                    # Find new lines by comparing with last text
                    new_lines = self.get_new_lines(current_text)
                    
                    # Send new lines to Discord
                    for line in new_lines:
                        if line.strip():
                            await self.chat_channel.send(f"**Game Chat**: {line.strip()}")
                    
                    self.last_text = current_text
                
                # Wait before next capture
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Error in monitor loop: {e}")
                await asyncio.sleep(5)
                
    def get_new_lines(self, current_text: str) -> list:
        """Compare current text with last text to find new lines"""
        if not self.last_text:
            return [current_text]
            
        current_lines = current_text.splitlines()
        last_lines = self.last_text.splitlines()
        
        # Find lines that are in current but not in last
        return [line for line in current_lines if line not in last_lines]
        
    def type_message(self, message: str):
        """Type a message into the game chat"""
        try:
            # Click the chat input position
            pyautogui.click(CHAT_INPUT_CLICK_POS)
            time.sleep(0.5)  # Wait for click to register
            
            # Type the message
            pyautogui.write(message, interval=TYPING_DELAY)
            pyautogui.press('enter')
            
        except Exception as e:
            logger.error(f"Error typing message: {e}")

bot = ChatBridgeBot()

@bot.event
async def on_ready():
    logger.info(f'Bot connected as {bot.user}')

@bot.command(name='msg')
async def send_message(ctx, *, message: str):
    """Send a message to the game chat"""
    if ctx.channel.id != DISCORD_CHANNEL_ID:
        return
        
    try:
        # Notify Discord that message is being sent
        await ctx.send(f"Sending message: {message}")
        
        # Type the message in game
        bot.type_message(message)
        
    except Exception as e:
        await ctx.send(f"Error sending message: {e}")

def main():
    """Run the bot"""
    try:
        # Ensure Tesseract is installed and configured
        pytesseract.get_tesseract_version()
        
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"Error running bot: {e}")

if __name__ == "__main__":
    main()
