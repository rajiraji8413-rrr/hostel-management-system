\# Hostel Management System



\## Project Overview



The Hostel Management System is a web-based application developed using Python and Django REST Framework. It helps manage hostel students, rooms, room allocations and fee payments.



The project provides REST APIs and a simple web interface to manage hostel operations efficiently.



\## Technologies Used



\- Python

\- Django

\- Django REST Framework

\- SQLite

\- HTML

\- CSS

\- Bootstrap

\- JavaScript

\- Postman

\- Git and GitHub



\## Features



\### 1. Student Management

\- Add new students

\- View student details

\- Update student information

\- Delete student records

\- Validate duplicate email addresses



\### 2. Room Management

\- Add and manage hostel rooms

\- View room details

\- Update room information

\- Track room capacity and available beds

\- Validate room capacity



\### 3. Room Allocation

\- Allocate rooms to students

\- View room allocations

\- Update allocation status

\- Prevent duplicate active allocations

\- Automatically update available bed counts



\### 4. Fee Payment Management

\- Add fee payment records

\- View payment details

\- Update payment information

\- Track paid and pending payments

\- Validate payment amounts



\### 5. Dashboard

\- Total students

\- Total rooms

\- Total allocations

\- Occupied beds

\- Available beds

\- Total payments

\- Paid and pending amounts



\### 6. Authentication

\- Token-based authentication

\- Protected API endpoints

\- Login using username and password



\## API Endpoints



| Method | Endpoint | Description |

|---|---|---|

| GET, POST | `/api/students/` | List and create students |

| GET, PUT, PATCH, DELETE | `/api/students/<id>/` | Retrieve and manage a student |

| GET, POST | `/api/rooms/` | List and create rooms |

| GET, PUT, PATCH, DELETE | `/api/rooms/<id>/` | Retrieve and manage a room |

| GET, POST | `/api/allocations/` | List and create allocations |

| GET, PUT, PATCH, DELETE | `/api/allocations/<id>/` | Retrieve and manage an allocation |

| GET, POST | `/api/payments/` | List and create payments |

| GET, PUT, PATCH, DELETE | `/api/payments/<id>/` | Retrieve and manage a payment |

| GET | `/api/dashboard/` | Dashboard statistics |

| POST | `/api/login/` | Obtain authentication token |



\## Frontend Pages



\- Dashboard

\- Students

\- Rooms

\- Allocations

\- Payments



\## Installation and Setup



\### 1. Clone the repository



```bash

git clone https://github.com/rajiraji8413-rrr/hostel-management-system.git

```



\### 2. Navigate to the project folder



```bash

cd hostel-management-system

```



\### 3. Create a virtual environment



```bash

python -m venv venv

```



\### 4. Activate the virtual environment



Windows PowerShell:



```powershell

.\\venv\\Scripts\\Activate.ps1

```



\### 5. Install dependencies



```bash

pip install django djangorestframework

```



\### 6. Apply migrations



```bash

python manage.py migrate

```



\### 7. Create a superuser



```bash

python manage.py createsuperuser

```



\### 8. Run the development server



```bash

python manage.py runserver

```



Open the application:



`http://127.0.0.1:8000/`



Admin panel:



`http://127.0.0.1:8000/admin/`



\## API Testing



APIs were tested using Postman.



Testing included:



\- GET, POST, PUT and PATCH requests

\- Token authentication

\- Invalid login credentials

\- Unauthorized API access

\- Duplicate student email validation

\- Room capacity validation

\- Duplicate active room allocation validation

\- Payment amount validation



\## Author



Developed as a Django REST Framework practice project.



\*\*GitHub Repository:\*\*  

https://github.com/rajiraji8413-rrr/hostel-management-system

