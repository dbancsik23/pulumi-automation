from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import current_timestamp

Base = declarative_base()


class StackConfiguration(Base):
    __tablename__ = 'stack_configurations'
    id = Column("id", Integer, index=True, primary_key=True)
    project_name = Column("project_name", String(255))
    stack_name = Column("stack_name", String(255))
    created_at = Column("created_at", DateTime(), default=current_timestamp())
    updated_at = Column("updated_at", DateTime(), default=current_timestamp())
    stack_configuration = Column("stack_configuration", Text, default="{}")
    stack_output = Column("stack_output", Text, default="{}")
