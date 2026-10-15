# Zombie Escape

Top-down wave survival shooter. Survive increasingly difficult zombie waves,
manage your ammunition, and use explosive barrels to clear groups of zombies.

## Installation and running

The game uses Python and Pygame. From the project folder, install the Pygame
Community Edition package:

```bash
python -m pip install pygame-ce
python game.py
```

`pygame-ce` provides the `pygame` module used by the game.

## Controls

| Key | Action |
|-----|--------|
| W/A/S/D or Arrow Keys | Move |
| Left Click | Shoot toward the cursor |
| R | Reload; after game over, restart |

## Gameplay

- **Health:** The player starts with 3 HP. A zombie touch removes 1 HP. After
  taking damage, the player has a 1-second invincibility period and blinks.
  The game ends at 0 HP. Health is shown in the HUD.
- **Ammunition:** The magazine holds 12 bullets. Each shot uses one bullet;
  shooting is blocked while empty or reloading. Press **R** to reload, which
  takes 2 seconds. The HUD shows ammunition or the remaining reload time.
- **Explosive barrels:** Four barrels are placed around the arena at the start
  of each game. Shooting one removes it and creates an explosion that destroys
  zombies within 115 pixels. Barrels do not respawn after exploding.
- **Zombie types:** Normal zombies have 3 HP and standard speed. Fast zombies
  are smaller, faster, and have 1 HP. Tank zombies are larger, slower, and have
  6 HP. New waves add fast zombies from wave 2 and tank zombies from wave 3,
  alongside normal zombies.
- **Waves and score:** Eliminate the required number of zombies to advance.
  The score combines time survived and kill bonuses. Press **R** on the game
  over screen to start a fresh game.
