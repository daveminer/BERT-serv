import pytest

from .models import Sentiment


@pytest.mark.django_db(True)
def test_success():
    sentiments_before = __count_sentiments()

    Sentiment.run(sentences=["Test sentiment sentence."])

    assert __count_sentiments() == sentiments_before + 1


def __count_sentiments():
    return Sentiment.objects.all().count()
