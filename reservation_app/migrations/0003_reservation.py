# Generated by Django 5.0.2 on 2024-02-09 13:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_app', '0002_alter_room_projector'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('comment', models.TextField()),
                ('room_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation_app.room')),
            ],
        ),
    ]
