from django.core.exceptions import BadRequest
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from ..models import Sentiment
import json
import logging

logger = logging.getLogger(__name__)

class SentimentCallback(View):
    def post(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body)
            if not isinstance(body, dict) or 'results' not in body:
                logger.warning("Invalid request format - missing 'results' field", extra={
                    "body": request.body.decode('utf-8', errors='replace')
                })
                return JsonResponse({
                    "error": "Request body must contain a 'results' field"
                }, status=400)
            
            results = body['results']
            if not isinstance(results, list):
                logger.warning("Invalid request format - 'results' is not a list", extra={
                    "results_type": type(results).__name__
                })
                return JsonResponse({
                    "error": "'results' must be a list"
                }, status=400)
            
            updated_count = 0
            errors = []
            
            for result in results:
                if not isinstance(result, dict):
                    errors.append("Invalid result format - not a dictionary")
                    continue
                
                article_id = result.get('article_id')
                sentiment_data = result.get('sentiment', {})
                
                if not article_id or not sentiment_data:
                    errors.append(f"Missing article_id or sentiment data for item {len(errors) + 1}")
                    continue
                
                try:
                    sentiment = Sentiment.objects.get(id=article_id)
                    sentiment.label = sentiment_data.get('label', sentiment.label)
                    sentiment.score = sentiment_data.get('score', sentiment.score)
                    sentiment.tags = sentiment_data.get('tags', sentiment.tags)
                    sentiment.save()
                    updated_count += 1
                    logger.info(f"Updated sentiment record {article_id}", extra={
                        "article_id": article_id,
                        "updated_fields": list(sentiment_data.keys())
                    })
                except Sentiment.DoesNotExist:
                    errors.append(f"Sentiment record with ID {article_id} not found")
                    continue
            
            response_data = {
                "updated_count": updated_count,
                "errors": errors
            }
            
            if errors:
                logger.warning("Partial success in callback processing", extra=response_data)
                return JsonResponse(response_data, status=207)  # Multi-Status
            
            logger.info("Successfully processed callback", extra={"updated_count": updated_count})
            return JsonResponse(response_data, status=200)
            
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON in request body", extra={
                "error": str(e),
                "body": request.body.decode('utf-8', errors='replace')
            })
            return JsonResponse({
                "error": "Could not parse request body as JSON"
            }, status=400)
        except Exception as e:
            logger.error("Unexpected error in callback processing", extra={
                "error": str(e),
                "error_type": type(e).__name__,
                "body": request.body.decode('utf-8', errors='replace')
            }, exc_info=True)
            return JsonResponse({
                "error": "Internal server error",
                "message": str(e)
            }, status=500) 