# Memory Fitness

A desktop cognitive training and benchmark application inspired by [humanbenchmark.com](https://humanbenchmark.com), built using Python, Tkinter, and CustomTkinter.

Developed as a school seminar project by **Peter Žukovský** and **Viktor Slašťan**.

---

## 🎮 Included Games & Tests

1. **Sequence Memory** – Remember and repeat an increasingly long sequence of highlighted circles.
2. **Chimp Test** – Memorize numbers in randomly positioned squares and click them in ascending order once numbers vanish.
3. **Aim Trainer** – Test your mouse precision and reflexes across 20 appearing targets.
4. **Typing** – Slovak word typing test measuring accuracy and words-per-minute (WPM).
5. **Verbal Memory** – Keep track of words you've seen versus new words to test recognition memory.
6. **Number Memory** – Memorize a number flashed on screen for a short duration with increasing digits each round.
7. **Visual Memory** – Remember the locations of flashing squares on a grid.
8. **Reaction Time** – Click as fast as possible when the target appears on screen.

---

## ✨ Features

- **User Accounts & Authentication**: Local user registration and login with SHA-256 hashed passwords.
- **Persistent Statistics**: Saves gameplay history and automatically displays the top 3 best scores per game in the pre-game waiting room.
- **Light & Dark Themes**: Customizable visual themes and responsive color schemes.
- **Dynamic Scaling**: Automatically scales UI canvas elements and fonts based on screen resolution.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or newer
- Required Python libraries:
  ```bash
  pip install customtkinter Pillow
  ```

### Running the App

```bash
python Memory_Fitness_2.py
```

1. Register an account on the login screen (Registrovať sa) or log in with existing credentials (Prihlásiť sa).
2. Choose a game from the main menu.
3. Review your best scores and instructions in the waiting room, then start playing!

---

## 📄 Documentation

For full details on project architecture, design choices, and test logs, see [`Documentation.pdf`](Documentation.pdf).
