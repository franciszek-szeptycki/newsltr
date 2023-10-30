# Generated by Django 4.2.6 on 2023-10-26 14:54

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("workspaces", "0007_alter_workspaceapikey_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="Campaign",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "workspace",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="campaign_workspace",
                        to="workspaces.workspace",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CampaignSubscriber",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "email",
                    models.EmailField(max_length=254, verbose_name="subscriber email"),
                ),
                ("joined_at", models.DateTimeField(auto_now_add=True)),
                ("tracking_data", models.JSONField(blank=True, null=True)),
                (
                    "campaign",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="campaigns.campaign",
                    ),
                ),
            ],
            options={
                "ordering": ["joined_at"],
                "unique_together": {("email", "campaign")},
            },
        ),
    ]
