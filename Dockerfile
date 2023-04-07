# Use the Python 3.9.7-buster image as the base image
FROM python:3.9.7-buster

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Install Nginx web server
RUN apt-get update && \
    apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/*

# Create a directory for the Django project
RUN mkdir Fermento

# Copy the entire current directory to the /Fermento directory in the container
COPY . /Fermento/

# Set the working directory to /Fermento
WORKDIR /Fermento

# Upgrade pip
RUN pip install --upgrade pip

# Install Python packages listed in requirements.txt
RUN pip install -r requirements.txt

# Create a directory for static files
RUN mkdir static

# Collect static files and run migrations
RUN python Fermento/manage.py collectstatic --noinput && python Fermento/manage.py migrate

# Copy the Nginx configuration file to the container's /etc/nginx/sites-available directory
COPY nginx.conf /etc/nginx/sites-available/default

# Expose port 6734 for the container
EXPOSE 6734

# Run the boot.sh script when the container starts
ENTRYPOINT ["./boot.sh"]
