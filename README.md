# Galaxy Defender

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Pygame](https://img.shields.io/badge/pygame-CE-yellow)
![Platform](https://img.shields.io/badge/platform-desktop-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

A 2D space shooter built with Python and Pygame. Pilot a rocket, shoot down UFOs, dodge asteroids, and survive to reach a score of 10.

---

## Features

- **Arcade shooting** — destroy UFOs with a 7-bullet magazine and a 3-second reload cooldown
- **Two enemy types** — UFOs (score targets) and asteroids (obstacles)
- **Lives & lost counter** — start with 3 lives; lose 1 on collision, game ends at 0 lives or 3 escaped UFOs
- **Real-time HUD** — score, lives, lost count, and ammo at a glance
- **Win/lose conditions** — score 10 to win, or defend against 3 escapes
- **Sound & music** — background music, fire, win, and lose SFX

---

## Tech

| Layer | Stack |
|-------|-------|
| Language | Python 3.8+ |
| Framework | Pygame CE 2.6+ |
| Audio | `pygame.mixer` (`.ogg`, `.wav`) |
| Input | Keyboard (arrow keys + space/R) |

---

## Installation

```bash
pip install pygame-ce
```

---

## Run

```bash
git clone https://github.com/itsradellana/galaxy-defender.git
cd galaxy-defender
python shooter_game.py
```

All asset files (sprites and audio) must stay alongside `shooter_game.py`.

---

## Controls

| Key | Action |
|-----|--------|
| `←` / `→` / `↑` / `↓` | Move rocket |
| `SPACE` | Fire bullet |
| `R` | Reload (3s cooldown) |

---

## Project Structure

```
galaxy-defender/
├── shooter_game.py    # Game logic (single file)
├── README.md
├── LICENSE
├── galaxy.jpg         # Background
├── rocket.png         # Player sprite
├── ufo.png            # Enemy sprite
├── asteroid.png       # Obstacle sprite
├── bullet.png         # Projectile sprite
├── space.ogg          # Background music
├── fire.ogg           # Fire SFX
├── win.wav            # Win SFX
└── lost.wav           # Lose SFX
```

---

## License

MIT License — see `LICENSE` file for details.

---

## About

Built as a learning project for Python and Pygame fundamentals: sprite management, collision detection, game loop architecture, and asset handling.
