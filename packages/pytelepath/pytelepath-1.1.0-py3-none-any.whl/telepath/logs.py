import itertools
import traceback

import telegram
import telepath as tp



def log_str_upd(u: telegram.Update):
    s = ""
    mu = u.effective_message.reply_markup
    clicked_cbd = u.callback_query and {b.callback_data: b for b in itertools.chain.from_iterable(mu.inline_keyboard)}[u.callback_query.data]
    try:
        s = "Update:\n"
        s += f"{repr(u)}\n"
        s += f"{u.message.date.astimezone() if u.message is not None else u.effective_message.date.astimezone()}\n"
        s += f"{u.effective_chat.id} "
        s += f"{u.effective_user.id} "
        s += f"{u.effective_user.last_name} "
        s += f"{u.effective_user.first_name} "
        s += f"{u.effective_user.username} "
        s += f"{u.effective_message.message_id}\n"
        if u.callback_query is not None:
            try:
                s += f"{clicked_cbd}\n"
            except Exception as e:
                print(traceback.format_exc())
            s += f"{u.callback_query.data}\n"
            s += f"{u.effective_message.text.replace("\n", " ")}\n"
            s += f"{mu}\n"
        else:
            s += f"{u.message.text}\n" if u.message else f"{u.effective_message.text}\n"
        s += '\n'
        return s
    except Exception as e:
        print(traceback.format_exc())
        return repr(u)

