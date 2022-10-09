from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, Integer, Text, BigInteger, VARCHAR
from database import Base


# class Movie(Base):
#     __tablename__ = "Movie"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(20), unique=True)
#     desc = Column(Text())
#     type = Column(String(20))
#     url = Column(String(100))
#     rating = Column(Integer)
#
# class Actor(Base):
#     __tablename__ = "Actor"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(50))

class SkillType(Base):
    __tablename__ = 'filter_skilltype'
    id = Column(BigInteger, primary_key=True, index=True)
    type = Column(String(500))


class Skill(Base):
    __tablename__ = "filter_skill"
    id = Column(BigInteger, primary_key=True, index=True)
    skill = Column(String(20))
    type_id = Column(BigInteger, ForeignKey("SkillType.id"))
