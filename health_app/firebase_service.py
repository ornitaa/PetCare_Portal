from pathlib import Path

import firebase_admin

from django.conf import settings

from firebase_admin import credentials


def get_firebase_app():

    try:
        return firebase_admin.get_app()

    except ValueError:
        pass


    credential_path = Path(
        settings.FIREBASE_SERVICE_ACCOUNT_FILE
    )


    if not credential_path.exists():

        raise FileNotFoundError(
            "Firebase service-account file was not found."
        )


    credential = credentials.Certificate(
        str(credential_path)
    )


    return firebase_admin.initialize_app(
        credential
    )