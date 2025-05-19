
QUESTION_ANSWER_TEMPLATE = '''
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

        <p style="margin-top:20px;"><strong>Antwort:</strong> {{q.answer}}</p><a href="{{url_for('game_board')}}"
            class="back-link">Zurück</a>
    </div>
</body>

</html>
'''