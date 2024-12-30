from sqlalchemy import Delete, Update
from sqlalchemy.sql.functions import current_timestamp

from app.db.db import session_maker
from app.db.models.db_model import StackConfiguration


def add(project_name: str, stack_name: str, stack_configuration: str = "{}",
        stack_output: str = "{}") -> StackConfiguration:
    with session_maker.begin() as session:
        stack_config = StackConfiguration()
        stack_config.project_name = project_name
        stack_config.stack_name = stack_name
        stack_config.stack_configuration = stack_configuration
        stack_config.stack_output = stack_output

        session.add(stack_config)
        session.flush()

        return stack_config


def update(
        id: int,
        project_name: str,
        stack_name: str,
        stack_configuration: str = "{}",
        stack_output: str = "{}"
) -> None:
    with session_maker.begin() as session:
        session.execute(
            Update(StackConfiguration)
            .where(StackConfiguration.id == id)
            .values({
                StackConfiguration.project_name: project_name,
                StackConfiguration.stack_name: stack_name,
                StackConfiguration.stack_configuration: stack_configuration,
                StackConfiguration.stack_output: stack_output,
                StackConfiguration.updated_at: current_timestamp()
            })
        )


def delete(id: int) -> None:
    with session_maker.begin() as session:
        session.execute(Delete(StackConfiguration).where(StackConfiguration.id == id))


def get(limit: int = 1000, offset: int = 0) -> list[StackConfiguration]:
    with session_maker() as session:
        return session.query(StackConfiguration).limit(limit).offset(offset).all()


def get_by_id(id: int) -> StackConfiguration | None:
    with session_maker() as session:
        return session.query(StackConfiguration).where(
            StackConfiguration.id == id
        ).first()


def get_by_project_name(project_name: str) -> list[StackConfiguration]:
    with session_maker.begin() as session:
        return session.query(StackConfiguration).where(
            StackConfiguration.project_name == project_name
        ).all()


def get_by_stack_name(stack_name: str) -> list[StackConfiguration]:
    with session_maker.begin() as session:
        return session.query(StackConfiguration).where(
            StackConfiguration.stack_name == stack_name
        ).all()


def get_by_project_and_stack(project_name: str, stack_name: str) -> StackConfiguration | None:
    with session_maker.begin() as session:
        return session.query(StackConfiguration).where(
            StackConfiguration.project_name == project_name,
            StackConfiguration.stack_name == stack_name
        ).one_or_none()
