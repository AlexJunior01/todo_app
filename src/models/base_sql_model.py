from typing import List

from sqlalchemy.exc import SQLAlchemyError

from src.database import Session


class BaseSQLModel:
    """Basic CRUD for models"""

    # TODO add correct documentation to each function of the class
    def update(self, db: Session, update_args: dict):
        try:
            for attr, value in update_args.items():
                setattr(self, attr, value)
            db.commit()
            return True, None
        except SQLAlchemyError as error:
            return False, ''.join(error.args)

    def save(self, db: Session):
        """
        Save a project instance in the database
        :param db: Database connection
        :return: Tuple(was_saved, error_description)
        """
        try:
            db.add(self)
            db.commit()
            return True, None
        except SQLAlchemyError as error:
            return False, ''.join(error.args)

    def delete(self, db: Session):
        """
        Delete a task instance from the database
        :param db: Database connection
        :return:
        """
        try:
            db.delete(self)
            db.commit()
            return True, None
        except SQLAlchemyError as error:
            return False, ''.join(error.args)
