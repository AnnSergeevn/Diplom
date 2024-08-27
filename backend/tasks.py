import yaml
from .models import Category, Parameter, ProductParameter, Product, Shop
from celery import shared_task
from .signals import password_reset_token_created
from netology_pd_diplom.celery import app


@shared_task
def send_email(sender, instance, reset_password_token, **kwargs):
    # Your email sending logic here
    return password_reset_token_created(sender, instance, reset_password_token, **kwargs)


def open_file(shop):
    with open(shop.get_file(), 'r') as f:
        data = yaml.safe_load(f)
    return data


@app.task
def do_import(data, user_id):
    file = open_file(data)

    shop, _ = Shop.objects.get_or_create(user_id=user_id,
                                         defaults={'name': file['shop']})

    load_cat = [
        Category(id=category['id'], name=category['name']) for category in file['categories']
    ]
    Category.objects.bulk_create(load_cat)

    Product.objects.filter(shop_id=shop.id).delete()

    load_prod = []
    product_id = {}
    load_pp = []
    for item in file['goods']:
        load_prod.append(Product(name=item['name'],
                                 category_id=item['category'],
                                 model=item['model'],
                                 external_id=item['id'],
                                 shop_id=shop.id,
                                 quantity=item['quantity'],
                                 price=item['price'],
                                 price_rrc=item['price_rrc']))
        product_id[item['id']] = {}

        for name, value in item['parameters'].items():
            parameter, _ = Parameter.objects.get_or_create(name=name)
            product_id[item['id']].update({parameter.id: value})
            load_pp.append(ProductParameter(product_id=product_id[item['id']][parameter.id],
                                            parameter_id=parameter.id,
                                            value=value))
    Product.objects.bulk_create(load_prod)
    ProductParameter.objects.bulk_create(load_pp)