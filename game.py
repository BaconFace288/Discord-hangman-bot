"""
Hangman game logic for Discord bot.
"""

import random
import json
from typing import List, Set, Optional


class HangmanGame:
    """Represents a single hangman game instance."""
    
    # ASCII art for hangman stages (0 = start, 6 = game over)
    HANGMAN_STAGES = [
        # Stage 0 - Empty
        """
        ┌─────┐
        │     
        │     
        │     
        │     
        │     
        └─────
        """,
        # Stage 1 - Head
        """
        ┌─────┐
        │     │
        │     O
        │     
        │     
        │     
        └─────
        """,
        # Stage 2 - Body
        """
        ┌─────┐
        │     │
        │     O
        │     │
        │     
        │     
        └─────
        """,
        # Stage 3 - Left arm
        """
        ┌─────┐
        │     │
        │     O
        │    ╱│
        │     
        │     
        └─────
        """,
        # Stage 4 - Right arm
        """
        ┌─────┐
        │     │
        │     O
        │    ╱│╲
        │     
        │     
        └─────
        """,
        # Stage 5 - Left leg
        """
        ┌─────┐
        │     │
        │     O
        │    ╱│╲
        │    ╱ 
        │     
        └─────
        """,
        # Stage 6 - Right leg (Game Over)
        """
        ┌─────┐
        │     │
        │     O
        │    ╱│╲
        │    ╱ ╲
        │     
        └─────
        """
    ]
    
    MAX_WRONG_GUESSES = 6
    
    def __init__(self, word: str, category: str, difficulty: str, endless_mode: bool = False):
        """
        Initialize a new hangman game.
        
        Args:
            word: The word to guess
            category: The category of the word
            difficulty: The difficulty level
            endless_mode: Whether this is an endless mode game
        """
        self.word = word.upper()
        self.category = category
        self.difficulty = difficulty
        self.guessed_letters: Set[str] = set()
        self.wrong_guesses: Set[str] = set()
        self.is_over = False
        self.is_won = False
        self.endless_mode = endless_mode
        self.wins = 0
        self.losses = 0
        
    @property
    def wrong_guess_count(self) -> int:
        """Get the number of wrong guesses."""
        return len(self.wrong_guesses)
    
    @property
    def remaining_attempts(self) -> int:
        """Get the number of remaining attempts."""
        return self.MAX_WRONG_GUESSES - self.wrong_guess_count
    
    def get_display_word(self) -> str:
        """
        Get the word with unguessed letters replaced by underscores.
        
        Returns:
            The display version of the word
        """
        display = []
        for char in self.word:
            if char == ' ':
                display.append('  ')  # Double space for word breaks
            elif char.isalpha():
                if char in self.guessed_letters:
                    display.append(char)
                else:
                    display.append('_')
            else:
                # Handle special characters (hyphens, apostrophes, etc.)
                display.append(char)
        return ' '.join(display)
    
    def get_hangman_art(self) -> str:
        """
        Get the current hangman ASCII art based on wrong guesses.
        
        Returns:
            ASCII art string
        """
        stage = min(self.wrong_guess_count, len(self.HANGMAN_STAGES) - 1)
        return self.HANGMAN_STAGES[stage]
    
    def guess_letter(self, letter: str) -> dict:
        """
        Process a letter guess.
        
        Args:
            letter: The letter to guess (should be single character)
            
        Returns:
            Dictionary with result information
        """
        letter = letter.upper()
        
        # Validate input
        if len(letter) != 1 or not letter.isalpha():
            return {
                'valid': False,
                'message': '❌ Please guess a single letter.',
                'game_over': False
            }
        
        # Check if already guessed
        if letter in self.guessed_letters or letter in self.wrong_guesses:
            return {
                'valid': False,
                'message': f'❌ You already guessed **{letter}**!',
                'game_over': False
            }
        
        # Process the guess
        if letter in self.word:
            self.guessed_letters.add(letter)
            
            # Check for win
            if self._check_win():
                self.is_over = True
                self.is_won = True
                return {
                    'valid': True,
                    'correct': True,
                    'message': f'✅ **{letter}** is in the word!',
                    'game_over': True,
                    'won': True
                }
            
            return {
                'valid': True,
                'correct': True,
                'message': f'✅ **{letter}** is in the word!',
                'game_over': False
            }
        else:
            self.wrong_guesses.add(letter)
            
            # Check for loss
            if self.wrong_guess_count >= self.MAX_WRONG_GUESSES:
                self.is_over = True
                return {
                    'valid': True,
                    'correct': False,
                    'message': f'❌ **{letter}** is not in the word.',
                    'game_over': True,
                    'won': False
                }
            
            return {
                'valid': True,
                'correct': False,
                'message': f'❌ **{letter}** is not in the word.',
                'game_over': False
            }
    
    def guess_word(self, word: str) -> dict:
        """
        Process a full word guess.
        
        Args:
            word: The word to guess
            
        Returns:
            Dictionary with result information
        """
        word = word.upper()
        
        if word == self.word:
            self.is_over = True
            self.is_won = True
            # Mark all letters as guessed for display
            for char in self.word:
                if char.isalpha():
                    self.guessed_letters.add(char)
            
            return {
                'valid': True,
                'correct': True,
                'message': '🎉 **Correct!** You solved the word!',
                'game_over': True,
                'won': True
            }
        else:
            # Wrong word guess counts as a wrong guess
            self.wrong_guesses.add('WORD')  # Placeholder to track word guesses
            
            if self.wrong_guess_count >= self.MAX_WRONG_GUESSES:
                self.is_over = True
                return {
                    'valid': True,
                    'correct': False,
                    'message': f'❌ **{word}** is not the correct word.',
                    'game_over': True,
                    'won': False
                }
            
            return {
                'valid': True,
                'correct': False,
                'message': f'❌ **{word}** is not the correct word.',
                'game_over': False
            }
    
    def _check_win(self) -> bool:
        """
        Check if the player has won.
        
        Returns:
            True if all letters have been guessed
        """
        for char in self.word:
            if char.isalpha() and char not in self.guessed_letters:
                return False
        return True
    
    def get_guessed_letters_display(self) -> str:
        """Get a formatted string of all guessed letters."""
        correct = sorted(list(self.guessed_letters))
        wrong = sorted([g for g in self.wrong_guesses if g != 'WORD'])
        
        result = []
        if correct:
            result.append(f"✅ Correct: {', '.join(correct)}")
        if wrong:
            result.append(f"❌ Wrong: {', '.join(wrong)}")
        
        return '\n'.join(result) if result else 'No guesses yet'
    
    def reset_for_new_round(self, word: str, category: str, difficulty: str):
        """Reset the game for a new round in endless mode."""
        self.word = word.upper()
        self.category = category
        self.difficulty = difficulty
        self.guessed_letters = set()
        self.wrong_guesses = set()
        self.is_over = False
        self.is_won = False
    
    def get_score_display(self) -> str:
        """Get formatted score for endless mode."""
        if self.endless_mode:
            total = self.wins + self.losses
            return f"🏆 Score: {self.wins} Wins | {self.losses} Losses | {total} Total"
        return ""


