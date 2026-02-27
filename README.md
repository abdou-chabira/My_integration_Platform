# Django Integration Platform

Features:

- OAuth integration simulation
- HubSpot API simulation
- Webhook handling with idempotency
- Rate limiting
- Monitoring endpoint
- Async processing with Celery + Redis
- Docker deployment
- Production-ready folder structure

## Run locally

1. docker-compose up --build
2. POST /api/oauth/connect/ to create OAuth connection
3. POST /api/webhook/ with Idempotency-Key header
4. GET /api/monitoring/ for stats
