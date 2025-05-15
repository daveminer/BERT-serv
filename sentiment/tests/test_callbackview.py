import json
import pytest
from django.test import RequestFactory
from django.urls import reverse
from sentiment.views.callbackview import SentimentCallback
from sentiment.models import Sentiment

@pytest.fixture
def factory():
    return RequestFactory()

@pytest.fixture
def sentiment_record(db):
    return Sentiment.objects.create(
        id=5,
        label="Positive",
        score=0.8,
        tags=["stock"],
        text="year over year growth is increasing"
    )

@pytest.mark.django_db
def test_valid_callback_request(factory, sentiment_record):
    """Test a valid callback request that updates a sentiment record."""
    view = SentimentCallback.as_view()
    data = {
        "results": [{
            "article_id": 5,
            "sentiment": {
                "label": "Negative",
                "score": 0.9,
                "tags": ["stock", "growth"]
            }
        }]
    }
    request = factory.post(
        reverse('sentiment-callback'),
        data=json.dumps(data),
        content_type='application/json'
    )
    
    response = view(request)
    
    assert response.status_code == 200
    response_data = json.loads(response.content)
    assert response_data["updated_count"] == 1
    assert not response_data["errors"]
    
    # Verify the record was updated
    updated_record = Sentiment.objects.get(id=5)
    assert updated_record.label == "Negative"
    assert updated_record.score == 0.9
    assert updated_record.tags == ["stock", "growth"]

@pytest.mark.django_db
def test_missing_results_field(factory):
    """Test request with missing 'results' field."""
    view = SentimentCallback.as_view()
    data = [{
        "article_id": 5,
        "tags": ["stock"],
        "text": "year over year growth is increasing"
    }]
    request = factory.post(
        reverse('sentiment-callback'),
        data=json.dumps(data),
        content_type='application/json'
    )
    
    response = view(request)
    
    assert response.status_code == 400
    response_data = json.loads(response.content)
    assert "error" in response_data
    assert "results" in response_data["error"].lower()

@pytest.mark.django_db
def test_results_not_list(factory):
    """Test request where 'results' is not a list."""
    view = SentimentCallback.as_view()
    data = {
        "results": {
            "article_id": 5,
            "tags": ["stock"],
            "text": "year over year growth is increasing"
        }
    }
    request = factory.post(
        reverse('sentiment-callback'),
        data=json.dumps(data),
        content_type='application/json'
    )
    
    response = view(request)
    
    assert response.status_code == 400
    response_data = json.loads(response.content)
    assert "error" in response_data
    assert "list" in response_data["error"].lower()

@pytest.mark.django_db
def test_invalid_result_format(factory):
    """Test request with invalid result format."""
    view = SentimentCallback.as_view()
    data = {
        "results": ["invalid", "format"]
    }
    request = factory.post(
        reverse('sentiment-callback'),
        data=json.dumps(data),
        content_type='application/json'
    )
    
    response = view(request)
    
    assert response.status_code == 207
    response_data = json.loads(response.content)
    assert response_data["updated_count"] == 0
    assert len(response_data["errors"]) == 2

@pytest.mark.django_db
def test_missing_article_id_or_sentiment(factory):
    """Test request with missing article_id or sentiment data."""
    view = SentimentCallback.as_view()
    data = {
        "results": [
            {"article_id": 5},  # missing sentiment
            {"sentiment": {"label": "Positive"}},  # missing article_id
            {"article_id": 5, "sentiment": {}}  # empty sentiment
        ]
    }
    request = factory.post(
        reverse('sentiment-callback'),
        data=json.dumps(data),
        content_type='application/json'
    )
    
    response = view(request)
    
    assert response.status_code == 207
    response_data = json.loads(response.content)
    assert response_data["updated_count"] == 0
    assert len(response_data["errors"]) == 3

@pytest.mark.django_db
def test_nonexistent_article_id(factory):
    """Test request with non-existent article_id."""
    view = SentimentCallback.as_view()
    data = {
        "results": [{
            "article_id": 999,
            "sentiment": {
                "label": "Positive",
                "score": 0.8
            }
        }]
    }
    request = factory.post(
        reverse('sentiment-callback'),
        data=json.dumps(data),
        content_type='application/json'
    )
    
    response = view(request)
    
    assert response.status_code == 207
    response_data = json.loads(response.content)
    assert response_data["updated_count"] == 0
    assert len(response_data["errors"]) == 1
    assert "not found" in response_data["errors"][0]

@pytest.mark.django_db
def test_invalid_json(factory):
    """Test request with invalid JSON."""
    view = SentimentCallback.as_view()
    request = factory.post(
        reverse('sentiment-callback'),
        data="invalid json",
        content_type='application/json'
    )
    
    response = view(request)
    
    assert response.status_code == 400
    response_data = json.loads(response.content)
    assert "error" in response_data
    assert "JSON" in response_data["error"]

@pytest.mark.django_db
def test_partial_success(factory, sentiment_record):
    """Test request with some valid and some invalid records."""
    view = SentimentCallback.as_view()
    data = {
        "results": [
            {
                "article_id": 5,
                "sentiment": {
                    "label": "Negative",
                    "score": 0.9
                }
            },
            {
                "article_id": 999,
                "sentiment": {
                    "label": "Positive",
                    "score": 0.8
                }
            }
        ]
    }
    request = factory.post(
        reverse('sentiment-callback'),
        data=json.dumps(data),
        content_type='application/json'
    )
    
    response = view(request)
    
    assert response.status_code == 207
    response_data = json.loads(response.content)
    assert response_data["updated_count"] == 1
    assert len(response_data["errors"]) == 1
    
    # Verify the valid record was updated
    updated_record = Sentiment.objects.get(id=5)
    assert updated_record.label == "Negative"
    assert updated_record.score == 0.9 