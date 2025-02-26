import datetime
from typing import Annotated

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column



tg_id = int
tgdate_col = Annotated[datetime.datetime, mapped_column(DateTime(timezone=True))]


class TgUserMixin:
    chat_id: Mapped[tg_id] = mapped_column(unique=True)
    user_id: Mapped[tg_id]
    username: Mapped[str | None]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    reg_message_id: Mapped[tg_id]
    start_message_date: Mapped[str | None]
    is_bot: Mapped[bool]


class TgMessageMixin:
    chat_id: Mapped[tg_id]
    user_id: Mapped[tg_id]
    tgdate: Mapped[tgdate_col]
    message_id: Mapped[tg_id]
    text: Mapped[str]
