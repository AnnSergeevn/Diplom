import yaml
from .models import Category, Parameter, ProductParameter, Product, Shop, ProductInfo
from celery import shared_task
from .signals import password_reset_token_created
from netology_pd_diplom.celery import app
from requests import get
from yaml import load as load_yaml, Loader

@shared_task
def send_email(sender, instance, reset_password_token, **kwargs):
    # Your email sending logic here
    return password_reset_token_created(sender, instance, reset_password_token, **kwargs)



@app.task
def do_import(url, user_id):
    stream = get(url).content
    data = load_yaml(stream, Loader=Loader)
    shop, _ = Shop.objects.get_or_create(name=data['shop'], user_id=request.user.id)
    for category in data['categories']:
        category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
        category_object.shops.add(shop.id)
        category_object.save()
    ProductInfo.objects.filter(shop_id=shop.id).delete()
    for item in data['goods']:
        product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])

        product_info = ProductInfo.objects.create(product_id=product.id,
                                                  external_id=item['id'],
                                                  model=item['model'],
                                                  price=item['price'],
                                                  price_rrc=item['price_rrc'],
                                                  quantity=item['quantity'],
                                                  shop_id=shop.id)
        for name, value in item['parameters'].items():
            parameter_object, _ = Parameter.objects.get_or_create(name=name)
            ProductParameter.objects.create(product_info_id=product_info.id,
                                            parameter_id=parameter_object.id,
                                            value=value)
