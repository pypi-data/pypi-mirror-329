import enum
from collections import OrderedDict
from itertools import chain

import telegram as t
import telepath as tp



class TgBtn:
    
    def __init__(self, text: str, cbdo: tp.CoolBackData):
        self._text = text
        self.cbdo = cbdo
    
    
    @staticmethod
    def from_params(text: str, btn_id, btn_type, msg_type, value=None):
        return TgBtn(text, tp.CoolBackData(msg_type, btn_type, btn_id, value))
    
    
    @staticmethod
    def from_ptb(ikb: t.InlineKeyboardButton):
        return TgBtn(ikb.text, tp.CoolBackData.from_str(ikb.callback_data))
    
    
    def text(self):
        return tp.with_checked_emoji(self.cbdo.checked, self._text)
    
    
    def callback_data(self) -> str:
        return self.cbdo.pack()
    
    
    def compile(self):
        return t.InlineKeyboardButton(self.text(), callback_data=self.callback_data())
    
    
    @property
    def id(self):
        return self.cbdo.btn_id
    
    
    @id.setter
    def id(self, new_id):
        self.cbdo.btn_id = new_id


class InlineKeyboard:
    
    def __init__(self, kb_tree):
        self.kb_tree: list[list[TgBtn]] = kb_tree
        pairs = [(b.id, b) for b in chain.from_iterable(kb_tree)]
        self.btns = OrderedDict(pairs)
    
    
    @staticmethod
    def from_markup(mu: t.InlineKeyboardMarkup):
        kb_tree = []
        for row in mu.inline_keyboard:
            kb_row = [TgBtn.from_ptb(b) for b in row]
            kb_tree.append(kb_row)
        return InlineKeyboard(kb_tree)
    
    
    @staticmethod
    def from_list(btn_list):
        return InlineKeyboard([[b] for b in btn_list])
    
    
    def compile(self):
        rows = [[tp.ikb(b.text(), callback_data=b.callback_data()) for b in row] for row in self.kb_tree]
        return t.InlineKeyboardMarkup(rows)


class KbLayout(enum.Enum):
    COL = 1
    ROW = 2
    CUSTOM = 3


class Message:
    def __init__(self, text, kb):
        self.text = text
        self.kb = kb
