from alembic import command as alembic_commands
from alembic.config import Config

from src.database import Session, BaseModel

alembic_configuration = Config("alembic.ini")


def run_migration(migration_type: str, revision: str):

    try:
        getattr(alembic_commands, migration_type)(alembic_configuration, revision)
    except Exception as err:  # pylint: disable=W0703
        print(err)


def update_object(
        db: Session,
        model: BaseModel,
        args: dict
) -> None:
    """
    Update one sqlalchemy object

    :param db: Database connection
    :param model: Database object that will be updated
    :param args: Fields to update
    :return:
    """
    for attr, value in args.items():
        setattr(model, attr, value)
    db.commit()
