from django.conf import settings
from django.contrib import admin
from django.urls import path


'''  admin/base_site.html override template also affects the title '''
admin.site.site_title = 'REAL Django Admin'   # DEFAULT: "Django site admin"
admin.site.site_header = 'Real Django Admin'  # DEFAULT: "Django Administration"
admin.site.index_title = 'Site Admin Home'    # DEFAULT: "Site Administration"


urlpatterns = [
    path(settings.ADMIN_PATH, admin.site.urls),
]