"""
Jeopardy Game Application mit 2 Runden, Zufalls-Kategorien, answered-greyout, auto-refresh, Reset & Unanswer per Doppelklick

Runde 1: 5 zufällige Kategorien mit originalen Punkten
Runde 2: 5 neue Kategorien (ohne Wiederholung) mit doppelten Punkten

Features:
- Admin: Fragen & Spieler verwalten
- Admin: Spiel zurücksetzen (inkl. Spieler löschen)
- Game: bereits beantwortete Fragen grau
- Game: per Doppelklick beantwortete Fragen wieder freigeben
- Auto-Refresh der Game-Seite alle 10 Sekunden

State in `state.json`:
- round: int
- categories1: List[str]
- categories2: List[str]
- answered: List[int]

Requirements:
- Python 3.x
- Flask (`pip install flask`)

Usage:
1. Lege ab:
   - jeopardy_app.py
   - questions.json (initial `[]`)
   - players.json   (initial `[]`)
   - state.json     (initial leer oder `[]`)
2. `python3 jeopardy_app.py`
3. Admin: http://<deine-domain>/admin
4. Game:  http://<deine-domain>/game
"""
import os, json, random
from flask import Flask, request, redirect, url_for, render_template_string
from json.decoder import JSONDecodeError

app = Flask(__name__)
DATA_Q = 'questions.json'
DATA_P = 'players.json'
STATE_FILE = 'state.json'

 # Load questions from JSON file
with open("questions.json") as f:
    questions = json.load(f)

# Group questions by category
categories = {}
for q in questions:
    categories.setdefault(q["category"], []).append(q)

