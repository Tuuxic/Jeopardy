from constants import QUESTIONS_PATH, PLAYERS_PATH, STATE_PATH
from json.decoder import JSONDecodeError
import os, json

from model.player import Player
from model.question import Question
from model.state import State

class DataManager:

    def __init__(self):
        self.state = self.load_state()
        self.players = self.load_players()
        self.questions = self.load_questions()

    def load_state(self):
        raw = DataManager.load_json(STATE_PATH)
        if not isinstance(raw, dict):
            return State()
        
        return State(**raw)

    def save_state(self):
        DataManager.save_json(STATE_PATH, self.state.get_dictionary())

    def reset_state(self):
        DataManager.save_json(STATE_PATH, State().get_dictionary())

    # --- Questions & Players ---
    # Fragen laden/speichern ohne zu überschreiben bei leerem/fehlerhaftem File
    def load_questions(self):
        if not os.path.exists(QUESTIONS_PATH):
            self.save_questions([])
        with open(QUESTIONS_PATH, 'r', encoding='utf-8') as f:
            try:
                questions_json = json.load(f)
                return [Question(**q) for q in questions_json]
            except JSONDecodeError:
                # behalte bisherige Datei, falls ungültiges JSON
                return []

    def save_questions(self):
        questions_json = [q.getDictionary() for q in self.questions]
        print(f"Saving questions: {questions_json}")
        DataManager.save_json(QUESTIONS_PATH, data = questions_json)

    # Spieler laden/speichern analog

    def load_players(self):
        if not os.path.exists(PLAYERS_PATH):
            self.save_players([])
        with open(PLAYERS_PATH, 'r', encoding='utf-8') as f:
            try:
                players_json = json.load(f)
                return [Player(**p) for p in players_json]
            except JSONDecodeError:
                return []

    def save_players(self):
        players_json = [p.getDictionary() for p in self.players]
        DataManager.save_json(PLAYERS_PATH, players_json)

    def reset_players(self):
        self.players = []
        self.save_players()


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


    def add_question(self, question):
        self.questions.append(question)
        self.save_questions()

    def delete_question(self, question_id):
        self.questions = [q for q in self.questions if q['id'] != question_id]
        self.save_questions()


    def add_answered(self, question_id: int):
        if question_id not in self.state.answered:
            self.state.answered.append(question_id)
    
    def remove_answered(self, question_id: int):
        if question_id in self.state.answered:
            self.state.answered.remove(question_id)

    def is_answered(self, question_id: int):
        return question_id in self.state.answered

    def add_player(self, player):
        self.players.append(player)
        self.save_players()

    def update_player(self, player_id, points):
        for i, p in enumerate(self.players):
            if p.id == player_id:
                self.players[i].points = points 
                break
        self.save_players()

    def delete_player(self, player_id):
        self.players = [p for p in self.players if p.id != player_id]
        self.save_players()
