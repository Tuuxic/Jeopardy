
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