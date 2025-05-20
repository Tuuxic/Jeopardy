import random
from flask import Flask, request, redirect, url_for
from data_manager import DataManager
from model.player import Player
from model.question import Question
from view_manager import ViewManager

app = Flask(__name__)

data_manager = DataManager()
view_manager = ViewManager()


# --- Admin Routes ---
@app.route('/admin')
def admin_index():
    return view_manager.displayAdminView(
        questions = data_manager.questions,
        players = data_manager.players
    )

@app.route('/admin/add_question', methods=['POST'])
def add_question():
    qs = data_manager.questions 
    nid = max([q.id for q in qs], default=0) + 1
    question = Question(
        id=nid,
        category=request.form['category'],
        value=int(request.form['value']),
        question=request.form['question'],
        answer=request.form['answer']
    )
    data_manager.add_question(question)
    return redirect(url_for('admin_index'))

@app.route('/admin/delete_question/<int:qid>')
def delete_question(qid):
    data_manager.delete_question(qid)
    return redirect(url_for('admin_index'))

@app.route('/admin/add_player', methods=['POST'])
def add_player():
    ps = data_manager.players
    nid = max([p.id for p in ps], default=0) + 1
    player = Player(
        id=nid,
        name=request.form['name'],
        points=int(request.form['points'])
    )
    data_manager.add_player(player)
    return redirect(url_for('admin_index'))

@app.route('/admin/update_player/<int:pid>', methods=['POST'])
def update_player(pid):
    data_manager.update_player(pid, int(request.form['points']))
    return redirect(url_for('admin_index'))

@app.route('/admin/delete_player/<int:pid>')
def delete_player(pid):
    data_manager.delete_player(pid)
    return redirect(url_for('admin_index'))

@app.route('/admin/reset', methods=['POST'])
def reset_game():
    data_manager.reset_players()
    data_manager.reset_state()
    return redirect(url_for('admin_index'))

# --- Game Routes ---
@app.route('/game')
def game_board():
    # TODO: Completely rework this function 

    qs = data_manager.questions
    st = data_manager.state

    all_cats = sorted({q.category for q in qs})
    if st.categories1 and any(c not in all_cats for c in st.categories1):
        # If any category in categories1 is not in all_cats, reset the game 
        data_manager.reset_state()

    if st.round == 1 and not st.categories1:
        # If no categories are set for round 1, select random categories
        st.categories1 = random.sample(all_cats, min(5, len(all_cats)))
        data_manager.save_state()


    if st.round == 1:
        # Check if all questions in categories1 are answered
        ids1 = [q.id for q in qs if q.category in st.categories1]
        if set(ids1) <= set(st.answered):
            # If all questions are answered, move to round 2
            st.round = 2
            st.answered = []
            rem = [c for c in all_cats if c not in st.categories1]
            st.categories2 = random.sample(rem, min(5, len(rem)))
            data_manager.save_state()

    # Get the current categories for the current round 
    cats = st.categories1 if st.round == 1 else st.categories2
    # Get the current points for the current questions 
    vals = sorted({q.value for q in qs if q.category in cats})
    # Set the multiplier for the current round
    mult = 1 if st.round == 1 else 2
    # Create the board with questions
    board = {cat: {val: None for val in vals} for cat in cats}
    # Fill the board with questions
    for q in qs:
        if q.category in cats and q.value in vals:
            board[q.category][q.value] = q

    return view_manager.displayGameView(
        cats=cats,
        vals=vals,
        board=board,
        players=data_manager.players,
        mult=mult,
        answered=st.answered
    )

@app.route('/game/question/<int:qid>', methods=['GET', 'POST'])
def show_question(qid):
    qs = data_manager.questions
    q = next((x for x in qs if x.id == qid), None)

    # Check if the question exists
    if not q:
        return "Frage nicht gefunden", 404
    
    if request.method == 'POST':
        data_manager.add_answered(qid)
        return view_manager.displayQuestionAnswerView(question = q) 

    return view_manager.displayQuestionView(question = q) 

@app.route('/game/unanswer/<int:qid>', methods=['POST'])
def unanswer_question(qid):
    data_manager.remove_answered(qid)
    return ('', 204)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
