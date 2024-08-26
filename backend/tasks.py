from .models import Category, Parameter, ProductParameter, Product, Shop
from celery import shared_task
from .signals import password_reset_token_created

@shared_task
def send_email(sender, instance, reset_password_token, **kwargs):
    # Your email sending logic here
    return password_reset_token_created(sender, instance, reset_password_token, **kwargs)


@shared_task
def do_import(backend):
    try:
        module = __import__(backend)
        print(f"Successfully imported module: {backend}")
    except ImportError:
        print(f"Failed to import module: {backend}")
