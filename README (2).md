# Velgo Agrisolutions Web Platform

Velgo Agrisolutions is a full-stack, responsive web platform for an agri-consultancy business, connecting farmers with expert services through a modern, interactive UI.


---

## 📋 About The Project

This project is a complete front-to-back solution for an agricultural consultancy firm. It allows users (farmers) to browse services, learn about the company, and book consultations or specific services.

The system is built on a modern **Firebase** backend, handling user authentication (Email, Google) and managing all bookings in a real-time **Firestore** database. A key feature is the "My Bookings" panel, where logged-in users can track the status of their requests (Pending, Accepted, or Rejected), which can only be updated by an admin.

The site is fully responsive, features a multilingual toggle (English/Tamil), and is enhanced with modern UI animations.

## ✨ Key Features

* **User Authentication:** Secure login and sign-up with both Email/Password and Google.
* **Firebase Backend:** Uses **Firestore** for real-time database management and **Firebase Auth** for user handling.
* **Service Booking:** Users can book specific services like "Soil Testing" or "AI & IoT Farming."
* **Consultation Booking:** A multi-step form for booking "On-Site" or "Office" consultations.
* **User Dashboard:** A "My Bookings" modal where users can track the status of their requests (Pending, Accepted, Rejected) in real-time.
* **Role-Based Access:** A built-in check for `admin` vs. `client` roles (with admins being redirected to a separate panel).
* **Dynamic Content:** Footer credits are loaded dynamically from Firestore, modifiable only by an admin.
* **Bilingual Support:** Easily toggle all site content between English (EN) and Tamil (TA).
* **Modern UI/UX:** A fully responsive design with AOS scroll animations, a floating WhatsApp button, and an integrated (simulated) chatbot.

## 💻 Tech Stack

* **Frontend:** HTML5, CSS3 (with CSS Variables), JavaScript (ES6 Modules)
* **Backend:** Firebase (Authentication, Firestore)
* **Libraries:** AOS (Animate on Scroll), Font Awesome (Icons)

## 🚀 Getting Started

This project is a static frontend that relies on a Firebase backend. To get it running locally, you must configure your own Firebase project.

### Prerequisites

You only need a modern web browser and a free Firebase account.

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/your-username/velgo-agrisolutions.git](https://github.com/your-username/velgo-agrisolutions.git)
    ```
2.  **Navigate to the directory:**
    ```sh
    cd velgo-agrisolutions
    ```
3.  **Open `index.html` in your browser.**
    * At this point, the site will load, but booking and login will **not** work until you complete the next step.

### Firebase Configuration (Required)

1.  Go to the [Firebase Console](https://console.firebase.google.com/) and create a new project.
2.  Enable **Authentication** and add the **Email/Password** and **Google** sign-in providers.
3.  Enable **Firestore Database**.
4.  In your Firebase project settings, find your web app's **Firebase config object**.
5.  In the `index.html` file, find the `<script type="module">` tag at the bottom.
6.  Replace the placeholder `firebaseConfig` object with your own project's config snippet:
    ```javascript
    // ...
    // TODO: உங்கள் சொந்த Firebase Configuration-ஐ இங்கு உள்ளிடவும்
    const firebaseConfig = {
      apiKey: "YOUR_API_KEY",
      authDomain: "YOUR_PROJECT.firebaseapp.com",
      projectId: "YOUR_PROJECT_ID",
      storageBucket: "YOUR_PROJECT.appspot.com",
      messagingSenderId: "YOUR_SENDER_ID",
      appId: "YOUR_APP_ID",
      measurementId: "YOUR_MEASUREMENT_ID"
    };
    // ...
    ```
7.  **Set Firestore Rules:** This is essential for security.
    * In your Firebase project, go to **Firestore Database** > **Rules**.
    * Copy the contents of the `firestore.rules` file from this repository.
    * Paste the rules into the Firebase editor and click **Publish**.
8.  **Set Up Admin User (Optional):**
    * Sign up for a new account on your website.
    * Go to the **Firebase Auth** console, find your new user, and copy their `User UID`.
    * In your `firestore.rules`, replace the hard-coded UID (`"SyVasaKRU...0x2"`) with your own UID to grant yourself admin rights.

## 📜 License

Distributed under the MIT License. See `LICENSE` file for more information.

## 👤 Contact

Lokesh - [lokeshloki.site](https://lokeshloki.site)
