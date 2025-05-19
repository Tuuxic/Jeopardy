# Jeopardy

Jeopardy game application with 2 rounds, random categories, answered-question greyout, auto-refresh, reset, and unanswer via double-click.

**Round 1**: 5 random categories with original point values  
**Round 2**: 5 new categories (no repeats) with double points

## Features:
- Admin: Manage questions & players
- Admin: Reset game (including deleting players)
- Game: Already answered questions are greyed out
- Game: Double-click to unanswer questions
- Auto-refresh the game page every 10 seconds

## State:
- round: int
- categories1: List[str]
- categories2: List[str]
- answered: List[int]

## Requirements:
- Python 3.x
- Flask (`pip install flask`)
- Pydantic (`pip install pydantic`)
- To install all requirements setup your local venv and run `pip install -r requirements.txt` 

## Usage:
1. Configure:
   - questions.json (initially `[]`)
   - players.json   (initially `[]`)
   - state.json     (initially empty or `[]`)
2. `python3 jeopardy_app.py`
3. Admin: http://\<your-domain\>/admin
4. Game:  http://\<your-domain\>/game