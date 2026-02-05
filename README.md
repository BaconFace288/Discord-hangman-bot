# 🎮 Discord Hangman Bot

A feature-rich Discord bot that lets you play the classic hangman game right in your Discord server! Challenge your friends to guess words across multiple categories and difficulty levels.

## ✨ Features

- 🎯 **Multiple Categories**: Animals, Countries, Movies, Programming, Food, and General
- 📊 **Three Difficulty Levels**: Easy, Medium, and Hard
- 🎨 **ASCII Art**: Beautiful hangman visualizations that update with each wrong guess
- 🎮 **Rich Discord Embeds**: Clean, colorful game displays
- 💬 **Multiple Commands**: Full set of commands for gameplay
- 🔄 **Per-Channel Games**: Each channel can have its own independent game

## 📋 Commands

| Command | Aliases | Description | Example |
|---------|---------|-------------|---------|
| `!hangman [category] [difficulty]` | `!hm`, `!start` | Start a new game | `!hangman animals easy` |
| `!guess <letter>` | `!g` | Guess a single letter | `!guess e` |
| `!solve <word>` | `!word` | Attempt to solve the word | `!solve elephant` |
| `!hint` | - | Get a hint about the word | `!hint` |
| `!quit` | `!end`, `!stop` | End the current game | `!quit` |
| `!categories` | `!cats` | List all categories | `!categories` |
| `!help` | `!h`, `!commands` | Show help information | `!help` |

## 🎲 Available Options

### Categories
- **animals** - Various animals from cats to hippopotamus
- **countries** - Countries from around the world
- **movies** - Popular movies and films
- **programming** - Programming terms and concepts
- **food** - Different types of food and dishes
- **general** - Common everyday words

### Difficulty Levels
- **easy** - 4-6 letter words
- **medium** - 7-9 letter words
- **hard** - 10+ letter words

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- A Discord account
- A Discord Bot Token

### Step 1: Create a Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Under the bot's username, click "Reset Token" and copy your bot token
5. Enable the following Privileged Gateway Intents:
   - Message Content Intent
6. Go to the "OAuth2" > "URL Generator" section
7. Select the following scopes:
   - `bot`
8. Select the following bot permissions:
   - Send Messages
   - Embed Links
   - Read Message History
   - Use Slash Commands (optional for future)
9. Copy the generated URL and open it in your browser to invite the bot to your server

### Step 2: Install the Bot

1. Clone or download this repository
2. Navigate to the project directory:
   ```bash
   cd discord-hangman-bot
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```

5. Open the `.env` file and add your bot token:
   ```
   DISCORD_BOT_TOKEN=your_actual_bot_token_here
   ```

### Step 3: Run the Bot

```bash
python bot.py
```

You should see a message indicating the bot is online!

## 🎯 How to Play

1. Start a game in any text channel:
   ```
   !hangman
   ```
   Or specify a category and difficulty:
   ```
   !hangman animals hard
   ```

2. Guess letters one at a time:
   ```
   !guess e
   ```

3. Think you know the word? Try to solve it:
   ```
   !solve elephant
   ```

4. Need help? Get a hint:
   ```
   !hint
   ```

5. Want to give up? Quit the game:
   ```
   !quit
   ```

## 🎨 Game Rules

- You have **6 wrong guesses** before the game is over
- Correctly guessed letters will be revealed in the word
- Wrong guesses will add to the hangman drawing
- Each wrong full-word guess counts as one mistake
- Only one game can be active per channel at a time

## 📁 Project Structure

```
discord-hangman-bot/
├── bot.py              # Main bot file with Discord commands
├── game.py             # Hangman game logic and word database
├── words.json          # Word database organized by category/difficulty
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── .gitignore         # Git ignore file
└── README.md          # This file
```

## 🔧 Customization

### Adding New Words

Edit the `words.json` file to add new words to existing categories or create new categories:

```json
{
  "your_category": {
    "easy": ["word1", "word2"],
    "medium": ["longerword1", "longerword2"],
    "hard": ["verylongword1", "verylongword2"]
  }
}
```

### Changing the Command Prefix

Edit `bot.py` and change the prefix in the bot initialization:

```python
bot = commands.Bot(command_prefix='!', intents=intents)
```

### Adjusting Max Wrong Guesses

Edit `game.py` and change the `MAX_WRONG_GUESSES` constant in the `HangmanGame` class:

```python
MAX_WRONG_GUESSES = 6  # Change this value
```

## 🚀 Deployment

For 24/7 hosting, you can deploy this bot to platforms like:

- **Railway** - [railway.app](https://railway.app)
- **Heroku** - [heroku.com](https://heroku.com)
- **Replit** - [replit.com](https://replit.com)
- **Google Cloud** - [cloud.google.com](https://cloud.google.com)

### Railway Deployment

1. Create a `Procfile` in the project root:
   ```
   worker: python bot.py
   ```

2. Push your code to GitHub

3. Go to [Railway](https://railway.app) and create a new project from your GitHub repo

4. Add your `DISCORD_BOT_TOKEN` as an environment variable in Railway

5. Deploy!

## 🤝 Contributing

Feel free to fork this project and add your own features! Some ideas:
- Score tracking and leaderboards
- Timed games
- Multiplayer modes
- Custom word lists per server
- Slash commands support

## 📝 License

This project is open source and available for personal and educational use.

## 🎉 Credits

Created with ❤️ using discord.py

---

**Have fun playing Hangman!** 🎮
