/* ============================================================
   PETCARE FIREBASE SERVICE WORKER
   ============================================================ */


/* ============================================================
   NOTIFICATION CLICK

   IMPORTANT:
   Keep this BEFORE importing Firebase.
   ============================================================ */

self.addEventListener(
    "notificationclick",
    function (event) {

        console.log(
            "[PetCare SW] Notification clicked:",
            event.notification
        );


        /*
         * Prevent another notification-click handler
         * from processing the same click.
         */

        event.stopImmediatePropagation();


        event.notification.close();


        /*
         * Get the destination saved inside the notification.
         * If no URL was provided, always use the global
         * reminders page.
         */

        const notificationData =
            event.notification.data || {};


        const targetPath =
            notificationData.url ||
            "/reminders/";


        /*
         * Convert relative path to full URL.
         */

        const targetUrl =
            new URL(
                targetPath,
                self.location.origin
            ).href;


        console.log(
            "[PetCare SW] Opening:",
            targetUrl
        );


        event.waitUntil(

            clients.matchAll({
                type: "window",
                includeUncontrolled: true,
            })
            .then(
                async function (clientList) {


                    /*
                     * PetCare is already open somewhere.
                     *
                     * Navigate that tab to the reminders page
                     * and focus it.
                     */

                    for (
                        const client
                        of clientList
                    ) {

                        try {

                            const clientUrl =
                                new URL(
                                    client.url
                                );


                            if (
                                clientUrl.origin
                                ===
                                self.location.origin
                            ) {

                                if (
                                    "navigate"
                                    in client
                                ) {

                                    await client.navigate(
                                        targetUrl
                                    );

                                }


                                if (
                                    "focus"
                                    in client
                                ) {

                                    return client.focus();

                                }

                            }

                        }

                        catch (error) {

                            console.error(
                                "[PetCare SW] Client URL error:",
                                error
                            );

                        }

                    }



                    /*
                     * PetCare isn't currently open.
                     *
                     * Open a new browser tab.
                     */

                    if (
                        clients.openWindow
                    ) {

                        return clients.openWindow(
                            targetUrl
                        );

                    }


                    return null;

                }
            )

        );

    }
);



/* ============================================================
   FIREBASE
   ============================================================ */

importScripts(
    "https://www.gstatic.com/firebasejs/12.19.0/firebase-app-compat.js"
);


importScripts(
    "https://www.gstatic.com/firebasejs/12.19.0/firebase-messaging-compat.js"
);



firebase.initializeApp({

    apiKey:
        "{{ firebase_api_key|escapejs }}",

    authDomain:
        "{{ firebase_auth_domain|escapejs }}",

    projectId:
        "{{ firebase_project_id|escapejs }}",

    storageBucket:
        "{{ firebase_storage_bucket|escapejs }}",

    messagingSenderId:
        "{{ firebase_messaging_sender_id|escapejs }}",

    appId:
        "{{ firebase_app_id|escapejs }}"

});



const messaging =
    firebase.messaging();