# 🐾 PetCare Portal

**PetCare Portal** is a full-stack web application designed to help pet owners manage their pets' health, daily care, adoption activities, lost-and-found reports, community interactions, nearby pet services, and emergency information from one centralized platform.

The system was developed as a university Web Engineering project using **Django, MySQL, JavaScript, Firebase Cloud Messaging, and Google Maps/Places APIs**.

---

## 📌 Project Overview

Pet owners often need to manage information across different places, including vaccination schedules, medical records, reminders, adoption posts, lost pet reports, and nearby veterinary services.

PetCare Portal brings these services together into one responsive web platform.

The system allows users to:

- manage multiple pets
- maintain pet health records
- track vaccinations
- monitor pet growth
- create care reminders
- receive browser push notifications
- report lost or found pets
- create adoption listings
- participate in a pet community
- locate nearby veterinarians and pet shops
- access emergency pet-care guidance

---

# ✨ Main Features

## 👤 User Authentication & Account Management

- User registration
- Secure login and logout
- Custom Django user model
- Password reset through email
- Logged-in password change
- User profile management
- Role-based staff/admin access

---

## 🐶 Pet Management

Users can maintain profiles for their own pets.

Features include:

- Add pet
- Edit pet
- Delete pet
- Upload pet photo
- View pet profile
- Store:
  - Name
  - Species
  - Breed
  - Sex
  - Birth date

Each user can access only their own pets.

---

# 🩺 Pet Health & Care

## Medical Records

Users can maintain medical information for each pet, including:

- Veterinary visits
- Diagnoses
- Treatment notes
- Medication information

---

## 💉 Vaccination Tracking

Users can:

- Add vaccination records
- Edit vaccination information
- Delete vaccination records
- Record administered dates
- Store upcoming vaccination dates
- View vaccinations globally or by pet

Vaccinations can automatically create associated care reminders.

---

## 📈 Growth Tracking

Pet growth information can be recorded over time.

Users can track:

- Weight
- Height
- Growth dates
- Important observations

Growth history is visualized using interactive charts.

---

## ⏰ Care Reminders

Users can create reminders for:

- Vaccinations
- Veterinary appointments
- Medication
- Grooming
- Feeding-related tasks
- General pet care

Reminder status and completion can also be managed.

---

# 🔔 Browser Push Notifications

PetCare Portal integrates **Firebase Cloud Messaging (FCM)** for browser notifications.

The system can:

- register browser devices
- request notification permission
- send reminder notifications
- display foreground notifications
- display background notifications
- open the reminders page when a notification is clicked
- prevent repeated notification delivery using notification timestamps

Vaccination-generated reminders can also trigger push notifications.

---

# 🧑‍🤝‍🧑 Community Forum

Pet owners can interact through the community section.

Users can:

- Create posts
- Edit their own posts
- Delete their own posts
- Search posts
- Comment on posts
- View community discussions

### Moderation

Community posts support the following moderation states:

- `PENDING`
- `APPROVED`
- `REJECTED`

Staff members can approve or reject posts through the custom administration dashboard.

Comments are published immediately and do not require admin approval.

---

# 🔎 Lost & Found

Users can report missing or found pets.

Features include:

- Create Lost & Found reports
- Search reports
- View report details
- Edit own reports
- Delete own reports
- Resolve reports
- Reopen reports
- View personal reports
- Contact the reporter

The detail interface is designed to remain clean while presenting the necessary information.

---

# 🏠 Pet Adoption

Pet owners can create adoption listings for pets that need new homes.

Users can:

- Browse active adoption listings
- Create an adoption listing
- Edit their own listing
- Close a listing
- Reopen a listing
- Mark a pet as adopted
- Contact the pet owner

The system prevents multiple active adoption listings for the same pet.

---

# 📍 Nearby Vets & Pet Shops

The system integrates **Google Maps / Places API** to help users locate nearby pet-related services.

Users can search for:

- Veterinary clinics
- Pet hospitals
- Pet food stores
- Pet accessory shops

Features include:

- Browser geolocation
- Interactive map
- Radius-based searching
- Nearby place results
- Location details

---

# 🚑 Emergency Pet Care Guide

The platform contains a dedicated emergency-care information section.

Topics include:

- Choking and breathing difficulty
- Severe bleeding
- Poisoning
- Seizures
- Heatstroke
- Burns
- Fractures and physical trauma
- Collapse or unconsciousness
- Safe transportation of an injured pet

The emergency guide also provides quick access to nearby veterinary services.

> **Important:** The emergency guide provides general first-response information and is not a replacement for professional veterinary care.

---

