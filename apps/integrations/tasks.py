from celery import shared_task
from .models import IntegrationEvent, OAuthConnection
from .services import HubspotClient

@shared_task(bind=True, max_retries=3)
def process_event(self, event_id):
    event = IntegrationEvent.objects.get(id=event_id)

    try:
        connection = OAuthConnection.objects.first()
        client = HubspotClient(connection.access_token)
        client.create_contact(event.payload)

        event.status = "completed"
        event.save()
    except Exception as exc:
        event.retry_count += 1
        event.status = "failed"
        event.save()
        raise self.retry(exc=exc, countdown=2 ** event.retry_count)