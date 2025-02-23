from .utils.celery_init import celery_app
from .utils.tasks import *  # This will import everything defined in tasks.__all__

__all__ = ['celery_app']
