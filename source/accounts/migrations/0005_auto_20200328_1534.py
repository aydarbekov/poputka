# Generated by Django 2.2 on 2020-03-28 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200328_0537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profiles',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='users_photo', verbose_name='Фото'),
        ),
    ]
