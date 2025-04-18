# Generated by Django 4.2.20 on 2025-04-11 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0008_alter_cartitem_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cartitem",
            name="cart",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="items",
                to="store.cart",
            ),
        ),
    ]
