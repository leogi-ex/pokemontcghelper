# PokemonTCGHelper 🃏

A Discord bot for Pokémon TCG Live (PTCGL) players. Paste your exported decklists directly into Discord and instantly receive scannable QR code grids — ready to import into the PTCGL app. Also includes deck management and combat log tracking features.

---

## Features

- **QR Code Generation** — Convert PTCGL decklist exports into grids of scannable QR codes, batched 10 per image for easy scanning in the app
- **Multi-expansion support** — Automatically groups QR codes by expansion, with section headers rendered in the Discord message
- **Deck management** — Create and version-control your decks directly from Discord
- **Combat log tracking** — Record match results and opponent decklists, organized by deck and version

---

## Project Structure

```
PokemonTCGHelper/
├── discord_bot_code.py         # Main bot logic: commands and events
├── CreateQRCodes/
│   └── Create_QR_Codes_Discord.py  # QR code generation and PTCGL code parsing
├── requirements.txt            # Python dependencies
├── config.txt                  # Bot configuration (not committed — see setup)
├── insults.txt                 # Text file used by a fun command
└── main_image.jpg              # Project image
```

---

## Prerequisites

- Python 3.9+
- A Discord bot token ([Discord Developer Portal](https://discord.com/developers/applications))
- The bot must have the following permissions:
  - Send Messages
  - Read Message History
  - Attach Files
  - Embed Links
  - Manage Messages (to delete processed messages)

---

## Setup

**1. Clone the repository**

```bash
git clone https://github.com/Leogi-ex/PokemonTCGHelper.git
cd PokemonTCGHelper
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Create `config.txt`**

Create a `config.txt` file in the root directory with the following structure:

```json
{
  "TOKEN": "your-discord-bot-token",
  "Channel_ID": 123456789012345678
}
```

| Key | Description |
|-----|-------------|
| `TOKEN` | Your Discord bot token |
| `Channel_ID` | The Discord channel the bot posts to by default |

**4. Create the combat log directory**

Required if you intend to use the combat log tracking feature:

```bash
mkdir -p "Combat Logs/Decks"
```

**5. Run the bot**

```bash
python discord_bot_code.py
```

---

## Commands

### `/hello`
A simple test command. The bot greets you by mention.

---

### `/getqrcodes` (or `!P GetQR`)
The core command. Paste your PTCGL decklist export and receive back a series of QR code grid images (10 codes per image), grouped and labeled by expansion.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `codes_for_qr` | ✅ | The full decklist export copied from PTCGL |

**How to use:**
1. Open Pokémon TCG Live and export your decklist to clipboard.
2. In Discord, run `/getqrcodes` and paste the export into the `codes_for_qr` field.
3. The bot replies with QR code grid images. Open the PTCGL app's QR scanner and scan each image to import your cards.

---

### `/create_deck`
Creates a new deck directory for tracking purposes.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `main_pokemon` | ✅ | Name of the main Pokémon (no spaces) |
| `decklist` | ✅ | Exported decklist from PTCGL |
| `sub_pokemon` | ➖ | Name of a secondary Pokémon (no spaces) |

---

### `/create_deck_version`
Creates a new version of an existing tracked deck (useful when you make changes to a deck over time).

| Parameter | Required | Description |
|-----------|----------|-------------|
| `main_pokemon` | ✅ | Name of the main Pokémon (no spaces) |
| `decklist` | ✅ | Updated decklist export from PTCGL |
| `sub_pokemon` | ➖ | Name of a secondary Pokémon (no spaces) |

---

### `/record_combat`
Saves the combat log from the previous message in the channel. Attach the PTCGL combat log file as a message, then run this command immediately after.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `deck` | ✅ | The deck you played |
| `opponent_deck` | ✅ | The deck your opponent played |
| `version` | ➖ | Which version of your deck you were using (auto-detected if omitted) |

Combat logs are saved under `Combat Logs/Decks/<deck>/v<version>/combat_logs/` and named with the opponent deck and timestamp.

---

## How QR Code Generation Works

PTCGL uses QR codes to import individual cards into the app. When you export a decklist, each card is represented by a code string. This bot:

1. Parses the raw PTCGL export, separating card codes from set/expansion labels
2. Generates a QR code image for each card code
3. Batches them into grids of 10 (2 rows × 5 columns) sized for easy in-app scanning
4. Posts each grid as a PNG image to Discord, with expansion name headers between groups

---

## Dependencies

See `requirements.txt`. Key libraries:

- [`discord.py`](https://discordpy.readthedocs.io/) — Discord bot framework
- `qrcode` / `Pillow` — QR code generation and image handling
- `matplotlib` — Rendering QR code grids as image figures

---

## License

This project does not currently specify a license. All rights reserved by the author.