# --- JSON Helpers ---
def load_json(path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump([], f)
        return [] 
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except JSONDecodeError:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump([], f)
        return []

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# --- State Management ---
def load_state():
    raw = load_json(STATE_FILE)
    if not isinstance(raw, dict):
        raw = {}
    defaults = {'round':1, 'categories1':[], 'categories2':[], 'answered':[]}
    for k,v in defaults.items(): raw.setdefault(k,v)
    save_json(STATE_FILE, raw)
    return raw

def save_state(state):
    save_json(STATE_FILE, state)

def reset_state():
    save_json(STATE_FILE, {'round':1,'categories1':[],'categories2':[],'answered':[]})

# --- Questions & Players ---
# Fragen laden/speichern ohne zu überschreiben bei leerem/fehlerhaftem File
def load_questions():
    if not os.path.exists(DATA_Q):
        save_questions([])
    with open(DATA_Q, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except JSONDecodeError:
            # behalte bisherige Datei, falls ungültiges JSON
            return []

def save_questions(q):
    save_json(DATA_Q, q)

# Spieler laden/speichern analog

def load_players():
    if not os.path.exists(DATA_P):
        save_players([])
    with open(DATA_P, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except JSONDecodeError:
            return []

def save_players(p):
    save_json(DATA_P, p)

def reset_players():
    save_json(DATA_P, [])

# --- Admin Routes ---
@app.route('/admin')
def admin_index():
    return render_template_string(ADMIN_TEMPLATE, questions=load_questions(), players=load_players())

@app.route('/admin/add_question', methods=['POST'])
def add_question():
    qs = load_questions()
    nid = max([q['id'] for q in qs], default=0) + 1
    qs.append({
        'id': nid,
        'category': request.form['category'],
        'value': int(request.form['value']),
        'question': request.form['question'],
        'answer': request.form['answer']
    })
    save_questions(qs)
    return redirect(url_for('admin_index'))

@app.route('/admin/delete_question/<int:qid>')
def delete_question(qid):
    save_questions([q for q in load_questions() if q['id'] != qid])
    return redirect(url_for('admin_index'))

@app.route('/admin/add_player', methods=['POST'])
def add_player():
    ps = load_players()
    nid = max([p['id'] for p in ps], default=0) + 1
    ps.append({'id': nid, 'name': request.form['name'], 'points': int(request.form['points'])})
    save_players(ps)
    return redirect(url_for('admin_index'))

@app.route('/admin/update_player/<int:pid>', methods=['POST'])
def update_player(pid):
    ps = load_players()
    for p in ps:
        if p['id'] == pid:
            p['points'] = int(request.form['points'])
            break
    save_players(ps)
    return redirect(url_for('admin_index'))

@app.route('/admin/delete_player/<int:pid>')
def delete_player(pid):
    save_players([p for p in load_players() if p['id'] != pid])
    return redirect(url_for('admin_index'))

@app.route('/admin/reset', methods=['POST'])
def reset_game():
    reset_state()
    reset_players()
    return redirect(url_for('admin_index'))

# --- Game Routes ---
@app.route('/game')
def game_board():
    qs = load_questions()
    st = load_state()
    all_cats = sorted({q['category'] for q in qs})
    if st['categories1'] and any(c not in all_cats for c in st['categories1']):
        st['round'] = 1
        st['categories1'] = []
        st['categories2'] = []
        st['answered'] = []
        save_state(st)
    if st['round'] == 1 and not st['categories1']:
        st['categories1'] = random.sample(all_cats, min(5, len(all_cats)))
        save_state(st)
    if st['round'] == 1:
        ids1 = [q['id'] for q in qs if q['category'] in st['categories1']]
        if set(ids1) <= set(st['answered']):
            st['round'] = 2
            st['answered'] = []
            rem = [c for c in all_cats if c not in st['categories1']]
            st['categories2'] = random.sample(rem, min(5, len(rem)))
            save_state(st)
    cats = st['categories1'] if st['round'] == 1 else st['categories2']
    vals = sorted({q['value'] for q in qs if q['category'] in cats})
    mult = 1 if st['round'] == 1 else 2
    board = {cat: {val: None for val in vals} for cat in cats}
    for q in qs:
        if q['category'] in cats and q['value'] in vals:
            board[q['category']][q['value']] = q
    return render_template_string(GAME_TEMPLATE, cats=cats, vals=vals, board=board, players=load_players(), mult=mult, answered=st['answered'])

@app.route('/game/question/<int:qid>', methods=['GET', 'POST'])
def show_question(qid):
    qs = load_questions()
    st = load_state()
    q = next((x for x in qs if x['id'] == qid), None)
    if not q:
        return "Frage nicht gefunden", 404
    if request.method == 'POST':
        if qid not in st['answered']:
            st['answered'].append(qid)
            save_state(st)
        return render_template_string(Q_ANSWER_TEMPLATE, q=q)
    return render_template_string(Q_TEMPLATE, q=q)

@app.route('/game/unanswer/<int:qid>', methods=['POST'])
def unanswer_question(qid):
    st = load_state()
    if qid in st['answered']:
        st['answered'].remove(qid)
        save_state(st)
    return ('', 204)

# --- HTML Templates ---
ADMIN_TEMPLATE = '''
<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <title>Jeopardy Admin</title>
  <style>
    body { font-family: sans-serif; margin: 20px; }
    table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
    form { margin-top: 10px; }
    input[type=text], input[type=number] { padding: 5px; margin-right: 10px; }
  </style>
</head>
<body>
  <h1>Admin Interface</h1>
  <h2>Fragen verwalten</h2>
  <table>
    <tr><th>ID</th><th>Kategorie</th><th>Punkte</th><th>Frage</th><th>Antwort</th><th>Aktion</th></tr>
    {% for q in questions %}
    <tr>
      <td>{{ q.id }}</td><td>{{ q.category }}</td><td>{{ q.value }}</td><td>{{ q.question }}</td><td>{{ q.answer }}</td>
      <td><a href="{{ url_for('delete_question', qid=q.id) }}">Löschen</a></td>
    </tr>
    {% endfor %}
  </table>
  <form action="{{ url_for('add_question') }}" method="post">
    Kategorie: <input name="category" required>
    Punkte: <input name="value" type="number" step="100" min="100" required>
    Frage: <input name="question" required>
    Antwort: <input name="answer" required>
    <button type="submit">Hinzufügen</button>
  </form>

  <h2>Spieler verwalten</h2>
  <table>
    <tr><th>ID</th><th>Name</th><th>Punkte</th><th>Aktion</th></tr>
    {% for p in players %}
    <tr>
      <td>{{ p.id }}</td><td>{{ p.name }}</td><td>{{ p.points }}</td>
      <td>
        <form action="{{ url_for('update_player', pid=p.id) }}" method="post" style="display:inline;">
          <input name="points" type="number" value="{{ p.points }}" required>
          <button>Speichern</button>
        </form>
        <a href="{{ url_for('delete_player', pid=p.id) }}">Löschen</a>
      </td>
    </tr>
    {% endfor %}
  </table>
  <form action="{{ url_for('add_player') }}" method="post">
    Name: <input name="name" required>
    Punkte: <input name="points" type="number" value="0" required>
    <button type="submit">Spieler hinzufügen</button>
  </form>

  <h2>Spiel zurücksetzen</h2>
  <form action="{{ url_for('reset_game') }}" method="post" onsubmit="return confirm('Spiel komplett zurücksetzen?');">
    <button>Reset Game & Spieler</button>
  </form>
</body>
</html>
'''

GAME_TEMPLATE = '''
<!doctype html>
<html lang="de">

<head>
    <meta charset="utf-8">
    <title>Jeopardy - Runde {{ mult==1 and '1' or '2' }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script>
        // Auto-Refresh alle 10s
        setInterval(() => location.reload(), 10000);
        // Unanswer per Doppelklick
        document.addEventListener('DOMContentLoaded', () => {
            document.querySelectorAll('.board-button.answered').forEach(btn => {
                btn.addEventListener('dblclick', () => {
                    const qid = btn.dataset.qid;
                    fetch(`/game/unanswer/${qid}`, { method: 'POST' }).then(() => location.reload());
                });
            });
        });
    </script>
    <style>
        body {
            font-family: sans-serif;
            padding: 10px;
            background: #0C0E0F;
            color:#fff;
        }

        h1 {
            margin-bottom: 30px;
            text-align:center;
        }
    
        }
        .players {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
        }

        .player {
            background: #171a1c;
            color:#fff;
            padding: 10px 15px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        .kasten{
            background:#171a1c;
            border-radius: 20px;
            padding: 20px 20px;
            max-width: 1600px;
            margin: 300px auto;
        
        }
        .board {
            display: flex;
            gap: 10px;

        }

        .column {
            flex: 1;
        }

        .col-title {
            text-align: center;
            margin-bottom: 10px;
            font-weight: bold;
            font-size: 1.2em;

        }

        .board-button {
            display: block;
            width: 100%;
            padding: 20px 0;
            margin-bottom: 10px;
            border: none;
            border-radius: 999px;
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: #fff;
            font-size: 1.2em;
            text-decoration: none;
            text-weight:bold;
            text-align: center;
        }

        .board-button:hover {
            opacity: 0.9;
        }

        .board-button.answered {
            background: #ccc !important;
            color: #666 !important;
            cursor: pointer;
        }
    </style>
</head>

<body>
    <div class="players">
        {% for p in players %}
        <div class="player">
            <strong>{{ p.name }}</strong><br>
            Punkte: {{ p.points }}
        </div>
        {% endfor %}
    </div>
    <div class="kasten">
    <h1>Jeopardy - Runde {{ mult==1 and '1' or '2' }}</h1>
        <div class="board">
            {% for cat in cats %}
            <div class="column">
                <div class="col-title">{{ cat }}</div>
                {% for val in vals %}
                {% if board[cat][val] %}
                {% set q = board[cat][val] %}
                {% if q.id in answered %}
                <div class="board-button answered" data-qid="{{ q.id }}">{{ val*mult }}</div>
                {% else %}
                <a href="{{ url_for('show_question', qid=q.id) }}" class="board-button">{{ val*mult }}</a>
                {% endif %}
                {% else %}
                <div style="height:60px; margin-bottom:10px;"></div>
                {% endif %}
                {% endfor %}
            </div>
            {% endfor %}
        </div>
    </div>
</body>

</html>
'''

Q_TEMPLATE = '''
<!doctype html>
<html lang="de">

<head>
    <meta charset="utf-8">
    <title>Frage</title>
    <style>
        body {
            font-family: sans-serif;
            background: #0C0E0F;
            color:#fff;
            padding: 20px;
            margin: 0;
        }

        .question-box {
            position: relative;
            background: linear-gradient(135deg, #4facfe, #00f2fe);
            border-radius: 20px;
            padding: 40px 20px;
            max-width: 1200px;
            margin: 500px auto;
            color: #fff;
            font-size: 2em;
            font-weight: bold;
            text-align:center;
        }
        img {
            width: 500px;
            height: 500px;
            display: block;
            margin: auto;
            padding: 50px;
        }
        .badge {
            position: absolute;
            padding: 5px 10px;
            background: rgba(0, 1, 144, 0.8);
            border-radius: 8px;
            color: #fff;
            font-size: 0.9em;
            margin: -10px auto;
        }

        .badge.category {
            top: -10px;
            left: 20px;
        }

        .badge.value {
            top: -10px;
            right: 20px;
        }

        .answer-btn {
            display: block;
            margin: 30px auto 0 auto;
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            background: #fff;
            color: #333;
            font-size: 1em;
            cursor: pointer;
        }

        .answer-btn:hover {
            opacity: 0.9;
        }
    </style>
</head>

<body>
    <div class="question-box">
        <div class="badge category">{{q.category}}</div>
        <div class="badge value">{{q.value}}</div>
    {% if q %}
      <div class="question">{{ q.question }}</div>

      {% if q.image %}
        <img src="{{ url_for('static', filename=q.image) }}" alt="Question Image">
      {% endif %}

      {% if q.video %}
        <video controls>
          <source src="{{ url_for('static', filename=q.video) }}" type="video/mp4">
          Your browser does not support the video tag.
        </video>
      {% endif %} 

      {% if q.audio %}
        <audio controls>
          <source src="{{ url_for('static', filename=q.audio) }}" type="audio/mpeg">
          Your browser does not support the audio tag.
        </audio>
      {% endif %} 

      {% if show_answer %}
        <div class="answer"><strong>Answer:</strong> {{ q.answer }}</div>
        <a href="{{ url_for('home') }}">Back to board</a>
      {% else %}
        <form method="post">
          <button class="answer-btn">Show Answer</button>
        </form>
      {% endif %}
    {% else %}
      <h1>Jeopardy Board</h1>
      <table>
        <tr>
          {% for cat in categories %}
            <td>{{ cat }}</td>
          {% endfor %}
        </tr>
        <tr>
          {% for cat in categories %}
            <td>
              {% if categories[cat] %}
                <a href="{{ url_for('question', category=cat) }}">{{ categories[cat][0]['value'] }}</a>
              {% else %}
                &nbsp;
              {% endif %}
            </td>
          {% endfor %}
        </tr>
      </table>
    {% endif %}
    </div>
  </body>

</html>
'''

Q_ANSWER_TEMPLATE = '''
<!doctype html>
<html lang="de">

<head>
    <meta charset="utf-8">
    <title>Antwort</title>
    <style>
        body {
            font-family: sans-serif;
            background: #0C0E0F;
            color:#fff;
            padding: 20px;
            margin: 0;
        }

        .question-box {
            position: relative;
            background: linear-gradient(135deg, #4facfe, #00f2fe);
            border-radius: 20px;
            padding: 80px 20px;
            max-width: 1200px;
            margin: 500px auto;
            color: #fff;
            font-size: 2em;
            text-align:center;
        }

        .badge {
            position: absolute;
            padding: 5px 10px;
            background: rgba(0, 1, 144, 0.8);
            border-radius: 8px;
            color: #fff;
            font-size: 1em;
            margin: -10px auto;
        }

        .badge.category {
            top: -10px;
            left: 20px;
        }

        .badge.value {
            top: -10px;
            right: 20px;
        }

        .back-link {
            display: block;
            margin: 30px auto 0 auto;
            padding: 10px 20px;
            background: #fff;
            color: #333;
            text-decoration: none;
            border-radius: 8px;
            max-width: 200px;
            text-align: center;
        }

        .back-link:hover {
            opacity: 0.9;
        }
    </style>
</head>

<body>
    <div class="question-box">
        <div class="badge category">{{q.category}}</div>
        <div class="badge value">{{q.value}}</div>
        <div>{{q.question}}</div>
        <p style="margin-top:20px;"><strong>Antwort:</strong> {{q.answer}}</p><a href="{{url_for('game_board')}}"
            class="back-link">Zurück</a>
    </div>
</body>

</html>
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
