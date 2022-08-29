# Generated by Django 4.1 on 2022-08-22 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crm', models.CharField(max_length=150)),
                ('passwd', models.CharField(max_length=150)),
                ('icon', models.ImageField(null=True, upload_to='avatars/%Y/%m/%d')),
            ],
        ),
    ]
