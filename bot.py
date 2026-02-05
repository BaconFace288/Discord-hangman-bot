"""
Discord Hangman Bot - A fun hangman game for Discord servers.
"""

import os
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from game import HangmanGame, WordDatabase
from typing import Dict

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Bot setup with command prefix
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Store active games per channel
active_games: Dict[int, HangmanGame] = {}

# Word database
word_db = WordDatabase('words.json')


@bot.event
async def on_ready():
    """Event handler for when the bot is ready."""
    print(f'🎮 {bot.user} is now online!')
    print(f'📊 Connected to {len(bot.guilds)} servers')
    print('─' * 40)


def create_game_embed(game: HangmanGame, title: str = "Hangman Game", 
                     description: str = "", color: discord.Color = discord.Color.blue()) -> discord.Embed:
    """
    Create a formatted embed for the game state.
    
    Args:
        game: The hangman game instance
        title: Embed title
        description: Embed description
        color: Embed color
        
    Returns:
        Discord embed object
    """
    embed = discord.Embed(title=title, description=description, color=color)
    
    # Add hangman art
    embed.add_field(
        name="Hangman",
        value=f"```{game.get_hangman_art()}```",
        inline=False
    )
    
    # Add word display
    embed.add_field(
        name="Word",
        value=f"```{game.get_display_word()}```",
        inline=False
    )
    
    # Add game info
    info = f"**Category:** {game.category.title()}\n"
    info += f"**Difficulty:** {game.difficulty.title()}\n"
    info += f"**Remaining Attempts:** {game.remaining_attempts}/{game.MAX_WRONG_GUESSES}"
    embed.add_field(name="Game Info", value=info, inline=True)
    
    # Add guessed letters
    embed.add_field(
        name="Guessed Letters",
        value=game.get_guessed_letters_display(),
        inline=True
    )
    
    # Add footer with helpful tips
    if not game.is_over:
        embed.set_footer(text="Use !guess <letter> to guess a letter or !solve <word> to solve")
    
    return embed


@bot.command(name='hangman', aliases=['hm', 'start'])
async def start_game(ctx, category: str = None, difficulty: str = None):
    """
    Start a new hangman game.
    
    Usage:
        !hangman - Start with random category and difficulty
        !hangman animals - Start with animals category, random difficulty
        !hangman animals easy - Start with animals category, easy difficulty
    """
    channel_id = ctx.channel.id
    
    # Check if game already exists in this channel
    if channel_id in active_games and not active_games[channel_id].is_over:
        await ctx.send("❌ A game is already in progress in this channel! Use `!quit` to end it.")
        return
    
    # Validate category
    if category and category.lower() not in word_db.get_categories():
        available = ', '.join(word_db.get_categories())
        await ctx.send(f"❌ Invalid category! Available categories: **{available}**")
        return
    
    # Validate difficulty
    if difficulty and difficulty.lower() not in word_db.get_difficulties():
        available = ', '.join(word_db.get_difficulties())
        await ctx.send(f"❌ Invalid difficulty! Available difficulties: **{available}**")
        return
    
    # Get random word
    word, selected_category, selected_difficulty = word_db.get_random_word(category, difficulty)
    
    # Create new game
    game = HangmanGame(word, selected_category, selected_difficulty)
    active_games[channel_id] = game
    
    # Send game start message
    embed = create_game_embed(
        game,
        title="🎮 Hangman Game Started!",
        description=f"Started by {ctx.author.mention}\nGuess the word letter by letter!",
        color=discord.Color.green()
    )
    
    await ctx.send(embed=embed)


@bot.command(name='endless', aliases=['infinity', 'marathon'])
async def start_endless_mode(ctx, difficulty: str = None):
    """
    Start an endless mode game that cycles through all categories.
    
    Usage:
        !endless - Start endless mode with random difficulties
        !endless easy - Start endless mode with only easy words
        !endless hard - Start endless mode with only hard words
    """
    channel_id = ctx.channel.id
    
    # Check if game already exists in this channel
    if channel_id in active_games and not active_games[channel_id].is_over:
        await ctx.send("❌ A game is already in progress in this channel! Use `!quit` to end it.")
        return
    
    # Validate difficulty if provided
    if difficulty and difficulty.lower() not in word_db.get_difficulties():
        available = ', '.join(word_db.get_difficulties())
        await ctx.send(f"❌ Invalid difficulty! Available difficulties: **{available}**")
        return
    
    # Get random word from any category
    word, selected_category, selected_difficulty = word_db.get_random_word(None, difficulty)
    
    # Create new game in endless mode
    game = HangmanGame(word, selected_category, selected_difficulty, endless_mode=True)
    active_games[channel_id] = game
    
    # Send game start message
    embed = create_game_embed(
        game,
        title="♾️ Endless Mode Started!",
        description=f"Started by {ctx.author.mention}\nGuess words from all categories!\nThe game continues until you quit.\n\n{game.get_score_display()}",
        color=discord.Color.purple()
    )
    
    await ctx.send(embed=embed)