class WordDatabase:
    """Manages the word database for hangman."""
    
    def __init__(self, words_file: str = 'words.json'):
        """
        Initialize the word database.
        
        Args:
            words_file: Path to the JSON file containing words
        """
        self.words_file = words_file
        self.words_data = self._load_words()
    
    def _load_words(self) -> dict:
        """Load words from the JSON file."""
        try:
            with open(self.words_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Return default words if file doesn't exist
            return self._get_default_words()
    
    def _get_default_words(self) -> dict:
        """Get default words if no file is found."""
        return {
            "animals": {
                "easy": ["cat", "dog", "fish", "bird", "lion"],
                "medium": ["elephant", "giraffe", "penguin"],
                "hard": ["hippopotamus", "rhinoceros"]
            },
            "general": {
                "easy": ["house", "water", "book", "table"],
                "medium": ["computer", "keyboard", "mountain"],
                "hard": ["encyclopedia", "refrigerator"]
            }
        }
    
    def get_random_word(self, category: Optional[str] = None, 
                       difficulty: Optional[str] = None) -> tuple:
        """
        Get a random word from the database.
        
        Args:
            category: Optional category filter
            difficulty: Optional difficulty filter
            
        Returns:
            Tuple of (word, category, difficulty)
        """
        # If no category specified, choose random
        if category is None or category.lower() not in self.words_data:
            category = random.choice(list(self.words_data.keys()))
        else:
            category = category.lower()
        
        # If no difficulty specified, choose random
        if difficulty is None or difficulty.lower() not in self.words_data[category]:
            difficulty = random.choice(list(self.words_data[category].keys()))
        else:
            difficulty = difficulty.lower()
        
        # Get random word from the selected category and difficulty
        word = random.choice(self.words_data[category][difficulty])
        
        return word, category, difficulty
    
    def get_categories(self) -> List[str]:
        """Get list of available categories."""
        return list(self.words_data.keys())
    
    def get_difficulties(self) -> List[str]:
        """Get list of available difficulties."""
        # Assume all categories have the same difficulties
        if self.words_data:
            first_category = next(iter(self.words_data.values()))
            return list(first_category.keys())
        return []
