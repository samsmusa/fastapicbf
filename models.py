# coding: utf-8
from sqlalchemy import BigInteger, CheckConstraint, Column, Date, ForeignKey, Index, Integer, String
from sqlalchemy.dialects.mysql import DATETIME, LONGTEXT, SMALLINT, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

from sqlalchemy import Table

FilterYouthSkill = Table(
    'filter_youth_skill',
    Base.metadata, Column("youth_id", ForeignKey('filter_youth.id'), primary_key=True),
    Column("skill_id", ForeignKey('filter_skill.id'), primary_key=True)
)


class AuthGroup(Base):
    __tablename__ = 'auth_group'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False, unique=True)
    active = Column(TINYINT(1), nullable=False)


class AuthenticationUser(Base):
    __tablename__ = 'authentication_user'

    id = Column(BigInteger, primary_key=True)
    password = Column(String(128), nullable=False)
    last_login = Column(DATETIME(fsp=6))
    is_superuser = Column(TINYINT(1), nullable=False)
    username = Column(String(150), nullable=False, unique=True)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    is_staff = Column(TINYINT(1), nullable=False)
    is_active = Column(TINYINT(1), nullable=False)
    date_joined = Column(DATETIME(fsp=6), nullable=False)
    created_at = Column(DATETIME(fsp=6), nullable=False)
    updated_at = Column(DATETIME(fsp=6), nullable=False)
    email_verified_at = Column(DATETIME(fsp=6), nullable=False)
    email = Column(String(254), nullable=False, unique=True)
    phone = Column(String(40))
    profile_image = Column(String(100))
    gender = Column(String(2))
    birth_date = Column(Date)
    age = Column(Integer)
    location = Column(String(200))
    country_code = Column(String(3))
    country = Column(String(255))
    city = Column(String(255))
    address = Column(String(255))
    bio = Column(LONGTEXT)


class DjangoContentType(Base):
    __tablename__ = 'django_content_type'
    __table_args__ = (
        Index('django_content_type_app_label_model_76bd3d3b_uniq', 'app_label', 'model', unique=True),
    )

    id = Column(Integer, primary_key=True)
    app_label = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)


class DjangoMigration(Base):
    __tablename__ = 'django_migrations'

    id = Column(BigInteger, primary_key=True)
    app = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    applied = Column(DATETIME(fsp=6), nullable=False)


class DjangoSession(Base):
    __tablename__ = 'django_session'

    session_key = Column(String(40), primary_key=True)
    session_data = Column(LONGTEXT, nullable=False)
    expire_date = Column(DATETIME(fsp=6), nullable=False, index=True)


class FilterJob(Base):
    __tablename__ = 'filter_job'

    id = Column(BigInteger, primary_key=True)
    title = Column(String(255))
    description = Column(LONGTEXT, nullable=False)


class FilterSkilltype(Base):
    __tablename__ = 'filter_skilltype'

    id = Column(BigInteger, primary_key=True)
    type = Column(String(500))


class FilterYouth(Base):
    __tablename__ = 'filter_youth'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(50))
    education_label = Column(String(100), nullable=False)
    education_field = Column(String(100), nullable=False)
    skills = relationship(
        "FilterSkill",
        secondary=FilterYouthSkill,
        back_populates="youth_skill"
    )


