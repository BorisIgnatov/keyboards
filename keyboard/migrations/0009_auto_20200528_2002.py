# Generated by Django 3.0.4 on 2020-05-28 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keyboard', '0008_auto_20200528_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewimage',
            name='image',
            field=models.ImageField(upload_to='review/images/'),
        ),
    ]
