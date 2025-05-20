from flask import render_template_string
from templates.admin_template import ADMIN_TEMPLATE
from templates.game_template import GAME_TEMPLATE
from templates.question_answer_template import QUESTION_ANSWER_TEMPLATE
from templates.question_template import QUESTION_TEMPLATE


class ViewManager:
    def __init__(self):
        self.views = {}

    def displayAdminView(self, questions, players):
        return render_template_string(
            ADMIN_TEMPLATE, 
            questions = questions, 
            players = players 
        )
    
    def displayGameView(self, cats, vals, board, players, mult, answered):
        return render_template_string(
            GAME_TEMPLATE,
            cats=cats,
            vals=vals,
            board=board,
            players= players,
            mult=mult,
            answered=answered
        )

    def displayQuestionView(self, question):
        return render_template_string(
            QUESTION_TEMPLATE, 
            q=question
        )
    
    def displayQuestionAnswerView(self, question):
        return render_template_string(
            QUESTION_ANSWER_TEMPLATE, 
            q=question, 
        )