class AuthPermission(Base):
    __tablename__ = 'auth_permission'
    __table_args__ = (
        Index('auth_permission_content_type_id_codename_01ab375a_uniq', 'content_type_id', 'codename', unique=True),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    content_type_id = Column(ForeignKey('django_content_type.id'), nullable=False)
    codename = Column(String(100), nullable=False)

    content_type = relationship('DjangoContentType')


class AuthenticationUserGroup(Base):
    __tablename__ = 'authentication_user_groups'
    __table_args__ = (
        Index('authentication_user_groups_user_id_group_id_8af031ac_uniq', 'user_id', 'group_id', unique=True),
    )

    id = Column(BigInteger, primary_key=True)
    user_id = Column(ForeignKey('authentication_user.id'), nullable=False)
    group_id = Column(ForeignKey('auth_group.id'), nullable=False, index=True)

    group = relationship('AuthGroup')
    user = relationship('AuthenticationUser')


class DjangoAdminLog(Base):
    __tablename__ = 'django_admin_log'
    __table_args__ = (
        CheckConstraint('(`action_flag` >= 0)'),
    )

    id = Column(Integer, primary_key=True)
    action_time = Column(DATETIME(fsp=6), nullable=False)
    object_id = Column(LONGTEXT)
    object_repr = Column(String(200), nullable=False)
    action_flag = Column(SMALLINT, nullable=False)
    change_message = Column(LONGTEXT, nullable=False)
    content_type_id = Column(ForeignKey('django_content_type.id'), index=True)
    user_id = Column(ForeignKey('authentication_user.id'), nullable=False, index=True)

    content_type = relationship('DjangoContentType')
    user = relationship('AuthenticationUser')


class FilterJobprofile(Base):
    __tablename__ = 'filter_jobprofile'

    id = Column(BigInteger, primary_key=True)
    skills = Column(LONGTEXT, nullable=False)
    job_id = Column(ForeignKey('filter_job.id'), nullable=False, index=True)

    job = relationship('FilterJob')


class FilterSkill(Base):
    __tablename__ = 'filter_skill'

    id = Column(BigInteger, primary_key=True)
    skill = Column(String(100))
    type_id = Column(ForeignKey('filter_skilltype.id'), nullable=False, index=True)

    type = relationship('FilterSkilltype')
    filteryouth = relationship(
        "FilterYouth",
        secondary=FilterYouthSkill,
        back_populates="skill_youth"
    )


class FilterYouthprofile(Base):
    __tablename__ = 'filter_youthprofile'

    id = Column(BigInteger, primary_key=True)
    skills = Column(LONGTEXT, nullable=False)
    youth_id = Column(ForeignKey('filter_youth.id'), nullable=False, index=True)

    youth = relationship('FilterYouth')


class AuthGroupPermission(Base):
    __tablename__ = 'auth_group_permissions'
    __table_args__ = (
        Index('auth_group_permissions_group_id_permission_id_0cd325b0_uniq', 'group_id', 'permission_id', unique=True),
    )

    id = Column(BigInteger, primary_key=True)
    group_id = Column(ForeignKey('auth_group.id'), nullable=False)
    permission_id = Column(ForeignKey('auth_permission.id'), nullable=False, index=True)

    group = relationship('AuthGroup')
    permission = relationship('AuthPermission')


class AuthenticationUserUserPermission(Base):
    __tablename__ = 'authentication_user_user_permissions'
    __table_args__ = (
        Index('authentication_user_user_user_id_permission_id_ec51b09f_uniq', 'user_id', 'permission_id', unique=True),
    )

    id = Column(BigInteger, primary_key=True)
    user_id = Column(ForeignKey('authentication_user.id'), nullable=False)
    permission_id = Column(ForeignKey('auth_permission.id'), nullable=False, index=True)

    permission = relationship('AuthPermission')
    user = relationship('AuthenticationUser')


class FilterJobSkill(Base):
    __tablename__ = 'filter_job_skill'
    __table_args__ = (
        Index('filter_job_skill_job_id_skill_id_01bfd827_uniq', 'job_id', 'skill_id', unique=True),
    )

    id = Column(BigInteger, primary_key=True)
    job_id = Column(ForeignKey('filter_job.id'), nullable=False)
    skill_id = Column(ForeignKey('filter_skill.id'), nullable=False, index=True)

    job = relationship('FilterJob')
    skill = relationship('FilterSkill')

#
# class FilterYouthSkill(Base):
#     __tablename__ = 'filter_youth_skill'
#     __table_args__ = (
#         Index('filter_youth_skill_youth_id_skill_id_be4fae76_uniq', 'youth_id', 'skill_id', unique=True),
#     )
#
#     id = Column(BigInteger, primary_key=True)
#     youth_id = Column(ForeignKey('filter_youth.id'), nullable=False)
#     skill_id = Column(ForeignKey('filter_skill.id'), nullable=False, index=True)
#
#     skill = relationship('FilterSkill')
#     youth = relationship('FilterYouth')
