# Generated by Django 4.2.6 on 2023-10-27 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("workspaces", "0007_alter_workspaceapikey_id"),
        ("campaigns", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="campaign",
            name="workspace",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="campaign",
                to="workspaces.workspace",
            ),
        ),
        migrations.AlterField(
            model_name="campaignsubscriber",
            name="campaign",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="subscribers",
                to="campaigns.campaign",
            ),
        ),
    ]