# PAI-E Semester Work

* Subject: KIV/PIA-E
* Student: Trong Quoc Huy Dinh
* Personal number: A25N0040P
* Email: qhdt@students.zcu.cz

## Warehouse Management System (PIA Semester Project)

A full-stack web application for managing warehouse inventory and orders with role-based access control.

The system supports multiple companies and user roles, ensuring strict data separation and secure access to business data.

## Main features

- Product and inventory management
- Order creation, processing, and status tracking
- Role-based access (superadmin, admin, manager, employee)
- Company-scoped data isolation
- Modular monolithic backend architecture with a separated REST API layer
- Dockerized deployment for easy setup

---

## Tech Stack

### Backend
* Python 3.10+
* Flask – Web application (HTML UI, authentication, routing)
* FastAPI – REST API layer
* SQLAlchemy – ORM
* Pydantic – Data validation
* JWT Authentication
* PostgreSQL – Relational database

### Frontend
* HTML5
* CSS3
* JavaScript (ES6)
* Bootstrap / Tabler UI
* Jinja2 – Server-side templating

### Infrastructure
* Docker & Docker Compose
* PostgreSQL container
* adminer (optional)

---

## Project Structure

The project is implemented as a single backend system with a clear separation
between the web UI (Flask), REST API (FastAPI), and database access layer.

```text
.
├── api # Backend RESTful API implemented using FastAPI.
│   ├── __init__.py
│   ├── config.py # Configuration of API using environment variables in Docker Compose 
│   ├── db # Database session setup and helpers
│   ├── dependencies # FastAPI dependency injection (auth, DB, permissions)
│   ├── Dockerfile # API container definition
│   ├── integrations # External service integrations
│   ├── main.py # FastAPI application entry point
│   ├── models # Domain and database models
│   ├── requirements.txt # API dependencies
│   ├── routes # API endpoint definitions
│   ├── schemas # Pydantic request/response schemas
│   ├── services # Business logic and service layer
│   └── utils # Shared utility functions
├── db
│   └── schema.sql # Schema of database
├── docker-compose.yml # Container orchestration
├── pytest.ini # Pytest configuration
├── README.md # Project documentation
├── requirements.txt # Depencencies for dev
├── tests
│   ├── conftest.py # Pytest configuration and shared fixtures
│   ├── routes # API endpoint tests
│   ├── services # Business logic unit tests
│   └── smoke # Smoke and basic integration tests
└── web_app
    ├── __init__.py
    ├── api_clients # Clients for communicating with the FastAPI backend
    ├── config.py # Web application configuration
    ├── Dockerfile # Web application container definition
    ├── localization # Application translations and localization files
    ├── requirements.txt # Web application dependencies
    ├── routes # Flask route handlers
    ├── static # Static assets (CSS, JavaScript, fonts, images)
    └── templates # Jinja2 HTML templates
```

---

## Starting The App

The recommended way to run the application is using Docker Compose.
This will start all required services automatically, including the database,
REST API, and web application.

### Prerequisites
* Docker Desktop (running)
* Environment Variables
 - DB_HOST
 - DB_USER
 - DB_PASSWORD
 - DB_NAME
 - JWT_SECRET
 - FLASK_SECRET_KEY
 - GITHUB_CLIENT_ID (optional, for GitHub OAuth)
 - GITHUB_CLIENT_SECRET (optional)
 - GITHUB_REDIRECT_URI (optional)

### Installation & Run
1.  Open a terminal in the project root.
2.  Run the following command:
    ```bash
    docker-compose up --build
    ```
3.  Wait for the containers to start. The initial build may take a few minutes.

**Note:** On first startup, the database initialization script located in the
`db/` directory is executed automatically to create the required schema.

### Using Github Login

To log into the app using a Github account, you must do these steps:
1. Log in to your GitHub account.
2. Go to **Settings** -> **Developer settings** (at the very bottom of the left sidebar).
3. Click on **OAuth Apps** -> **New OAuth App**.
4. Fill in the form:
    - Application Name: inventory_app (or similar).
    - Homepage URL: http://localhost:8000
    - Authorization callback URL: http://localhost:8500/api/users/auth/github/callback
5. Click **Register application**.
6. You will now see your **Client ID**.
7. Click **Generate a new client secret** to get your **Client Secret**. **Copy both of these**.
8. Add them to your `.env` file:
    ```bash
    GITHUB_CLIENT_ID=your_client_id
    GITHUB_CLIENT_SECRET=your_client_secret
    GITHUB_REDIRECT_URI=http://localhost:8500/api/users/auth/github/callback
    ```
---

## Service Ports

Once Docker is running, you can access the following services:

* **Web Application:** [http://localhost:8000](http://localhost:8000)
* **API:** [http://localhost:8500](http://localhost:8500)
* **Adminer:** [http://localhost:8080](http://localhost:8080)
* **PostgreSQL:** `localhost:5432`

---

## Default Login Credentials

The system comes pre-seeded with the following users:

| Username       | Email                     | Password    |
|----------------|---------------------------|-------------|
| **superadmin** | `superadmin@example.com`  | `superadmin`|
| **admin**      | `admin@technova.com`      | `admin`     |
| **manager**   | `manager@technova.com`    | `manager`   |
| **employee**  | `employee@technova.com`   | `employee`  |

---

## Key Workflows

### Role Hierarchy and Company Scope

The system enforces a strict role hierarchy combined with company-based data
isolation:

- **Superadmin**
  - System-wide access
  - Creates and manages companies
  - Can create users for any company

- **Admin**
  - Company-level access
  - Can create and manage users only within their own company

- **Manager**
  - Company-level access
  - Can create users within their own company
  - Manages inventory and orders

- **Employee**
  - Limited access within their own company
  - Can view and work with assigned data

Users can only access data that belongs to their assigned company.

---

### 1. Company and User Management

- **Superadmin** creates companies in the system.
- **Superadmin** can create users and assign them to specific companies.
- **Admin** and **Manager** can create and manage users **only within their own company**.
- Role assignment is validated according to the role hierarchy.

---

### 2. Item Management

- Users assigned to a company (**Admin**, **Manager**) can:
  - Create item entries
  - Edit existing items
- Items are always associated with a single company.
- Users cannot view or modify items belonging to other companies.

---

### 3. Order Creation and Processing

- Authorized users can create orders within their company.
- The system supports **two types of orders**:
  - **Sale orders** – reduce inventory quantity
  - **Purchase orders** – increase inventory quantity
- Orders go through defined states:
  - `pending`
  - `completed`
  - `cancelled`
- Inventory levels are automatically updated based on order type and status.

---

### 4. Access Control Enforcement

- All actions are validated at both UI and API level.
- Role and company checks are applied consistently across the application.
- Unauthorized actions are rejected with appropriate error responses.

## Testing

The project includes automated tests for backend logic and API endpoints.

### Running Backend Tests
To run the integration and unit tests:

1. go to project root in terminal and use command:
    ```bash
    pytest -v
    ```

### Static type checker
To run the type check:

1. go to project root in terminal and use command:
    ```bash
    mypy .
    ```
