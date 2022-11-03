from alembic import command as alembic_commands
from alembic.config import Config

alembic_configuration = Config("alembic.ini")


def run_migration(migration_type: str, revision: str):

    try:
        getattr(alembic_commands, migration_type)(alembic_configuration, revision)
    except Exception as err:  # pylint: disable=W0703
        print(err)
