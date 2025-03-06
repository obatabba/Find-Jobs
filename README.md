# Find-Jobs

Find-Jobs is a hiring platform built with Django and Django REST Framework. It provides a set of RESTful endpoints for creating users, manage profiles, manage job listings, companies, apply to jobs, upload resumes, and more!

###
**Check it out, deployed on Render platform: (the first time you hit the website might take a minute to load)**
- https://find-jobs-jn25.onrender.com/

### Features
- **User Accounts:**

  - **Employer Account:** Create companies, post and manage job listings, monitor applicants and their resumes, and perform CRUD operations on their companies and job posts.
  - **Employee Account:** Information rich profile, browse companies and job listings, apply for jobs, upload resumes, and cancel applications.
- **Endpoints:**\
  The API endpoints allow you to:

  - Create users and log in (generate JWT).
  - Update profile information and profile pictures.
  - Create, modify and delete companies (employer accounts only).
  - Create, modify and delete jobs (employer accounts only).
  - View applicants details and resumes -employees who applies to your jobs- (employer accounts only).
  - List job offering, enhanced with searching, sorting, and pagination.
  - Apply for jobs and upload resumes/cancel applications (employee accounts only).
  - List and search companies.
### Technologies Used
- **Backend:** Django, Django REST Framework
- **Environment Management:** Pipenv
- **Database:** SQLtie
### Getting Started
#### Prerequisites
- Python 3.x installed
- Pipenv for dependency management
#### Installation
1.Clone the repository:
```
git clone https://github.com/obatabba/Find-Jobs.git
cd Find-Jobs
```

2.Install dependencies:
  - for Unix based systems:
  ```
  # Use Gunicorn as WSGI server.
  
  pipenv install --categories "packages unix"
  pipenv shell
  ```
  - for Windows:
  ```
  # Use waitress as WSGI server, additional required libaris for windows.

  pipenv install --categories "packages windows"
  pipenv shell
  ```

3.Apply migrations:

```
python manage.py migrate
```

4.Run the development server:

```
python manage.py runserver
```

5.Access the API:
Open your browser and go to http://127.0.0.1:8000/ to see the API endpoints.\

6.Deployment:
- Make sure you do all the steps in [Installation](#installation), Then collect the static files with:
```
python manage.py collectstatic
```
Or if you're using a Unix system, simply run `./build.sh` 

- Run the web server:
  - use **Gunicorn** (Unix systems):
  ```
  gunicorn FindJobs.wsgi
  ```
  
  - use **waitress** (on Windows):
  ```
  python server.py
  ```
  
### Project Structure
```
Find-Jobs/
├── FindJobs/            # Main Django app for the project
├── admin_extend/        # Third-party extended admin features
├── employment/          # The core of the project
├── manage.py
├── Pipfilemanagement file
├── Pipfile.lockversions
└── .gitignore
```

### API Endpoints Overview

**/employment/companies/** – List and create companies.\
**/employment/companies/id:int/** – Retrieve, update, and delete a specific company.

**/employment/companies/id:int/jobs/** - List and create jobs for a specific company (access restricted to company managers).\
**/employment/companies/id:int/jobs/id:int/** - Retrieve, update, and delete a specific job (access restricted to company managers).

**/employment/companies/id:int/jobs/id:int/applicants/** - List applicants for a specific job (access restricted to company managers).\
**/employment/companies/id:int/jobs/id:int/applicants/id:int** - Retrieve the details of a specific applicant and thier resume (access restricted to company managers).

**/employment/jobs/** – List, filter, and search all jobs.\
**/employment/jobs/int:id/** – Retrieve a specific job, provide actions for applying/cancel application to jobs.

**/employment/employers/** – List all employers.\
**/employment/employers/id:int/** – Retrieve a specific employer.

**/employment/employees/** – List all employees.\
**/employment/employees/id:int/** – Retrieve a specific employee.

**/auth/users/** – List and create users (listing only for admins).\
**/auth/users/id:int/** – Retrieve, update and delete a specific user.

**/auth/jwt/create/** – Create a Json Web Token for authentication.

### Contributing
Contributions are welcome! Please follow these steps:\
1.Fork the repository.\
2.Create a feature branch (`git checkout -b feature/YourFeature`).\
3.Commit your changes (`git commit -m 'Add some feature'`).\
4.Push to the branch (`git push origin feature/YourFeature`).\
5.Open a pull request.

### License
This project is licensed under the MIT License. See the LICENSE file for details.

### Third-Party Libraries
django-admin-extend by [kux](https://github.com/kux) – [django-admin-extend](https://github.com/kux/django-admin-extend)
Licensed under the MIT License. The library’s copyright notice and full license text are included in the LICENSE file.


### Contact
For any questions or suggestions, please open an issue or contact me.
