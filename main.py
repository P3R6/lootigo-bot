import os
import json
import time
import requests

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID   = os.environ["TELEGRAM_CHAT_ID"]
SEEN_FILE = "seen_ids.json"

GAMERPOWER_GAME = os.environ["GAMERPOWER_GAME_URL"]
GAMERPOWER_LOOT = os.environ["GAMERPOWER_LOOT_URL"]
TELEGRAM_API    = f"https://api.telegram.org/bot{BOT_TOKEN}"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'en-US,en;q=0.9',
}

def pe(emoji_id, fallback):
    return f'<tg-emoji emoji-id="{emoji_id}">{fallback}</tg-emoji>'

EMOJI_GAME     = pe("5467583879948803288", "🎮")
EMOJI_DESC     = pe("5334882760735598374", "📝")
EMOJI_PLATFORM = pe("5431376038628171216", "💻")
EMOJI_TYPE     = pe("5431721976769027887", "📂")
EMOJI_PRICE    = pe("5375296873982604963", "💸")
EMOJI_DATE     = pe("5451732530048802485", "⏳")
EMOJI_HOW      = pe("5318986077455795572", "📌")
EMOJI_LOOT     = pe("5467583879948803288", "🎮")

MAX_CAPTION = 1024

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE) as f:
            return set(json.load(f))
    return set()

def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(sorted(list(seen)), f, indent=2)

def get_claim_url(item):
    gp_url = item.get("open_giveaway", "").strip()
    if not gp_url:
        return ""
    try:
        r = requests.get(gp_url, headers=HEADERS, allow_redirects=False, timeout=10)
        location = r.headers.get("location", "").strip()
        if location:
            print(f"    redirect: {location}")
            return location
        return gp_url
    except Exception as e:
        print(f"    error: {e}")
        return gp_url

def truncate(text, max_len):
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."

def build_caption(item, title_emoji):
    # توضیحات رو کوتاه میکنیم تا caption از 1024 کاراکتر بیشتر نشه
    title       = item.get('title', '')
    description = item.get('description', '')
    platforms   = item.get('platforms', '')
    type_       = item.get('type', '')
    worth       = item.get('worth', '')
    end_date    = item.get('end_date', '')
    instructions= item.get('instructions', '')

    # اول بدون کوتاه کردن بساز
    caption = (
        f"{title_emoji} <b>{title}</b>\n\n"
        f"{EMOJI_DESC} {description}\n\n"
        f"{EMOJI_PLATFORM} <b>Platform:</b> {platforms}\n"
        f"{EMOJI_TYPE} <b>Type:</b> #{type_}\n"
        f"{EMOJI_PRICE} <b>Price:</b> {worth}\n"
        f"{EMOJI_DATE} <b>Ends:</b> {end_date}\n\n"
        f"{EMOJI_HOW} <b>How to Claim</b>\n{instructions}"
    )

    # اگه طولانیه، description و instructions رو کوتاه کن
    if len(caption) > MAX_CAPTION:
        available = MAX_CAPTION - (len(caption) - len(description) - len(instructions))
        half = max(available // 2, 50)
        description  = truncate(description, half)
        instructions = truncate(instructions, half)
        caption = (
            f"{title_emoji} <b>{title}</b>\n\n"
            f"{EMOJI_DESC} {description}\n\n"
            f"{EMOJI_PLATFORM} <b>Platform:</b> {platforms}\n"
            f"{EMOJI_TYPE} <b>Type:</b> #{type_}\n"
            f"{EMOJI_PRICE} <b>Price:</b> {worth}\n"
            f"{EMOJI_DATE} <b>Ends:</b> {end_date}\n\n"
            f"{EMOJI_HOW} <b>How to Claim</b>\n{instructions}"
        )

    return caption[:MAX_CAPTION]

def send_photo(item, is_loot=False):
    claim_url   = get_claim_url(item)
    title_emoji = EMOJI_LOOT if is_loot else EMOJI_GAME
    caption     = build_caption(item, title_emoji)

    payload = {
        "chat_id": CHAT_ID,
        "photo": item.get("image", ""),
        "caption": caption,
        "parse_mode": "HTML",
        "reply_markup": json.dumps({
            "inline_keyboard": [[
                {"text": "✅ Claim Now", "url": claim_url, "style": "success"}
            ]]
        })
    }

    resp = requests.post(f"{TELEGRAM_API}/sendPhoto", data=payload, timeout=15)
    if not resp.ok:
        print(f"  Telegram error: {resp.status_code} - {resp.text[:300]}")
        return False
    print(f"  Sent: {item.get('title', '')}")
    return True

def process(url, seen, is_loot=False):
    try:
        data = requests.get(url, timeout=15).json()
    except Exception as e:
        print(f"  Fetch error: {e}")
        return
    if not isinstance(data, list):
        print(f"  Unexpected: {str(data)[:200]}")
        return
    new_items = [i for i in data if str(i.get("id")) not in seen]
    print(f"  Total: {len(data)} | New: {len(new_items)} | Skipped: {len(data)-len(new_items)}")
    for item in new_items:
        ok = send_photo(item, is_loot=is_loot)
        if ok:
            seen.add(str(item.get("id", "")))
        time.sleep(30)

def main():
    seen = load_seen()
    print(f"Loaded {len(seen)} seen IDs")
    print("\nProcessing Games...")
    process(GAMERPOWER_GAME, seen, is_loot=False)
    print("\nProcessing Loot/DLC...")
    process(GAMERPOWER_LOOT, seen, is_loot=True)
    save_seen(seen)
    print(f"\nSaved {len(seen)} seen IDs - Done.")

if __name__ == "__main__":
    main()
