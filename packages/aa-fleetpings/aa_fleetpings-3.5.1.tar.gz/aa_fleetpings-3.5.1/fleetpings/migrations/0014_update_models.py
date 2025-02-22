# Generated by Django 4.0.10 on 2023-06-23 10:49

# Django
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("fleetpings", "0013_fleetcomm_channel"),
    ]

    operations = [
        migrations.AlterField(
            model_name="discordpingtargets",
            name="restricted_to_group",
            field=models.ManyToManyField(
                blank=True,
                help_text="Restrict ping rights to the following groups …",
                related_name="discord_role_require_groups",
                to="auth.group",
                verbose_name="Group restrictions",
            ),
        ),
        migrations.AlterField(
            model_name="fleetdoctrine",
            name="restricted_to_group",
            field=models.ManyToManyField(
                blank=True,
                help_text="Restrict this doctrine to the following groups …",
                related_name="fleetdoctrine_require_groups",
                to="auth.group",
                verbose_name="Group restrictions",
            ),
        ),
        migrations.AlterField(
            model_name="fleettype",
            name="restricted_to_group",
            field=models.ManyToManyField(
                blank=True,
                help_text="Restrict this fleet type to the following groups …",
                related_name="fleettype_require_groups",
                to="auth.group",
                verbose_name="Group restrictions",
            ),
        ),
        migrations.AlterField(
            model_name="webhook",
            name="restricted_to_group",
            field=models.ManyToManyField(
                blank=True,
                help_text="Restrict ping rights to the following groups …",
                related_name="webhook_require_groups",
                to="auth.group",
                verbose_name="Group restrictions",
            ),
        ),
        migrations.RenameModel(
            old_name="DiscordPingTargets",
            new_name="DiscordPingTarget",
        ),
    ]
