# Jeopardy

Jeopardy Game Application mit 2 Runden, Zufalls-Kategorien, answered-greyout, auto-refresh, Reset & Unanswer per Doppelklick

Runde 1: 5 zufällige Kategorien mit originalen Punkten
Runde 2: 5 neue Kategorien (ohne Wiederholung) mit doppelten Punkten

## Features:
- Admin: Fragen & Spieler verwalten
- Admin: Spiel zurücksetzen (inkl. Spieler löschen)
- Game: bereits beantwortete Fragen grau
- Game: per Doppelklick beantwortete Fragen wieder freigeben
- Auto-Refresh der Game-Seite alle 10 Sekunden

## State in `state.json`:
- round: int
- categories1: List[str]
- categories2: List[str]
- answered: List[int]

## Requirements:
- Python 3.x
- Flask (`pip install flask`)

## Usage:
1. Lege ab:
   - jeopardy_app.py
   - questions.json (initial `[]`)
   - players.json   (initial `[]`)
   - state.json     (initial leer oder `[]`)
2. `python3 jeopardy_app.py`
3. Admin: http://<deine-domain>/admin
4. Game:  http://<deine-domain>/game