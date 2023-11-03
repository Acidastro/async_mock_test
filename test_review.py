from unittest.mock import AsyncMock, patch

import pytest


@pytest.mark.parametrize(
    ('text', 'review', 'status'), [
        ('Первый тестовый текст, поэтому мне всё понравилось', True, 'Next estimate step send'),
    ])
@patch('review_module.review.send_tmsg_to_queue', new_callable=AsyncMock)
@patch('review_module.review.send_message_to_queue', new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_check_review_positive(
        send_message_to_queue,
        send_tmsg_to_queue,
        text, review, status, mock_class_review):
    """ EST TEST 1 step (est, est, wait_comment) with {} """
    res = await mock_class_review.check_review(text)
    assert res.ok == review
    assert res.status == status
