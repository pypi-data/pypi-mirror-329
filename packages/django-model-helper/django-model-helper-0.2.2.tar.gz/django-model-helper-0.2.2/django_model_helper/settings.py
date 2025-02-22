import django_environment_settings

DJANGO_USER_SCHEMA = django_environment_settings.get(
    "DJANGO_USER_SCHEMA",
    "django_model_helper.schemas.User",
    aliases=[
        "USER_SCHEMA",
    ],
)
