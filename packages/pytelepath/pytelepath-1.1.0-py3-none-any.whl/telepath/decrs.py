import functools
import logging
import traceback

import telegram
import telegram.ext as te

from . import logs



def answers_callback_query(func):
    @functools.wraps(func)
    async def wrapper(update: telegram.Update, context: te.ContextTypes.DEFAULT_TYPE):
        try:
            return await func(update, context)
        except:
            traceback.print_exc()
        finally:
            await context.bot.answerCallbackQuery(update.callback_query.id)
    
    
    return wrapper


def self_answers_callback_query(func):
    @functools.wraps(func)
    async def wrapper(self, update: telegram.Update, context: te.ContextTypes.DEFAULT_TYPE):
        try:
            return await func(self, update, context)
        except:
            traceback.print_exc()
        finally:
            await context.bot.answerCallbackQuery(update.callback_query.id)
    
    
    return wrapper


def alog_update(name):
    def decor(func):
        @functools.wraps(func)
        async def wrapper(self, update: telegram.Update, context: te.ContextTypes.DEFAULT_TYPE):
            # logging.getLogger(name).warning(log_str_upd(update))
            logging.info(logs.log_str_upd(update))
            return await func(self, update, context)
        
        
        return wrapper
    
    
    return decor


def answers_callback_query_vargs(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except:
            traceback.print_exc()
        finally:
            d = {type(arg): arg for arg in args}
            d.update({type(kw): kw for kw in kwargs.values()})
            update = d[telegram.Update]
            ctx = d[telegram.ext.ContextTypes.DEFAULT_TYPE]
            await ctx.bot.answerCallbackQuery(update.callback_query.id)
    
    
    return wrapper
