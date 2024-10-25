from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from orm.setting import db


class URL(db.Model):
    id = mapped_column(Integer, autoincrement=True, primary_key=True)
    short_id = mapped_column(String, unique=True, nullable=False)
    long_url = mapped_column(String, unique=True, nullable=False)
    description = mapped_column(String)
    enabled = mapped_column(Boolean, default=True)
