# Generated by Django 4.2.7 on 2023-11-15 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_rename_member_user_id_address_member_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(max_length=100, null=True),
        ),
    ]