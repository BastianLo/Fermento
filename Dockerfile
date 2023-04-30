# Use the Python 3.9.7-buster image as the base image
FROM python:3.9.7-buster

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Install Nginx web server
RUN apt-get update && \
    apt-get install -y nginx gettext && \
    rm -rf /var/lib/apt/lists/*

# Create a directory for the Django project
RUN mkdir Fermento

# Copy the entire current directory to the /Fermento directory in the container
COPY . /Fermento/

# Set the working directory to /Fermento
WORKDIR /Fermento

RUN curl -sL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs
# Copy the Vue.js app to the /client directory in the container
COPY client /client

# Install Node.js dependencies and build the Vue.js app
RUN cd /client && npm install && npm run build

# Copy the built Vue.js app to the Django static files directory
RUN cp -r /client/dist/* /Fermento/static/

# Upgrade pip
RUN pip install --upgrade pip

# Install Python packages listed in requirements.txt
RUN pip install -r requirements.txt

# Create a directory for static files
RUN mkdir /static

# Copy the Nginx configuration file to the container's /etc/nginx/sites-available directory
COPY nginx.conf /etc/nginx/sites-available/default

# Expose port 6733 for the container
EXPOSE 6733

# Run the boot.sh script when the container starts
ENTRYPOINT ["./boot.sh"]
