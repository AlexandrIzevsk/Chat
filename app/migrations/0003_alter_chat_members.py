# Generated by Django 5.1.7 on 2025-03-19 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_chat_chatcustomer_chat_members_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='members',
            field=models.ManyToManyField(related_name='rooms', through='app.ChatCustomer', to='app.customer'),
        ),
    ]
