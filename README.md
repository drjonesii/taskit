# TaskIt

TaskIt is a task management application built with Django. It allows users to create, edit, delete, and vote on tasks. Users can also categorize tasks and view tasks created by all users.

## Features

- User registration and authentication
- Add, edit, delete, and vote on tasks
- Categorize tasks
- View tasks created by all users
- Sort tasks by various fields
- Responsive design with CSS styling

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/taskit.git
    cd taskit
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:
    - For development (SQLite):
        ```bash
        python manage.py migrate
        ```

    - For production (PostgreSQL):
        Set the following environment variables:
        ```bash
        export DJANGO_ENV=production
        export DJANGO_DEBUG=False
        export POSTGRES_DB=your_database_name
        export POSTGRES_USER=your_database_user
        export POSTGRES_PASSWORD=your_database_password
        export POSTGRES_HOST=your_database_host
        export POSTGRES_PORT=5432
        ```
        Then run the migrations:
        ```bash
        python manage.py migrate
        ```

5. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

6. Seed the database with initial data:
    ```bash
    python manage.py seed
    ```

7. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Usage

- Access the application at `http://127.0.0.1:8000/`.
- Register a new user or log in with an existing account.
- Add, edit, delete, and vote on tasks.
- View tasks created by all users.
- Sort tasks by various fields.

## Running Tests

To run the tests, use the following command:
```bash
python manage.py test tasks
