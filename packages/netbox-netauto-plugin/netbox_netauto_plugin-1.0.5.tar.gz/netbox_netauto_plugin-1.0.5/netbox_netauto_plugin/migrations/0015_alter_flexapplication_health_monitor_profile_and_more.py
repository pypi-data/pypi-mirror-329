# Generated by Django 5.0.9 on 2024-10-30 20:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_netauto_plugin', '0014_alter_profile_options_alter_flexapplication_tcp_wan_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flexapplication',
            name='health_monitor_profile',
            field=models.ForeignKey(blank=True, limit_choices_to={'type': 'health_monitor'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='netbox_netauto_plugin.profile'),
        ),
        migrations.AlterField(
            model_name='flexapplication',
            name='status',
            field=models.CharField(default='create', editable=False, max_length=20),
        ),
        migrations.AlterField(
            model_name='l4application',
            name='health_monitor_profile',
            field=models.ForeignKey(blank=True, limit_choices_to={'type': 'health_monitor'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='netbox_netauto_plugin.profile'),
        ),
        migrations.AlterField(
            model_name='l4application',
            name='status',
            field=models.CharField(default='create', editable=False, max_length=20),
        ),
        migrations.AlterField(
            model_name='mtlsapplication',
            name='health_monitor_profile',
            field=models.ForeignKey(blank=True, limit_choices_to={'type': 'health_monitor'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='netbox_netauto_plugin.profile'),
        ),
        migrations.AlterField(
            model_name='mtlsapplication',
            name='status',
            field=models.CharField(default='create', editable=False, max_length=20),
        ),
    ]
