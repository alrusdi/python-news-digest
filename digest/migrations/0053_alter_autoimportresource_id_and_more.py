# Generated by Django 4.1.3 on 2022-12-04 14:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("digest", "0052_alter_item_article_path_alter_keyword_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="activated_at",
            field=models.DateTimeField(
                db_index=True,
                default=datetime.datetime.now,
                verbose_name="Activated date",
            ),
        ),
    ]
