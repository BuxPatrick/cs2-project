Step 1: Project Initialization

Create a Django project named stroke_system and an app named core. Set up the project structure with a virtual environment, static files, and templates folders. Enable user authentication and include core in INSTALLED_APPS.

Step 2: User Authentication with Role-Based Access

Implement a custom user profile model linked to Django’s default User model. The profile should include a role field with options: "Technician" and "Neurologist". Set up login, logout, and registration views and templates that allow the user to choose and register with a role.

Step 3: Homepage with Role Selection

Build a landing page where the user chooses between Technician and Neurologist. Based on this, redirect them to the respective login/registration pages. After login, redirect them to a role-specific dashboard.

Step 4: Technician Dashboard

Create a dashboard for technicians that includes:

A button to “Add New Patient” using a form.

A table listing previously added patients.

Option to edit or update patient notes. Patient fields include: name, age, sex, medical history, chief complaint, vital signs (BP, HR, RR, O2 sat), lab results, imaging summary, and NIHSS score.

Step 5: Neurologist Dashboard

Create a dashboard for neurologists that displays a list of submitted patient records. Each entry should show a summary and link to a detailed view. In the detailed view, allow the neurologist to:

Review all patient info (read-only).

Add a diagnosis and treatment simulation.

Submit and save the consultation.

Step 6: Data Models

Create models for:

Patient: stores all technician-entered data.

Consultation: stores neurologist diagnosis, treatment plan, and timestamp.

Ensure the patient is linked to the technician who created it, and consultations are linked to the neurologist who submitted them.

Step 7: Alert Simulation Logic

Add logic to show alerts when certain vital signs exceed thresholds (e.g., BP > 180/100). These can be simple color-coded banners or modal warnings on the technician and neurologist dashboards.

Step 8: Templates and Navigation

Build clean HTML templates using Django’s templating system:

Base template with navbar and user role logic.

Role-specific dashboards.

Forms for adding and viewing patients and consultations. Ensure easy navigation between views and pages.

Step 9: Styling and UX

Use Bootstrap (or Tailwind) to style the app. Ensure mobile-responsiveness and intuitive layout, especially for technicians in emergency scenarios. Use cards, tables, and modals for displaying patient data.

Step 10: Sample Data and Testing

Preload the app with the 4 sample patients from the provided PDF (John Doe, Jane Smith, Bob Johnson, Maria Rodriguez). Use them to test the end-to-end flow from technician input to neurologist consultation.

Step 11: Final Touches

Add:

A logout button and user profile dropdown.

“Last updated” timestamps on patient and consultation entries.

Page access restriction: only technicians can access technician pages, and only neurologists can access theirs.

Optional Step 12: (If time allows)

Add downloadable or printable patient reports after consultation submission.

