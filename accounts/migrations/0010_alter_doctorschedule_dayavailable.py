# Generated by Django 3.2.9 on 2022-01-24 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20220104_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorschedule',
            name='dayAvailable',
            field=models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednseday', 'Wednseday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday')], max_length=40),
        ),
    ]
