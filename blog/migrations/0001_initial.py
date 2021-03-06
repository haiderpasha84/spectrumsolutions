# Generated by Django 3.2 on 2021-05-12 05:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='post',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default='', max_length=255)),
                ('slug', models.CharField(max_length=130)),
                ('timeStamp', models.DateTimeField()),
                ('thumbnail', models.ImageField(default='', upload_to='shop/images')),
                ('status', models.BooleanField(default='False')),
                ('content', tinymce.models.HTMLField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            managers=[
                ('acceptpost', django.db.models.manager.Manager()),
            ],
        ),
    ]
