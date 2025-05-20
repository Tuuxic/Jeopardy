from typing import Any
from constants import QUESTIONS_PATH, PLAYERS_PATH, STATE_PATH
from json.decoder import JSONDecodeError
import os, json

from model.player import Player
from model.question import Question
from model.state import State

class DataManager:
    state: State 
    players: list[Player] 
    questions: list[Question] 

    def __init__(self):
        self.state: State = self.load_state()
        self.players: list[Player] = self.load_players()
        self.questions: list[Question] = self.load_questions()

    # --- State ---

    def load_state(self) -> State:
        raw = JsonHelper.load_json(STATE_PATH)
        if not isinstance(raw, dict):
            return State()
        
        return State(**raw)

    def save_state(self) -> State:
        JsonHelper.save_json(STATE_PATH, self.state.to_json())

    def reset_state(self) -> None:
        self.state = State()
        self.save_state()

    # --- Questions --- 

    def load_questions(self) -> list[Question]:
        if not os.path.exists(QUESTIONS_PATH):
            self.questions = []
            self.save_questions()
        with open(QUESTIONS_PATH, 'r', encoding='utf-8') as f:
            try:
                questions_json = json.load(f)
                return [Question(**q) for q in questions_json]
            except JSONDecodeError:
                # behalte bisherige Datei, falls ungültiges JSON
                return []

    def save_questions(self) -> None:
        questions = [q.to_json() for q in self.questions]
        JsonHelper.save_json(QUESTIONS_PATH, data = questions)

    
    def add_question(self, question: Question) -> None:
        self.questions.append(question)
        self.save_questions()

    def delete_question(self, question_id: int) -> None:
        self.questions = [q for q in self.questions if q.id != question_id]
        self.save_questions()


    def add_answered(self, question_id: int) -> None:
        if question_id not in self.state.answered:
            self.state.answered.append(question_id)
    
    def remove_answered(self, question_id: int) -> None:
        if question_id in self.state.answered:
            self.state.answered.remove(question_id)

    def is_answered(self, question_id: int) -> bool:
        return question_id in self.state.answered


    # --- Players --- 

    def load_players(self) -> list[Player]:
        if not os.path.exists(PLAYERS_PATH):
            self.reset_players()
        with open(PLAYERS_PATH, 'r', encoding='utf-8') as f:
            try:
                players_json = json.load(f)
                return [Player(**p) for p in players_json]
            except JSONDecodeError:
                return []

    def save_players(self):
        players = [p.to_json() for p in self.players]
        JsonHelper.save_json(PLAYERS_PATH, players)

    def reset_players(self) -> None:
        self.players = []
        self.save_players()


    def add_player(self, player: Player) -> None:
        self.players.append(player)
        self.save_players()

    def update_player(self, player_id: int, points: int) -> None:
        for i, p in enumerate(self.players):
            if p.id == player_id:
                self.players[i].points = points 
                break
        self.save_players()

    def delete_player(self, player_id: int) -> None:
        self.players = [p for p in self.players if p.id != player_id]
        self.save_players()


class JsonHelper:
    @staticmethod
    def load_json(path: str) -> list:
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
        
    @staticmethod
    def save_json(path: str, data: Any):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)