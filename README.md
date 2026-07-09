# Home Service Application

A multi-role web application that connects **customers** with **service professionals** (electricians, cleaners, plumbers, etc.) for on-demand home services, with a dedicated **admin** panel for platform oversight.

Built as part of the *Modern Application Development* project.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Database Schema](#database-schema)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Database Initialization](#database-initialization)
  - [Running the Application](#running-the-application)
- [API Routes](#api-routes)
- [Roles & Workflow](#roles--workflow)
- [Demo](#demo)
- [Author](#author)

---

## Overview

The Home Service Application is a multi-user platform built with Flask that supports three distinct roles — **Admin**, **Professional**, and **Customer** — each with a dedicated dashboard and permission set. Customers can search for and book services, professionals can manage incoming requests, and admins oversee the entire platform, including approving professionals and services.

## Key Features

- **Role-based authentication** — separate login and dashboard flows for Admin, Professional, and Customer
- **Admin controls** — approve or block professionals and customers, create and manage services
- **Service booking workflow** — customers raise requests; professionals accept, reject, or complete them
- **Ratings** — customers can rate completed services
- **Search** — customers can search available services by name
- **Analytics dashboards** — visual summaries for Admin, Professional, and Customer using Chart.js

## Tech Stack

| Layer              | Technology                          |
|---------------------|--------------------------------------|
| Markup & Styling    | HTML5, CSS3, Bootstrap               |
| Client-side Logic   | JavaScript                           |
| Templating          | Jinja2                               |
| Backend Framework   | Flask                                |
| ORM / Database      | Flask-SQLAlchemy                     |
| Data Visualization  | Chart.js                             |

## Database Schema

The application is built around five core entities:

- **admin_info** — admin credentials and role
- **customer_info** — customer profile, address, and approval status
- **professional_info** — professional profile, service offered, experience, and approval status
- **service_info** — service catalog (name, price, estimated time, description)
- **request_info** — service requests linking a customer, professional, and service, with status/date tracking

> The full entity-relationship diagram is available in the project report (`Modern_Application_Development_Report.pdf`).

## Project Structure

A typical layout for this project is as follows (adjust to match your actual repository):

```
home-service-application/
├── app.py                  # Application entry point
├── requirements.txt        # Python dependencies
├── backend/
│   ├── models.py           # SQLAlchemy models (Admin, Customer, Professional, Service, Request)
│   ├── routes/              # Route/controller definitions
│   └── config.py            # App configuration
├── templates/               # Jinja2 HTML templates
├── static/                  # CSS, JS, images
└── instance/
    └── database.sqlite3     # SQLite database (generated at runtime)
```

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

Clone the repository and install the dependencies:

```bash
pip install -r requirements.txt
```

### Database Initialization

The database and the first admin account need to be created once, before the first run. Open a Python shell in the project's root directory:

```bash
python
```

Then run the following inside the Python shell:

```python
from backend.models import *
from app import *

db.create_all()

u1 = Admin_Info(email="admin@gmail.com", fname="Admin", password="Admin123@")
db.session.add(u1)
db.session.commit()

exit()
```

> **Note:** This creates the database tables and seeds a default admin account (`admin@gmail.com` / `Admin123@`). Change this password immediately after your first login in any non-local environment.

### Running the Application

```bash
python app.py
```

By default, Flask will start the app on `http://127.0.0.1:5000`.

## API Routes

| Route                                  | Description                          |
|------------------------------------------|----------------------------------------|
| `/login`                                | Login for admin, professional, and customer |
| `/logout`                               | Logout |
| `/admin_dashboard`                      | Admin dashboard |
| `/professional_dashboard`               | Professional dashboard |
| `/customer_dashboard`                   | Customer dashboard |
| `/professional_Register`                | Professional registration |
| `/customer_Register`                    | Customer registration |
| `/profile`                              | User profile |
| `/service/add`                          | Add a new service |
| `/service/edit/<int:key>`               | Edit an existing service |
| `/service/delete/<int:key>`             | Delete a service |
| `/book_service`                         | Book a service |
| `/service_rating`                       | Rate a completed service |
| `/approve_professional/<int:id>`        | Approve a professional |
| `/block_professional/<int:id>`          | Block a professional |
| `/block_customer/<int:id>`              | Block a customer |
| `/approve_service/<int:id>`             | Approve a service |
| `/reject_service/<int:id>`              | Reject a service |
| `/complete_service/<int:id>`            | Mark a service request as complete |
| `/cancel_service/<int:id>`              | Cancel a service request |
| `/admin_summary`                        | Admin analytics summary |
| `/professional_summary`                 | Professional analytics summary |
| `/customer_summary`                     | Customer analytics summary |
| `/search_service`                       | Search services by name |

## Roles & Workflow

**Admin**
- Monitors all activity on the platform
- Creates and manages the service catalog
- Approves or blocks professionals and customers

**Professional**
- Registers and waits for admin approval
- Receives customer service requests
- Accepts, rejects, or completes assigned requests

**Customer**
- Registers and browses/searches available services
- Books a service and tracks its status
- Rates the professional once the service is completed

## Author

**Tripurari Kumar**
23F2003868
[23f2003868@ds.study.iitm.ac.in](mailto:23f2003868@ds.study.iitm.ac.in)

---

*This project was developed as part of the Modern Application Development coursework.*
