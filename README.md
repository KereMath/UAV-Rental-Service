######################################
# UAV Rental Service
######################################

Welcome to the UAV Rental Service, a platform where users can rent or list UAVs (Unmanned Aerial Vehicles). This project provides an intuitive interface for managing UAV rentals, user authentication, and more.

## Features

- **User Authentication**: Register, login, and manage user accounts.
- **User Roles**: Supports both regular users and sellers. Users can rent UAVs, while sellers can list their UAVs for rent.
- **UAV Management**: Add, list, unlist, and delete UAVs.
- **Rental Management**: Rent UAVs, manage rental records, and update rental statuses.
- **User Dashboards**: Separate dashboards for sellers and users to manage their UAVs and rentals.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

### Setting Up the Project
Ensure Docker and Docker Compose are installed on your machine.


Clone the repository to your local machine and Build and start the containers:


```bash

git clone https://github.com/KereMath/UAV-Rental-Service.git

cd UAV-Rental-Service/

sudo docker-compose up --build

```
After that just access this link via browser:

http://localhost:8001/accounts/

######################################
# Project Structure
######################################

- **landing_page.html**: Landing page for the UAV Rental Service.
- **login.html**: Login page for users.
- **membership.html**: Membership settings page for users.
- **register.html**: Registration page for new users.
- **seller_dashboard.html**: Dashboard for sellers to manage their UAVs and rentals.
- **user_dashboard.html**: Dashboard for users to browse available UAVs and manage their rentals.
- **forms.py**: Django forms for user registration and profile updates.
- **models.py**: Django models for CustomUser, UAV, RentalRecord, and UAVListing.
- **serializers.py**: Django REST Framework serializers for user authentication and UAV management.
- **views.py**: Django views for handling user registration, login, UAV management, and rental management.
- **docker-compose.yml**: Docker Compose configuration file for setting up the database and web service.
- **Dockerfile**: Dockerfile for building the web service container.
- **requirements.txt**: List of dependencies for the project.

######################################
# API Endpoints
######################################

### User Authentication

- **POST /accounts/api/register/**: Register a new user.
- **POST /accounts/api/login/**: Login a user and obtain an authentication token.

### UAV Management

- **GET /accounts/api/uavs/**: List UAVs.
- **POST /accounts/api/uavs/**: Create a new UAV.
- **PATCH /accounts/api/uavs/{id}/toggle_availability/**: Toggle UAV availability.
- **POST /accounts/api/uavs/{id}/list_uav/**: List a UAV with a price.
- **POST /accounts/api/uavs/{id}/unlist_uav/**: Unlist a UAV.

### Rental Management

- **POST /accounts/api/rent_uav/**: Rent a UAV.
- **GET /accounts/api/rental_records/**: List rental records for the logged-in user.
- **POST /accounts/api/rental_records/{id}/update_status/**: Update the status of a rental record.
- **POST /accounts/api/rentals/{id}/cancel/**: Cancel a pending rental.




