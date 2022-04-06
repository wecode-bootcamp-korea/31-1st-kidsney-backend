# Generated by Django 4.0.3 on 2022-04-06 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('products', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('quantity', models.IntegerField(default=0)),
                ('product_size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carts', to='products.productsize')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carts', to='users.user')),
            ],
            options={
                'db_table': 'carts',
            },
        ),
    ]
