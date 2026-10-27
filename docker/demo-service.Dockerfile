FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY scripts/demo_service.py /app/demo_service.py

EXPOSE 8080

CMD ["sh", "-c", "python /app/demo_service.py --host 0.0.0.0 --port 8080 --ready-after ${READY_AFTER:-10}"]