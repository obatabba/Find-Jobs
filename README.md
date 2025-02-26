# Find-Jobs

Find-Jobs is a simplified hiring platform built with Django and Django REST Framework. It provides a set of RESTful endpoints to manage job listings, companies, employers, and employees.

### Features
- **User Accounts:**

  - **Employer Account:** Create companies, post and manage job listings, monitor applicants and their resumes, and perform CRUD operations on their companies and job posts.
  - **Employee Account:** Browse companies and job listings, apply for jobs, upload resumes, and cancel applications.
- **Endpoints:**\
  The API endpoints allow you to:

  - Manage companies and job listings.
  - Create and update employer and employee profiles.
  - Apply for jobs and manage job applications.
  - Upload and manage resumes.
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

```
pipenv install
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
Open your browser and go to http://127.0.0.1:8000/ to see the API endpoints.

### Project Structure
```
Find-Jobs/
├── FindJobs/            # Main Django app(s) for the project
├── admin_extend/        # Custom admin configurations/extensions
├── employment/          # Employment and job-related functionality
├── manage.py            # Django management script
├── Pipfile              # Pipenv dependency management file
├── Pipfile.lock         # Locked dependency versions
└── .gitignore           # Git ignore rules
```

### API Endpoints Overview

**/employment/companies/** – List and create companies.\
**/employment/companies/id:int/** – Retrieve, update, and delete a specific company.

**/employment/companies/id:int/jobs/** - List and create jobs for a specific company (access restricted to company managers).\
**/employment/companies/id:int/jobs/id:int/** - Retrieve, update, and delete a specific job (access restricted to company managers).

**/employment/companies/id:int/jobs/id:int/applicants/** - List applicants for a specific job (access restricted to company managers).\
**/employment/companies/id:int/jobs/id:int/applicants/id:int** - Retrieve the details of a specific applicant and thier resume (access restricted to company managers).

**/employment/jobs/** – List, all delete job listings.\
**/employment/jobs/int:id/** – Retrieve a specific job, and actions for apply/cancel application.

**/employment/employers/** – List all employers.\
**/employment/employers/id:int/** – Retrieve a specific employer.

**/employment/employees/** – List all employees.\
**/employment/employees/id:int/** – Retrieve a specific employee.

**auth/users/** – List and create users (listing only for admins).\
**auth/users/id:int/** – Retrieve, update and delete a specific user.

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

### Contact
For any questions or suggestions, please open an issue or contact me.
