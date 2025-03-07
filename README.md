# Find-Jobs

Find-Jobs is a hiring platform built with Django and Django REST Framework. It provides a set of RESTful endpoints for creating users, managing profiles, job listings, companies, applying to jobs, uploading resumes, and more!

**Check it out on the Render platform (the first visit may take a minute to load):**  
- [https://find-jobs-jn25.onrender.com/](https://find-jobs-jn25.onrender.com/)

---

## Features

- **User Accounts:**
  - **Employer Account:** Create and manage companies, create and manage job listings, monitor applicants and their resumes.
  - **Employee Account:** Create an information-rich profile, browse companies and job listings, apply for jobs, upload resumes, and cancel applications.
  
- **API Endpoints:**  
  The API endpoints allow you to:
  - Create users and log in (JWT generation).
  - Update profile information and profile pictures.
  - Create, modify, and delete companies (employer accounts only).
  - Create, modify, and delete jobs (employer accounts only).
  - View applicant details and resumes—employees who apply to your jobs (employer accounts only).
  - List job offerings enhanced with searching, sorting, and pagination.
  - Apply for jobs, upload resumes, and cancel applications (employee accounts only).
  - List and search companies.

---

## Technologies Used

- **Backend:** Django, Django REST Framework  
- **Environment Management:** Pipenv  
- **Database:** SQLite/PostgreSQL

---

## Getting Started

### Prerequisites
- Python 3.13 installed
- Pipenv for dependency management

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/obatabba/Find-Jobs.git
   cd Find-Jobs
   ```

2. **Install dependencies:**

   - **For Unix-based systems:**
     ```bash
     # Use Gunicorn as the WSGI server.
     pipenv install --categories "packages unix"
     pipenv shell
     ```

   - **For Windows:**
     ```bash
     # Use Waitress as the WSGI server; additional required libraries for Windows.
     pipenv install --categories "packages windows"
     pipenv shell
     ```

3. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

5. **Access the API:**  
   Open your browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to see the API endpoints.

6. **Deployment:**
   - Ensure you have completed all the steps in [Installation](#installation). Then, collect the static files:
     ```bash
     python manage.py collectstatic
     ```
     Alternatively, on Unix systems, you can simply run:
     ```bash
     ./build.sh
     ```
   - **Run the web server:**
     - **Unix systems (using Gunicorn):**
       ```bash
       gunicorn FindJobs.wsgi
       ```
     - **Windows (using Waitress):**
       ```bash
       python server.py
       ```

---

## Environment Variables

This project uses environment variables to manage sensitive settings and deployment-specific configurations. To properly deploy this project, please create a `.env` file in the project root (or set these variables in your deployment environment).

### Required Variables

- **DJANGO_SETTINGS_MODULE:**  
  The `settings.py` module to use in production.
  ***For production, set it to*** `FindJobs.settings.prod`, defaults to `FindJobs.settings.dev`.  
  *Example:*  
  ```
  DJANGI_SETTINGS_MODULE=FindJobs.settings.prod
  ```

- **SECRET_KEY:**  
  The secret key used for cryptographic signing in Django.  
  *Example:*  
  ```
  SECRET_KEY="your-secret-key-here"
  ```

- **ALLOWED_HOSTS:**  
  A comma-separated list of allowed hostnames.  
  *Example:*  
  ```
  ALLOWED_HOSTS=127.0.0.1,localhost,find-jobs.example.com
  ```

- **DATABASE_URL:**  
  The URL for your PostgreSQL database connection.
  *Example:*  
  ```
  DATABASE_URL=postgres://user:password@localhost:5432/yourdbname
  ```

### Optional
If you uncomment `python3 manage.py createsuperuser` in `build.sh`, this will create a super-user when building the project, and you will have to set the following environment variables as they will be used for creating your super-user:

- **DJANGO_SUPERUSER_USERNAME:**  
  The username to use for creating the user.\
  *Example:*  
  ```
  DJANGO_SUPERUSER_USERNAME=admin
  ```

- **DJANGO_SUPERUSER_EMAIL:**  
  The email to use for creating the user.\
  *Example:*  
  ```
  DJANGO_SUPERUSER_EMAIL=admin@domain.com
  ```

- **DJANGO_SUPERUSER_PASSWORD:**  
  The password to use for creating the user. **Note** that django, by default, doesn't allow short, common and numeric passwords.\
  *Example:*  
  ```
  DJANGO_SUPERUSER_PASSWORD=mywebsiteadminuser
  ```

---

## Project Structure

```
Find-Jobs/
├── FindJobs/               # Main Django app for the project
├── admin_extend/           # Third-party extended admin features
├── employment/             # Core project functionalities
├── manage.py
├── Pipfile                 # Pipenv management file
├── Pipfile.lock            # Pipenv lock file
└── .gitignore
```

---

## API Endpoints Overview

- **/employment/companies/** – List and create companies.  
- **/employment/companies/<id:int>/** – Retrieve, update, and delete a specific company.

- **/employment/companies/<id:int>/jobs/** – List and create jobs for a specific company (access restricted to company managers).  
- **/employment/companies/<id:int>/jobs/<id:int>/** – Retrieve, update, and delete a specific job (access restricted to company managers).

- **/employment/companies/<id:int>/jobs/<id:int>/applicants/** – List applicants for a specific job (access restricted to company managers).  
- **/employment/companies/<id:int>/jobs/<id:int>/applicants/<id:int>** – Retrieve the details of a specific applicant and their resume (access restricted to company managers).

- **/employment/jobs/** – List, filter, and search all jobs.  
- **/employment/jobs/<id:int>/** – Retrieve a specific job and provide actions for applying or canceling an application.

- **/employment/employers/** – List all employers.  
- **/employment/employers/<id:int>/** – Retrieve a specific employer.

- **/employment/employees/** – List all employees.  
- **/employment/employees/<id:int>/** – Retrieve a specific employee.

- **/auth/users/** – List and create users (listing available only for admins).  
- **/auth/users/<id:int>/** – Retrieve, update, and delete a specific user.

- **/auth/jwt/create/** – Create a JSON Web Token for authentication.

---

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Third-Party Libraries

- **django-admin-extend** by [kux](https://github.com/kux) – [django-admin-extend](https://github.com/kux/django-admin-extend)  
  Licensed under the MIT License. The library’s copyright notice and full license text are included in the LICENSE file.

---

## Contact

For any questions or suggestions, please open an issue or contact me.
