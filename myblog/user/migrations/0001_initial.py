# Generated by Django 2.1.5 on 2019-01-15 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('u_name', models.CharField(max_length=10, verbose_name='姓名')),
                ('u_password', models.CharField(max_length=150, verbose_name='密码')),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
