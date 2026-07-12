# 🎮 Free Games Telegram Bot

> 🔴 **Live Example:** [@Lootigo](https://t.me/Lootigo) — Daily free games, DLCs and in-game items from Steam, Epic, Ubisoft, PlayStation, Xbox & Mobile

A fully automated bot that fetches free games and loot from **GamerPower** every 30 minutes and sends them to your Telegram channel — powered by **GitHub Actions** (100% free, no server needed).

---

## ✨ Features

- 🔄 Runs automatically every **30 minutes** via GitHub Actions
- 🎮 Fetches free **Games** and **DLC/Loot** separately
- 🔗 Resolves redirect links to get the **direct claim URL** (Steam, Epic, GOG, etc.)
- 🚫 **No duplicates** — seen posts are saved to the repo so nothing gets sent twice
- 💅 Supports **Telegram Premium animated emoji** in captions
- 🟢 **Green styled button** (Bot API 9.4) for Claim Now
- 🔒 All sensitive URLs and tokens stored as **GitHub Secrets**
- 💸 **Completely free** — no VPS, no hosting, no cost

---

## 🚀 Setup Guide

### Step 1 — Fork or create a repo

Click **Use this template** or fork this repo into your GitHub account.

---

### Step 2 — Create a Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` and follow the steps
3. Copy the **bot token** (looks like `123456789:ABCdefGHI...`)
4. Add your bot as **Admin** to your channel

---

### Step 3 — Get your Channel ID

1. Forward any message from your channel to **@userinfobot**
2. Copy the **Chat ID** (starts with `-100...`)

---

### Step 4 — Add GitHub Secrets

Go to your repo → **Settings → Secrets and variables → Actions → New repository secret**

Add these 4 secrets:

| Secret Name | Value |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Your bot token from BotFather |
| `TELEGRAM_CHAT_ID` | Your channel ID (e.g. `-1002394493903`) |
| `GAMERPOWER_GAME_URL` | `https://www.gamerpower.com/api/giveaways?type=game` |
| `GAMERPOWER_LOOT_URL` | `https://www.gamerpower.com/api/giveaways?type=loot` |

---

### Step 5 — Enable Actions

Go to the **Actions** tab in your repo and enable workflows if prompted.

---

### Step 6 — Test it

Go to **Actions → Free Games Bot → Run workflow → Run workflow**

Your channel should receive its first posts within seconds! 🎉

---

## 📁 File Structure

```
├── main.py                      # Main bot logic
├── seen_ids.json                # Auto-generated — tracks sent posts
└── .github/
    └── workflows/
        └── bot.yml              # GitHub Actions scheduler
```

---

## ⚙️ Customization

### Change the schedule
In `bot.yml`, edit the cron line:
```yaml
- cron: "*/30 * * * *"   # every 30 min
- cron: "0 * * * *"      # every hour
- cron: "0 */6 * * *"    # every 6 hours
```

### Change button color
In `main.py`, find `"style": "success"` and change to:
- `"success"` → 🟢 Green
- `"primary"` → 🔵 Blue
- `"danger"` → 🔴 Red

### Use your own Premium emoji
Replace the emoji IDs in `main.py` under the `# Emoji` section with your own custom emoji IDs.
To find an emoji ID, forward a premium emoji to **@RawDataBot**.

---

## 🔒 Privacy & Security

- Bot token and channel ID are stored as **encrypted GitHub Secrets** — never exposed in code
- API URLs are also stored as secrets so the repo reveals nothing sensitive
- `seen_ids.json` is committed automatically by the Actions bot after each run

---

## 📊 How It Works

```
GitHub Actions (every 30 min)
        ↓
Fetch free games from GamerPower API
        ↓
Filter out already-sent IDs (seen_ids.json)
        ↓
Resolve redirect → get direct claim URL
        ↓
Send photo + caption + button to Telegram channel
        ↓
Save updated seen_ids.json to repo
```

---

## 🙋 FAQ

**Q: Is this really free?**
Yes. GitHub Actions gives you 2,000 free minutes/month. This bot uses ~1 min per run × 48 runs/day = ~48 min/day, well within the free tier.

**Q: Will it send old giveaways when I first set it up?**
Yes — on the first run it has no history, so it will send everything currently active. After that, only new ones.

**Q: What if a giveaway has no redirect link?**
It falls back to the GamerPower page link automatically.

**Q: Can I use this for multiple channels?**
Fork the repo for each channel and set different secrets.

---

## 📜 License

MIT — free to use, modify, and distribute.
