# Generated by Django 2.0 on 2017-12-03 01:32

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Custom primary key represented by a UUID', primary_key=True, serialize=False)),
                ('active', models.BooleanField(db_index=True, default=True, help_text='Whether the vehicle in active service')),
                ('current_location', django.contrib.gis.db.models.fields.PointField(blank=True, help_text='The coordinates representing the vehicles current location', null=True, srid=4326)),
                ('current_bearing', models.IntegerField(blank=True, help_text='The current bearing (direction of travel, in degrees) of the vehicle', null=True)),
                ('last_update_at', models.DateTimeField(blank=True, help_text='When the vehicle last reported its location', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VehicleLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('at', models.DateTimeField()),
                ('vehicle', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.PROTECT, related_name='location_updates', to='vehicles.Vehicle')),
            ],
        ),
    ]
