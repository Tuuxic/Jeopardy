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