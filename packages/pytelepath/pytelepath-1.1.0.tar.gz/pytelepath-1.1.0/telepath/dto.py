import dataclasses

import telegram as t



@dataclasses.dataclass(slots=True)
class TgUpd:
    chat_id: int
    user_id: int
    msg_id: int
    cbd: str | None
    kbm: t.InlineKeyboardMarkup | None
    
    
    @staticmethod
    def of(u: t.Update):
        return TgUpd(u.effective_chat.id, u.effective_user.id, u.effective_message.id,
                     u.callback_query and u.callback_query.data,
                     u.effective_message.reply_markup)


