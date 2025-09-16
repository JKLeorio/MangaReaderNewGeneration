import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from settings import DATABASE_URL, DEBUG

test_database_engine = create_engine(DATABASE_URL, echo=True if DEBUG else False)
test_session_maker = sessionmaker(test_database_engine)
test_scoped_session = test_session_maker()


@pytest.fixture(scope="session")
def session():
    return test_scoped_session