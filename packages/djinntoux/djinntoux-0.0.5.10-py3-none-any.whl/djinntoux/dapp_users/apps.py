from django.apps import AppConfig

class UsersConfig(AppConfig):

    default_auto_field = "django.db.models.AutoField"

    name = "djinntoux.dapp_users"

    ''' to sort non-project apps to the end in the admin UI '''
    verbose_name = "zz: Auth Users (Custom via PyPI)"

    ''' to sort all actual database tables to the end in, e.g., psql;
        main project app table labels should be prefixed with "zz_" '''
    label = "zy_users"