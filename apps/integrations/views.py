from rest_framework.views import APIView
from rest_framework.response import Response
from .models import IntegrationEvent, OAuthConnection
from .tasks import process_event
from apps.common.utils import rate_limit
from django.utils import timezone
import secrets
from datetime import timedelta

# OAuth
class OAuthConnectView(APIView):
    def post(self, request):
        access_token = secrets.token_urlsafe(32)
        refresh_token = secrets.token_urlsafe(32)
        connection = OAuthConnection.objects.create(
            provider="hubspot",
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=timezone.now() + timedelta(hours=1)
        )
        return Response({"connection_id": connection.id, "access_token": access_token})

# Webhook
class WebhookView(APIView):
    def post(self, request):
        ip = request.META.get("REMOTE_ADDR")
        if not rate_limit(f"rate:{ip}"):
            return Response({"error": "rate limit exceeded"}, status=429)

        idempotency_key = request.headers.get("Idempotency-Key")
        if idempotency_key:
            existing = IntegrationEvent.objects.filter(idempotency_key=idempotency_key).first()
            if existing:
                return Response({"event_id": existing.id, "status": existing.status, "idempotent": True})

        event = IntegrationEvent.objects.create(
            source="hubspot",
            event_type=request.data.get("event_type"),
            payload=request.data,
            idempotency_key=idempotency_key
        )

        process_event.delay(str(event.id))
        return Response({"event_id": event.id, "status": "accepted"})

# Monitoring
from django.db.models import Count
class MonitoringView(APIView):
    def get(self, request):
        stats = IntegrationEvent.objects.values("status").annotate(count=Count("id"))
        total = IntegrationEvent.objects.count()
        return Response({"total_events": total, "by_status": stats, "system": "healthy"})