import json
from fastapi import APIRouter, Depends
from jinja2 import Template, Environment, meta
from core.config import settings
from db.broker import get_brokers
from schemas.send_notification import DelayedNotification, InstantNotification

router = APIRouter(prefix='/send_notification')


@router.post('/instant',
             summary="Instant",
             description="Send instant notification to workers")
async def send_instant(*, form: InstantNotification, brokers=Depends(get_brokers)):
    tm = Template(form.template)
    env = Environment()
    parsed_content = env.parse(tm)
    tokens = meta.find_undeclared_variables(parsed_content)
    incorrect_variables = set(tokens) - set(settings.correct_variables)
    if incorrect_variables:
        raise ValueError('incorrect variables in template')
    brokers[settings.name_instant_queues].push(json.dumps(form.dict()))


@router.post('/delayed',
             summary="Delayed",
             description="Send delayed notifications to workers")
async def send_delayed(*, form: DelayedNotification, brokers=Depends(get_brokers)):
    brokers[settings.name_delayed_queues].push(json.dumps(form.dict()))
