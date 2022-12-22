import pytest
from .models import Sentiment
from torch import Tensor


@pytest.mark.django_db(True)
@pytest.fixture
def test_success(mocker):
    mocker.patch('sentiment.models.Sentiment.finbert',
                 return_value=Tensor([[3.7920, -4.8535, -2.6651]]))

    sentiments_before = __count_sentiments()

    Sentiment.run(sentences=['Test sentiment sentence.'])

    assert __count_sentiments() == sentiments_before + 1


def __count_sentiments():
    return Sentiment.objects.all().count()
