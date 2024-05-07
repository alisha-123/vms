# Generated by Django 4.2.11 on 2024-04-28 17:09

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('vendor_code', models.CharField(default=uuid.uuid4, max_length=36, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('contact_details', models.TextField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('on_time_delivery_rate', models.FloatField(default=0.0)),
                ('quality_rating_avg', models.FloatField(default=0.0)),
                ('average_response_time', models.FloatField(default=0.0)),
                ('fulfillment_rate', models.FloatField(default=0.0)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]