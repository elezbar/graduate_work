# celery -A sheduler beat --loglevel=INFO
# celery -A sheduler worker --loglevel=INFO --pool=solo
# docker exec db psql -U app -d movies_database -f database.ddl