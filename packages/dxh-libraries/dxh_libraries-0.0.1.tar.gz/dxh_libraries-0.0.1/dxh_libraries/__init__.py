from .allauth import GoogleOAuth2Adapter, FacebookOAuth2Adapter
from .celery import shared_task 
from .__version__ import (  
__version__,
)

__all__ = ["GoogleOAuth2Adapter", "FacebookOAuth2Adapter", "shared_task"]