@bot.command(name='guess', aliases=['g'])
async def guess_letter(ctx, letter: str = None):
    """
    Guess a letter in the current game.
    
    Usage:
        !guess a
        !g e
    """
    channel_id = ctx.channel.id
    
    # Check if game exists
    if channel_id not in active_games:
        await ctx.send("❌ No active game in this channel! Use `!hangman` to start a new game.")
        return
    
    game = active_games[channel_id]
    
    # Check if game is over
    if game.is_over:
        await ctx.send("❌ This game has ended! Use `!hangman` to start a new game.")
        return
    
    # Check if letter provided
    if letter is None:
        await ctx.send("❌ Please provide a letter to guess! Usage: `!guess <letter>`")
        return
    
    # Process the guess
    result = game.guess_letter(letter)
    
    if not result['valid']:
        await ctx.send(result['message'])
        return
    
    # Determine embed color based on result
    if result['game_over']:
        if result['won']:
            color = discord.Color.gold()
            title = "🎉 You Won!"
            description = f"{ctx.author.mention} correctly guessed the word!"
            if game.endless_mode:
                game.wins += 1
        else:
            color = discord.Color.red()
            title = "💀 Game Over!"
            description = f"The word was: **{game.word}**"
            if game.endless_mode:
                game.losses += 1
    else:
        color = discord.Color.green() if result['correct'] else discord.Color.orange()
        title = "Hangman Game"
        description = result['message']
    
    # Send updated game state
    embed = create_game_embed(game, title=title, description=description, color=color)
    await ctx.send(embed=embed)
    
    # Handle game over
    if result['game_over']:
        if game.endless_mode:
            # Continue to next round
            await ctx.send(f"**🔄 Next round starting in 3 seconds...**\\n{game.get_score_display()}")
            await asyncio.sleep(3)
            
            # Get new word
            word, category, difficulty = word_db.get_random_word()
            game.reset_for_new_round(word, category, difficulty)
            
            # Send new game embed
            embed = create_game_embed(
                game,
                title="🎮 Next Round!",
                description=f"New word from **{category.title()}** category!\\n{game.get_score_display()}",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
        else:
            # Clean up if not endless mode
            del active_games[channel_id]


@bot.command(name='solve', aliases=['word'])
async def solve_word(ctx, *, word: str = None):
    """
    Attempt to solve the word.
    
    Usage:
        !solve elephant
        !word computer
    """
    channel_id = ctx.channel.id
    
    # Check if game exists
    if channel_id not in active_games:
        await ctx.send("❌ No active game in this channel! Use `!hangman` to start a new game.")
        return
    
    game = active_games[channel_id]
    
    # Check if game is over
    if game.is_over:
        await ctx.send("❌ This game has ended! Use `!hangman` to start a new game.")
        return
    
    # Check if word provided
    if word is None:
        await ctx.send("❌ Please provide a word to guess! Usage: `!solve <word>`")
        return
    
    # Process the word guess
    result = game.guess_word(word)
    
    # Determine embed color based on result
    if result['game_over']:
        if result['won']:
            color = discord.Color.gold()
            title = "🎉 You Won!"
            description = f"{ctx.author.mention} correctly solved the word!"
            if game.endless_mode:
                game.wins += 1
        else:
            color = discord.Color.red()
            title = "💀 Game Over!"
            description = f"The word was: **{game.word}**"
            if game.endless_mode:
                game.losses += 1
    else:
        color = discord.Color.orange()
        title = "Hangman Game"
        description = result['message']
    
    # Send updated game state
    embed = create_game_embed(game, title=title, description=description, color=color)
    await ctx.send(embed=embed)
    
    # Handle game over
    if result['game_over']:
        if game.endless_mode:
            # Continue to next round
            await ctx.send(f"**🔄 Next round starting in 3 seconds...**\n{game.get_score_display()}")
            await asyncio.sleep(3)
            
            # Get new word
            word, category, difficulty = word_db.get_random_word()
            game.reset_for_new_round(word, category, difficulty)
            
            # Send new game embed
            embed = create_game_embed(
                game,
                title="🎮 Next Round!",
                description=f"New word from **{category.title()}** category!\n{game.get_score_display()}",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
        else:
            # Clean up if not endless mode
            del active_games[channel_id]


@bot.command(name='quit', aliases=['end', 'stop'])
async def quit_game(ctx):
    """
    Quit the current game.
    
    Usage:
        !quit
    """
    channel_id = ctx.channel.id
    
    # Check if game exists
    if channel_id not in active_games:
        await ctx.send("❌ No active game in this channel!")
        return
    
    game = active_games[channel_id]
    
    # Create final embed showing the word
    description = f"{ctx.author.mention} ended the game.\nThe word was: **{game.word}**"
    if game.endless_mode:
        description += f"\n\n{game.get_score_display()}"
    
    embed = discord.Embed(
        title="🏳️ Game Ended",
        description=description,
        color=discord.Color.light_gray()
    )
    
    await ctx.send(embed=embed)
    del active_games[channel_id]


@bot.command(name='hint')
async def get_hint(ctx):
    """
    Get a hint about the current word.
    
    Usage:
        !hint
    """
    channel_id = ctx.channel.id
    
    # Check if game exists
    if channel_id not in active_games:
        await ctx.send("❌ No active game in this channel! Use `!hangman` to start a new game.")
        return
    
    game = active_games[channel_id]
    
    # Check if game is over
    if game.is_over:
        await ctx.send("❌ This game has ended! Use `!hangman` to start a new game.")
        return
    
    # Provide hint
    hint_embed = discord.Embed(
        title="💡 Hint",
        description=f"**Category:** {game.category.title()}\n**Difficulty:** {game.difficulty.title()}\n**Word Length:** {len([c for c in game.word if c.isalpha()])} letters",
        color=discord.Color.purple()
    )
    
    await ctx.send(embed=hint_embed)


@bot.command(name='categories', aliases=['cats'])
async def list_categories(ctx):
    """
    List all available categories.
    
    Usage:
        !categories
    """
    categories = word_db.get_categories()
    
    embed = discord.Embed(
        title="📚 Available Categories",
        description="\n".join([f"• {cat.title()}" for cat in categories]),
        color=discord.Color.blue()
    )
    
    embed.set_footer(text="Use !hangman <category> to start a game with a specific category")
    
    await ctx.send(embed=embed)


@bot.command(name='help', aliases=['h', 'commands'])
async def show_help(ctx):
    """
    Show help information.
    
    Usage:
        !help
    """
    embed = discord.Embed(
        title="🎮 Hangman Bot - Commands",
        description="Play hangman with your friends in Discord!",
        color=discord.Color.blue()
    )
    
    # Game commands
    embed.add_field(
        name="🎯 Game Commands",
        value=(
            "`!hangman [category] [difficulty]` - Start a new game\n"
            "`!endless [difficulty]` - Start endless mode (all categories)\n"
            "`!guess <letter>` - Guess a letter\n"
            "`!solve <word>` - Attempt to solve the word\n"
            "`!hint` - Get a hint about the word\n"
            "`!quit` - End the current game"
        ),
        inline=False
    )
    
    # Info commands
    embed.add_field(
        name="ℹ️ Info Commands",
        value=(
            "`!categories` - List all available categories\n"
            "`!help` - Show this help message"
        ),
        inline=False
    )
    
    # Examples
    embed.add_field(
        name="📖 Examples",
        value=(
            "`!hangman` - Random category and difficulty\n"
            "`!hangman animals` - Animals category, random difficulty\n"
            "`!hangman movies hard` - Hard movies\n"
            "`!guess e` - Guess the letter 'e'\n"
            "`!solve elephant` - Try to solve with 'elephant'"
        ),
        inline=False
    )
    
    # Available options
    categories = ', '.join(word_db.get_categories())
    difficulties = ', '.join(word_db.get_difficulties())
    
    embed.add_field(
        name="🎲 Available Options",
        value=f"**Categories:** {categories}\n**Difficulties:** {difficulties}",
        inline=False
    )
    
    embed.set_footer(text="Have fun playing Hangman! 🎉")
    
    await ctx.send(embed=embed)


# Error handling
@bot.event
async def on_command_error(ctx, error):
    """Handle command errors."""
    if isinstance(error, commands.CommandNotFound):
        return  # Ignore unknown commands
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing required argument. Use `!help` for command usage.")
    else:
        print(f"Error: {error}")
        await ctx.send(f"❌ An error occurred. Please try again.")


# Run the bot
if __name__ == '__main__':
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ Error: DISCORD_BOT_TOKEN not found in environment variables!")
        print("Please create a .env file with your bot token.")
