# GameChat2Discord (ScreenChatBridgeBot)

A Discord bot that bridges game chat with Discord by monitoring screen regions and simulating keyboard input.

## Features

- 🔍 Screen monitoring with OCR to detect game chat
- 💬 Automatic forwarding of game chat to Discord
- ⌨️ Send messages from Discord to game chat using `!msg` command
- 🎮 No game modifications required - works with any game

## Prerequisites

- Python 3.7+
- Tesseract OCR
- Discord Bot Token

## Quick Start

1. **Install Python packages**:
```sh
pip install discord.py pytesseract pillow pyautogui numpy
```

2. **Install Tesseract OCR**:
- Windows: Download installer from [here](https://github.com/UB-Mannheim/tesseract/wiki)
- Linux: `sudo apt-get install tesseract-ocr`
- Mac: `brew install tesseract`

3. **Configuration**:
Create `config.py`:
```python
DISCORD_TOKEN = 'your_discord_token_here'
DISCORD_CHANNEL_ID = 123456789  # Your channel ID
CHAT_REGION = (100, 100, 400, 600)  # Screen region to monitor
CHAT_INPUT_CLICK_POS = (200, 580)  # Where to click to type
```

4. **Run the bot**:
```sh
python bot.py
```

## Usage

### Finding Screen Coordinates

Run this script and hover over important screen positions:
```python
import pyautogui
while True:
    print(pyautogui.position())
```

### Discord Commands

- Send message to game: `!msg <your message>`
- Example: `!msg Hello from Discord!`

## Troubleshooting

- **Messages not being detected**: Adjust `CHAT_REGION` coordinates
- **Bot not responding**: Check Discord token and permissions
- **Typing in wrong place**: Update `CHAT_INPUT_CLICK_POS`

## Support

Having issues? [Open an issue](https://github.com/kozaworld/ScreenChatBridgeBot/issues/new)

## License

MIT License - see LICENSE file

## Author

👤 **kozaworld**

* GitHub: [@kozaworld](https://github.com/kozaworld)