# 🛡️ Custom Administration Dashboard

A dedicated staff-only administration dashboard provides an overview of the system.

The dashboard includes statistics such as:

- Total users
- Total pets
- Community posts
- Pending posts
- Active adoption listings
- Vaccinations
- Upcoming vaccinations
- Pending reminders

Administrators can also directly:

- View pending community posts
- Approve posts
- Reject posts
- Review recent users
- Review adoption activity

Django's built-in Admin interface remains available for low-level database administration.

---

# 🌐 Bengali Localization Prototype

PetCare Portal includes a prototype bilingual interface using Django's internationalization framework.

Selected core pages support switching between:

- English
- বাংলা

This demonstrates how the platform can be made more accessible to users in Bangladesh.

Full Bengali localization across every module is planned as a future enhancement.

---

# 📱 Responsive User Interface

The system has been designed for:

- Desktop
- Tablet
- Mobile

Responsive testing has been performed at multiple viewport sizes, including:

- 1440px
- 1366px
- 1024px
- 768px
- 390px
- 375px

The interface uses a custom visual theme based around:

- Deep green
- Sage green
- Mint
- Cream
- Gold
- Warm orange

---

# 🔐 Security & Access Control

The application includes several access-control measures.

### Ownership Protection

Users cannot access another user's private:

- Pets
- Medical records
- Vaccinations
- Growth records
- Care reminders
- Adoption management functions
- Lost & Found management functions

Server-side ownership validation is used rather than relying only on hidden interface buttons.

### Other Security Measures

- Django CSRF protection
- Authentication-required views
- Staff-only administration routes
- Environment-based secret configuration
- Password hashing through Django authentication
- Restricted object-level access
- Protected Firebase credentials

---

# 🛠️ Technology Stack

## Backend

- Python
- Django
- Django ORM

## Database

- MySQL

## Frontend

- HTML5
- CSS3
- JavaScript
- Bootstrap
- Font Awesome

## APIs & Services

- Firebase Cloud Messaging
- Google Maps API
- Google Places API

## Visualization

- Chart.js

## Other Tools

- Git
- GitHub
- MySQL Workbench
- VS Code

---

# 🏗️ High-Level Architecture

```text
                         ┌──────────────────────┐
                         │        User          │
                         │   Web / Mobile       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Django Frontend    │
                         │ HTML / CSS / JS      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Django Backend     │
                         │ Views / Forms / ORM  │
                         └─────┬────────┬───────┘
                               │        │
                  ┌────────────┘        └────────────┐
                  ▼                                  ▼
        ┌──────────────────┐               ┌───────────────────┐
        │      MySQL       │               │ External Services │
        │     Database     │               │                   │
        └──────────────────┘               │ Firebase          │
                                           │ Google Maps       │
                                           │ Google Places     │
                                           └───────────────────┘
```

---

# 📂 Main Modules

The project is divided into several functional areas:

```text
PetCare_Portal/
│
├── config/
│   └── Django project configuration
│
├── users_app/
│   └── Authentication, accounts, dashboard and administration
│
├── pets_app/
│   └── Pet profiles and pet management
│
├── health_app/
│   └── Medical records, vaccinations, growth and reminders
│
├── community_app/
│   └── Community posts and comments
│
├── templates/
│   └── Django HTML templates
│
├── static/
│   └── CSS, JavaScript and static assets
│
├── media/
│   └── User-uploaded content during local development
│
├── locale/
│   └── Internationalization files
│
├── manage.py
└── requirements.txt
```

Additional modules implement:

- Adoption
- Lost & Found
- Nearby Pet Services
- Emergency Care
- Push Notifications

---

# ⚙️ Local Installation

## 1. Clone the Repository

```bash
git clone https://github.com/ornitaa/PetCare_Portal.git
cd PetCare_Portal
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🗄️ MySQL Setup

Create a MySQL database:

```sql
CREATE DATABASE petcare_portal
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Configure your database credentials through environment variables.

Do not commit database passwords directly to GitHub.

---

# 🔑 Environment Variables

Create a `.env` file in the project root.

Example:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True

DB_NAME=petcare_portal
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

Google API configuration may also be required:

```env
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
```

Firebase-related configuration must also be supplied according to the project's Django settings.

> Never commit real API keys, passwords, Firebase service-account files, or other secrets to GitHub.

---

# 🔥 Firebase Setup

Browser push notifications require a Firebase project.

The application uses:

- Firebase Cloud Messaging
- Browser notification permission
- Firebase service worker
- Server-side Firebase Admin SDK

A Firebase Admin service-account JSON file is required locally/privately.

Example configured path:

