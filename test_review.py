from unittest.mock import AsyncMock, patch


async def foo():
    match = {'phone': "7988866325418"}
    result = [x async for x in await FindReqDB(match).find()]
    return result


@patch('database.api.FindReqDB.find', new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_my_function(mock_find):
    async def async_generator():
        yield "test_value"

    mock_find.return_value = async_generator()

    result = await foo()
    print(result)
    assert result == ["test_value"]
    mock_find.assert_called_once()
    mock_find.assert_called()
