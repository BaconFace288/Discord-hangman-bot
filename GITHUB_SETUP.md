# GitHub Upload Instructions for Discord Hangman Bot

## Step 1: Create a New GitHub Repository

1. Go to https://github.com/new in your web browser
2. Fill in the repository details:
   - **Repository name**: `discord-hangman-bot` (or your preferred name)
   - **Description**: `A fun Discord bot for playing hangman with 900+ words across 9 categories`
   - **Visibility**: Choose Public or Private
   - **DO NOT** check any of these boxes:
     - ❌ Add a README file
     - ❌ Add .gitignore
     - ❌ Choose a license
   (We already have these files in your local repository)

3. Click **"Create repository"**

## Step 2: Get Your Repository URL

After creating the repository, GitHub will show you a page with setup instructions. You'll see a URL that looks like:
```
https://github.com/YOUR_USERNAME/discord-hangman-bot.git
```

Copy this URL - you'll need it for the next step.

## Step 3: Push Your Code to GitHub

I've already initialized the git repository and made the initial commit. 

Now you just need to run these commands (replace `YOUR_GITHUB_URL` with the URL you copied):

```bash
cd C:\Users\Juniors\Desktop\SoftwareDevelopment\discord-hangman-bot
git remote add origin YOUR_GITHUB_URL
git branch -M main
git push -u origin main
```

**Example** (replace with your actual URL):
```bash
git remote add origin https://github.com/YourUsername/discord-hangman-bot.git
git branch -M main
git push -u origin main
```

You may be prompted to authenticate with GitHub. Use your GitHub credentials.

## Step 4: Deploy on Railway

Once your code is on GitHub:

1. Go to https://railway.app
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your `discord-hangman-bot` repository
5. Railway will automatically detect the `Procfile` and `requirements.txt`
6. Add your environment variable:
   - Click on your project
   - Go to **"Variables"** tab
   - Add: `DISCORD_BOT_TOKEN` = `your_actual_bot_token`
7. Click **"Deploy"**

Railway will automatically:
- Install Python dependencies from `requirements.txt`
- Use the `Procfile` to run your bot
- Keep your bot running 24/7

## Step 5: Verify Deployment

Check the Railway logs to see:
```
🎮 [YourBotName] is now online!
📊 Connected to X servers
```

Your bot should now be live in your Discord server!

---

## Quick Reference

**Local Git Status:**
✅ Git repository initialized
✅ All files added and committed
✅ Ready to push to GitHub

**Files in Repository:**
- bot.py (main bot file)
- game.py (game logic)
- words.json (900+ words across 9 categories)
- requirements.txt (dependencies)
- Procfile (Railway deployment config)
- README.md (documentation)
- .gitignore (git configuration)
- .env.example (environment template)

**Total:** 8 files, 2036 lines of code

---

## Need Help?

Let me know once you've created the GitHub repository and I can help you with the push commands!