```text
firebase-service-account.json
```

This file **must not be committed to GitHub**.

Ensure it is included in `.gitignore`.

---

# 🗃️ Database Migration

Run:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create an administrator account:

```bash
python manage.py createsuperuser
```

---

# 📦 Static Files

For local development:

```bash
python manage.py collectstatic
```

For production deployment, static files should be handled using an appropriate production configuration such as WhiteNoise or the selected hosting provider's static-file service.

---

# ▶️ Run the Application

```bash
python manage.py runserver
```

Then open the local server in your browser.

---

# 🔔 Running Reminder Notifications

During local development, reminder notifications can be checked using the Django management command:

```bash
python manage.py send_reminder_pushes
```

During development on Windows, this command can be executed automatically using **Windows Task Scheduler**.

For deployment, this task should be handled by a production scheduler, cron service, or background worker.

---

# 🧪 Testing

The project has been manually tested module-by-module.

Testing includes:

- Authentication testing
- Pet CRUD testing
- Health-record testing
- Vaccination testing
- Growth tracking
- Reminder testing
- Push notification testing
- Community moderation
- Lost & Found
- Adoption
- Nearby services
- Emergency guide
- Ownership/security testing
- Responsive interface testing

### Example Test Case

| Test ID | Module | Scenario | Expected Result | Status |
|---|---|---|---|---|
| TC-PET-01 | Pet Management | Add a pet with valid data | Pet is saved and appears in My Pets | PASS |
| TC-AUTH-01 | Authentication | Login using valid credentials | User is redirected to dashboard | PASS |
| TC-COM-01 | Community | Submit a new post | Post enters pending moderation | PASS |
| TC-NOTIF-01 | Notifications | Reminder becomes due | Browser push notification appears | PASS |
| TC-ADOPT-01 | Adoption | Create adoption listing | Listing appears as active | PASS |

---

# 🚀 Deployment Status

The application is currently being prepared for production deployment.

Production deployment requires configuration for:

- Django production server
- Production MySQL-compatible database
- Static-file serving
- Persistent media storage
- Firebase credentials
- Google Maps credentials
- Scheduled reminder execution
- HTTPS
- Production environment variables

---

# 🔮 Future Enhancements

Possible future improvements include:

### Complete Bengali Localization

Extend Bengali translation support to:

- All application pages
- Forms
- Validation messages
- Notifications
- Community
- Adoption
- Lost & Found
- Emergency guidance

### Additional Improvements

- Native mobile application
- In-app notifications
- Email reminder notifications
- Advanced veterinary appointment management
- Pet health analytics
- More advanced search and filtering
- Cloud-based media storage
- Veterinary account/role support
- Shelter/rescue organization accounts

---

# 📊 Project Status

```text
Authentication                ✅ Complete
Pet Management                ✅ Complete
Medical Records               ✅ Complete
Vaccination Management        ✅ Complete
Growth Tracking               ✅ Complete
Care Reminders                ✅ Complete
Push Notifications            ✅ Complete
Community Forum               ✅ Complete
Community Moderation          ✅ Complete
Lost & Found                  ✅ Complete
Adoption                      ✅ Complete
Nearby Pet Services           ✅ Complete
Emergency Care Guide          ✅ Complete
Custom Admin Dashboard        ✅ Complete
Responsive UI                 ✅ Complete
Bengali Localization Demo     ✅ Prototype
Production Deployment         🚧 In Progress
```

---

# ⚠️ Important Security Notes

The following must never be committed to a public repository:

```text
.env
firebase-service-account.json
database passwords
Google API secrets
Django SECRET_KEY
production credentials
private certificates
```

A `.gitignore` file should include at least:

```gitignore
.env
venv/
.venv/
__pycache__/
*.pyc
firebase-service-account.json
staticfiles/
.DS_Store
.idea/
.vscode/
```

Depending on the deployment strategy, user-uploaded local media may also need to be excluded.

---

# 🎓 Academic Project

PetCare Portal was created as a university **Web Engineering project** to demonstrate the complete development lifecycle of a modern web application, including:

- Requirement analysis
- Database design
- System architecture
- Backend development
- Frontend development
- Third-party API integration
- Authentication and authorization
- Testing
- Security
- Responsive design
- Deployment preparation

---

# 🤝 Contributions

This project was developed primarily for academic purposes.

Suggestions and improvements are welcome through GitHub Issues or Pull Requests.

---

# 📄 License

This project is intended primarily for educational and academic use.

A formal open-source license may be added in the future.

---

<p align="center">
  🐾 <strong>PetCare Portal</strong><br>
  Their care. One place.
</p>