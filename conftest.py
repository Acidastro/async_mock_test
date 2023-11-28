from unittest.mock import AsyncMock, patch, Mock

import pytest

from database.api import FindReqDB
from database.core import get_clients_review, get_conn
from review_module.models.review_models import ClientsReviewModel
from review_module.review import CheckReviewChain, ReviewManagerDB
from tests.conftests import account_file, get_file, conn, logger
from utilities.models import RecordHook

path_ = 'data/'
# path_ = 'review_module/tests/data/'

@pytest.fixture
def fixture_mock_db_manager(fixture_mock_get_records_for_phones):
    with patch('sendout.sendout_core.sendout_analyze.SendoutManagerDB', new_callable=Mock) as _mock:
        _mock.return_value = fixture_mock_get_records_for_phones
        yield _mock


@pytest.fixture
def fixture_mock_get_records_for_phones():
    file = get_file(_path + "records_for_phones.json")
    file.sort(key=lambda x: x['datetime'], reverse=True)

    records_for_phones = AsyncMock()
    records_for_phones.get_records_for_phones.return_value = file
    return records_for_phones


@pytest.fixture
def client_review():
    return get_clients_review(get_conn())


@pytest.fixture
@patch.object(ReviewManagerDB, '__init__', return_value=None)
@patch('review_module.review.ReviewManagerDB.get_records', new_callable=AsyncMock)
@patch('review_module.review.ReviewManagerDB.get_account', new_callable=AsyncMock)
@patch('review_module.review.ReviewManagerDB.get_client_review', new_callable=AsyncMock)
def mock_class_review(
        mock_get_client_review,
        mock_get_account,
        mock_get_records,
        _,
        client_review_model,
        get_records_file,
        account_file,
        conn,
        logger,
        ):
    mock_get_client_review.return_value = client_review_model
    mock_get_account.return_value = account_file
    mock_get_records.return_value = get_records_file
    cr = CheckReviewChain(conn, '79885883848', 'testos', logger)
    cr.db.conn = Mock(return_value=None)
    cr.db.update_client_review_custom = AsyncMock()
    return cr


@pytest.fixture
def client_acc():
    file = get_file(path_ + 'client_rewiew_acc.json')
    return file


@pytest.fixture
def client_review_model():
    file = get_file(path_ + 'client_rewiew_acc.json')
    res = ClientsReviewModel(**file)
    return res


@pytest.fixture
def get_records_file():
    file = get_file(path_ + 'records.json')
    res = [RecordHook(**file)]
    return res
