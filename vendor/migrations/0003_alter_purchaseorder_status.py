# Generated by Django 5.0 on 2023-12-09 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_alter_vendor_average_response_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('completed', 'completed'), ('in progress', 'in progress'), ('acknowleged', 'acknowleged'), ('on hold', 'on hold'), ('cancelled', 'cancelled')], max_length=50),
        ),
    ]
