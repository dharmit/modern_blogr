import datetime

from pyramid.security import (
    Allow,
    Everyone,
    Authenticated,
    )

from sqlalchemy import (
    Column,
    Table,
    ForeignKey,
    Integer,
    Unicode,
    UnicodeText,
    DateTime,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    )

from sqlalchemy.sql import (
    extract,
    func,
    desc,
    )

from webhelpers2.text import urlify
from webhelpers2.date import time_ago_in_words

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True, nullable=False)
    password = Column(Unicode(255), nullable=False)
    last_logged = Column(DateTime, default=datetime.datetime.utcnow)
    entries = relationship("Entry")

    @classmethod
    def by_name(cls, name):
        return DBSession.query(cls).filter(cls.name == name).first()

    def verify_password(self, password):
        return self.password == password


entries_tags = Table('entries_tags', Base.metadata,
    Column('tag_id', Integer, ForeignKey('tags.id')),
    Column('entry_id', Integer, ForeignKey('entries.id'))
)


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), nullable=False)
    body = Column(UnicodeText, default='')
    user_id = Column(Integer, ForeignKey('users.id'))
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, default=datetime.datetime.utcnow)
    tags = relationship('Tag', secondary=entries_tags, backref='entries')

    @classmethod
    def all(cls):
        return DBSession.query(cls).order_by(desc(cls.created)).all()

    @classmethod
    def by_id(cls, id):
        return DBSession.query(cls).filter(cls.id == id).first()

    @classmethod
    def by_tag_name(cls, tag_name):
        query = DBSession.query(cls)
        return query.filter(cls.tags.any(name=tag_name)).all()

    @classmethod
    def get_page(cls, page, per_page):
        query = DBSession.query(cls).order_by(desc(cls.created))
        return query.slice((page - 1) * per_page, page * per_page).all()

    @classmethod
    def get_month(cls, year, month):
        entries_a_month = DBSession.query(cls).filter(
            (extract('year', cls.created) == year) &
            (extract('month', cls.created) == month)
        ).order_by(cls.created.desc()).all()
        return entries_a_month

    @property
    def author(self):
        return DBSession.query(User).get(self.user_id)

    @property
    def slug(self):
        return urlify(self.title)

    @property
    def created_in_words(self):
        return time_ago_in_words(self.created)


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), unique=True, index=True)

    def __init__(self, name):
        self.name = name

    @staticmethod
    def extract_tags(tags_string):
        tags = tags_string.replace(';', ' ').replace(',', ' ')
        tags = [tag.lower() for tag in tags.split()]
        tags = set(tags)

        return tags

    @classmethod
    def get_by_name(cls, tag_name):
        tag = DBSession.query(cls).filter(cls.name == tag_name)
        return tag.first()

    @classmethod
    def create_tags(cls, tags_string):
        tags_list = cls.extract_tags(tags_string)
        tags = []

        for tag_name in tags_list:
            tag = cls.get_by_name(tag_name)
            if not tag:
                tag = Tag(name=tag_name)
                DBSession.add(tag)
            tags.append(tag)

        return tags

    @classmethod
    def tag_counts(cls):
        query = DBSession.query(Tag.name, func.count('*'))
        return query.join(Entry.tags).group_by(Tag.name)


class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'view'),
                (Allow, Authenticated, 'create'),
                (Allow, Authenticated, 'edit') ]
                
    def __init__(self, request):
        pass
