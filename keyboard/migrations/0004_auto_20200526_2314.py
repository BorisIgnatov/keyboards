# Generated by Django 3.0.4 on 2020-05-26 17:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('keyboard', '0003_switch_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyboardImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='keyboard/images/')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='review/images/')),
            ],
        ),
        migrations.RemoveField(
            model_name='keyboard',
            name='image',
        ),
        migrations.AddField(
            model_name='keyboard',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='keyboard',
            name='rating',
            field=models.FloatField(default=0),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField()),
                ('content', models.TextField()),
                ('is_positive', models.BooleanField()),
                ('images', models.ManyToManyField(to='keyboard.ReviewImage')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='keyboard',
            name='images',
            field=models.ManyToManyField(to='keyboard.KeyboardImage'),
        ),
    ]
