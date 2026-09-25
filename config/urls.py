from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from health_app import views as health_views
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path(
    "i18n/",
    include("django.conf.urls.i18n"),
    ),
    path("admin/", admin.site.urls),

    path("", include("users_app.urls")),

    path("pets/", include("pets_app.urls")),

    path("", include("health_app.global_urls")),

    path(
        "lost-found/",
        include("lostfound_app.urls"),
    ),

    path(
        "community/",
        include("community_app.urls"),
    ),

    path(
        "adoption/",
        include("adoption_app.urls"),
    ),
    path(
    "nearby-vets/",
    include("vets_app.urls"),
    ),
    path(
    "firebase-messaging-sw.js",
    health_views.firebase_messaging_service_worker,
    name="firebase_messaging_service_worker",
    ),
    
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )