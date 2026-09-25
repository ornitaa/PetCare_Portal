from django.conf import settings


def firebase_public_settings(request):

    return {
        "firebase_api_key":
            settings.FIREBASE_API_KEY,

        "firebase_auth_domain":
            settings.FIREBASE_AUTH_DOMAIN,

        "firebase_project_id":
            settings.FIREBASE_PROJECT_ID,

        "firebase_storage_bucket":
            settings.FIREBASE_STORAGE_BUCKET,

        "firebase_messaging_sender_id":
            settings.FIREBASE_MESSAGING_SENDER_ID,

        "firebase_app_id":
            settings.FIREBASE_APP_ID,

        "firebase_vapid_key":
            settings.FIREBASE_VAPID_KEY,
    }