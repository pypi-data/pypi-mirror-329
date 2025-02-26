from django.conf import settings


def general(request):
    return {
        'PROJECT_NAME': getattr(settings, 'PROJECT_NAME', None),
        'ENV_NAME': getattr(settings, 'ENV_NAME', None),
        'ADMIN_HEADER_BG': getattr(settings, 'ADMIN_HEADER_BG', None),
        'GOOGLE_ANALYTICS_ID': getattr(settings, 'GOOGLE_ANALYTICS_ID', None),
    }