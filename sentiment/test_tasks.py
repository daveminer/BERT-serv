import json
import numpy
import pytest
from .tasks import run_sentiment

@pytest.mark.django_db(True)
@pytest.mark.filterwarnings("ignore:entry_points")
def test_run_sentiment(mocker):
    mock_finbert = mocker.patch('sentiment.tasks.finbert')

    fake_finbert_return = numpy.array(
        [[ 3.6286101, -4.290355, -2.529494 ], [ -1.0189443, 4.5508056, -5.3832393]]
    )
    mock_finbert().__getitem__().detach().numpy.return_value = fake_finbert_return

    mock_results = run_sentiment.s(
        ["Stonks go up.", "For great justice."]
    ).apply().get()

    assert mock_results == json.dumps({'ids': [1, 2]})
