import sqlalchemy as db
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Category(Base):

    __tablename__ = 'Category'

    id: int = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    name_category: str = db.Column(db.String(255), nullable=False)


class Article(Base):

    __tablename__ = 'Article'

    id: int = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    category_id: int = db.Column(db.Integer, db.ForeignKey(Category.id,  onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    title: str = db.Column(db.String(255), nullable=False)
    body: str = db.Column(db.Text, nullable=False)
    link_dzer: str = db.Column(db.String(10000), nullable=False)
    link_source: str = db.Column(db.String(10000), nullable=False)
    time_parse: str = db.Column(db.String(255), nullable=False)
