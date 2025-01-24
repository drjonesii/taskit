# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Set environment variables for Django
ENV DJANGO_ENV=development
ENV DJANGO_DEBUG=False
ENV POSTGRES_DB=your_database_name
ENV POSTGRES_USER=your_database_user
ENV POSTGRES_PASSWORD=your_database_password
ENV POSTGRES_HOST=your_database_host
ENV POSTGRES_PORT=5432

# Run the application
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver"]