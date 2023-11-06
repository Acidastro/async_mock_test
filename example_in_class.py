@pytest.fixture
def fixture_mock_get_by_id_client_1():
    mock_get_by_id = Mock()
    mock_get_by_id.return_value = get_file(path_ + 'client_categories_1.json')
    with patch.object(Clients, 'get_by_id', new=mock_get_by_id), \
            patch.object(CheckMsg, 'conn', new_callable=PropertyMock(return_value=None)):
        yield

@pytest.mark.asyncio
async def test_check_client_category_1(fixture_mock_get_by_id_client_1):
    example = Example()
    res = await checker.check_client_category()
    assert res


class Example:
  
  async def check_client_category(self):
    client = target.Clients(self.account.crm_data).get_by_id(self.record.data.client.id)
    return True
