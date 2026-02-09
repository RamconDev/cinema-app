# Cinema Flask - Cinema Management System

A comprehensive web-based cinema management system built with Flask, featuring movie scheduling, auditorium management, seat reservations, and user authentication with role-based access control.

## 🎬 Features

### Public Features
- **Movie Catalog**: Browse available movies with details, genres, and posters
- **Showtimes**: View upcoming movie functions/screenings
- **Seat Selection**: Interactive seat selection interface for reservations
- **Reservation System**: Create and manage movie ticket reservations

### Admin Features
- **Movie Management**: Create, update, and manage movies with genres
- **Genre Management**: Add and organize movie genres
- **Auditorium Management**: Create auditoriums and configure seating arrangements
- **Function Scheduling**: Schedule movie screenings with specific times and auditoriums
- **User Management**: Create and manage user accounts with role assignments
- **Role Management**: Define and manage user roles (admin, client, etc.)

### Authentication & Authorization
- User registration and login system
- Password hashing with bcrypt
- Role-based access control (RBAC)
- Session management with Flask-Login

## 🛠️ Technologies

### Backend
- **Flask 3.1.2** - Web framework
- **SQLAlchemy 2.0.44** - ORM for database operations
- **Flask-Migrate 4.1.0** - Database migrations with Alembic
- **Flask-Login 0.6.3** - User session management
- **Flask-Bcrypt 1.0.1** - Password hashing
- **Flask-WTF 1.2.2** - Form handling and CSRF protection
- **WTForms 3.2.1** - Form validation

### Database
- **SQLite** (default) - Lightweight database for development
- **PostgreSQL/MySQL** support - Configurable for production

### Frontend
- **Jinja2** - Template engine
- **SASS/SCSS** - CSS preprocessing
- **Bootstrap** (inferred from structure) - UI framework

### Additional Tools
- **python-dotenv** - Environment variable management
- **Alembic** - Database migration tool

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd cinema-flask
```

### 2. Create a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
# Secret key for Flask sessions (change this in production!)
SECRET_KEY=your_secret_key_here

# Database Configuration
# For SQLite (default):
DB_ENGINE=sqlite
NAME_DB=cinema_app

# For PostgreSQL (optional):
# DB_ENGINE=postgresql
# USER_DB=your_db_user
# USER_PASSWORD=your_db_password
# SERVER_DB=localhost:5432
# NAME_DB=cinema_db

# For MySQL (optional):
# DB_ENGINE=mysql+pymysql
# USER_DB=your_db_user
# USER_PASSWORD=your_db_password
# SERVER_DB=localhost:3306
# NAME_DB=cinema_db
```

### 5. Initialize the Database

The application will automatically create the database and initialize with sample data when you first run it. The `run.py` script includes automatic initialization.

Alternatively, you can manually run migrations:

```bash
flask db upgrade
```

### 6. Run the Application

```bash
python run.py
```

The application will be available at `http://localhost:5000` (or `http://127.0.0.1:5000`)

## 📁 Project Structure

```
cinema-flask/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── register_blueprints.py  # Blueprint registration
│   ├── init_data.py         # Initial data seeding
│   ├── schema.sql           # Database schema
│   ├── auth/                # Authentication module
│   │   ├── routes.py        # Auth routes
│   │   ├── forms/           # Authentication forms
│   │   └── templates/       # Auth templates
│   ├── cinema/              # Cinema management module
│   │   ├── routes.py        # Cinema routes
│   │   ├── forms/           # Cinema forms
│   │   └── templates/       # Cinema templates
│   ├── public/              # Public-facing module
│   │   ├── routes.py        # Public routes
│   │   ├── forms/           # Public forms
│   │   └── templates/       # Public templates
│   ├── models/              # Database models
│   │   ├── auth_user.py
│   │   ├── auth_role.py
│   │   ├── cinema_movie.py
│   │   ├── cinema_genre.py
│   │   ├── cinema_auditorium.py
│   │   ├── cinema_seat.py
│   │   ├── cinema_function.py
│   │   └── public_reservation.py
│   ├── static/              # Static files (CSS, images)
│   └── templates/           # Base templates
├── migrations/              # Database migrations
├── instance/                # Instance folder (database files)
├── config.py               # Configuration settings
├── run.py                   # Application entry point
└── requirements.txt         # Python dependencies
```

## 🗄️ Database Schema

The system uses the following main entities:

- **Users** - User accounts with authentication
- **Roles** - User roles (admin, client, etc.)
- **Movies** - Movie information
- **Genres** - Movie genres
- **Movie_Genres** - Many-to-many relationship between movies and genres
- **Auditoriums** - Cinema auditoriums
- **Seats** - Seats within auditoriums
- **Functions** - Movie screenings/schedules
- **Reservations** - User reservations
- **Reservation_Seats** - Seats reserved in each reservation

## 👤 Default Users

The application creates default users on first run:

- **Admin User:**
  - Email: `admin@example.com`
  - Password: `123`
  - Role: Admin

- **Client Users:**
  - Email: `user1@example.com` / `user2@example.com`
  - Password: `123`
  - Role: Client

**⚠️ Important:** Change these default credentials in production!

## 🔧 Configuration

### Development Mode
The application runs in development mode by default with debug enabled. To change this, modify `app/__init__.py`:

```python
from config import Config as Config  # For production
# or
from config import TestingConfig as Config  # For testing
```

### Database Migrations

Create a new migration:
```bash
flask db migrate -m "Description of changes"
```

Apply migrations:
```bash
flask db upgrade
```

## 🎯 Usage

1. **Access the Application**: Navigate to `http://localhost:5000`
2. **Public View**: Browse movies and make reservations (no login required for viewing)
3. **Login**: Use admin credentials to access management features
4. **Manage Content**: 
   - Create genres and movies
   - Set up auditoriums with seats
   - Schedule movie functions
   - Manage users and roles

## 🔒 Security Notes

- Change the default `SECRET_KEY` in production
- Use strong passwords for database connections
- Update default user credentials
- Enable HTTPS in production
- Review and configure CORS settings if needed

## 📝 License

[Specify your license here]

## 🤝 Contributing

[Add contribution guidelines if applicable]

## 📧 Contact

[Add contact information if desired]

---

Built with ❤️ using Flask
