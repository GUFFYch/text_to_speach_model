# Generated by Django 4.2.4 on 2023-09-19 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=200)),
                ('speed', models.FloatField(default=1.0)),
                ('color', models.CharField(default='FFFFFF', max_length=6)),
            ],
        ),
    ]
