# Generated by Django 5.0.9 on 2024-09-30 14:19

import netbox_netauto_plugin.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipam', '0070_vlangroup_vlan_id_ranges'),
        ('netbox_netauto_plugin', '0009_alter_flexapplication_health_monitor_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flexapplication',
            old_name='dst_address',
            new_name='virtual_ip_address',
        ),
        migrations.RenameField(
            model_name='flexapplication',
            old_name='dst_address_string',
            new_name='virtual_ip_address_string',
        ),
        migrations.RenameField(
            model_name='flexapplication',
            old_name='dst_port',
            new_name='virtual_port',
        ),
        migrations.RenameField(
            model_name='l4application',
            old_name='dst_address',
            new_name='virtual_ip_address',
        ),
        migrations.RenameField(
            model_name='l4application',
            old_name='dst_address_string',
            new_name='virtual_ip_address_string',
        ),
        migrations.RenameField(
            model_name='l4application',
            old_name='dst_port',
            new_name='virtual_port',
        ),
        migrations.RenameField(
            model_name='mtlsapplication',
            old_name='dst_address',
            new_name='virtual_ip_address',
        ),
        migrations.RenameField(
            model_name='mtlsapplication',
            old_name='dst_address_string',
            new_name='virtual_ip_address_string',
        ),
        migrations.RenameField(
            model_name='mtlsapplication',
            old_name='dst_port',
            new_name='virtual_port',
        ),
        migrations.AddField(
            model_name='flexapplication',
            name='member_ip_addresses',
            field=models.ManyToManyField(blank=True, related_name='+', to='ipam.ipaddress'),
        ),
        migrations.AddField(
            model_name='flexapplication',
            name='member_ip_addresses_string',
            field=models.CharField(blank=True, max_length=500, null=True, validators=[netbox_netauto_plugin.validators.validate_cidr_list]),
        ),
        migrations.AddField(
            model_name='flexapplication',
            name='member_port',
            field=models.PositiveIntegerField(default=80),
        ),
        migrations.AddField(
            model_name='l4application',
            name='member_ip_addresses',
            field=models.ManyToManyField(blank=True, related_name='+', to='ipam.ipaddress'),
        ),
        migrations.AddField(
            model_name='l4application',
            name='member_ip_addresses_string',
            field=models.CharField(blank=True, max_length=500, null=True, validators=[netbox_netauto_plugin.validators.validate_cidr_list]),
        ),
        migrations.AddField(
            model_name='l4application',
            name='member_port',
            field=models.PositiveIntegerField(default=80),
        ),
        migrations.AddField(
            model_name='mtlsapplication',
            name='member_ip_addresses',
            field=models.ManyToManyField(blank=True, related_name='+', to='ipam.ipaddress'),
        ),
        migrations.AddField(
            model_name='mtlsapplication',
            name='member_ip_addresses_string',
            field=models.CharField(blank=True, max_length=500, null=True, validators=[netbox_netauto_plugin.validators.validate_cidr_list]),
        ),
        migrations.AddField(
            model_name='mtlsapplication',
            name='member_port',
            field=models.PositiveIntegerField(default=80),
        ),
    ]
