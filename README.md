UAV Rental Service
Welcome to the UAV Rental Service, a platform where users can rent or list UAVs (Unmanned Aerial Vehicles). This project provides an easy-to-use interface for managing UAV rentals, user authentication, and more.

Features
User Authentication: Register, login, and manage user accounts.
User Roles: Supports both regular users and sellers. Users can rent UAVs, while sellers can list their UAVs for rent.
UAV Management: Add, list, unlist, and delete UAVs.
Rental Management: Rent UAVs, manage rental records, and update rental statuses.
User Dashboards: Separate dashboards for sellers and users to manage their UAVs and rentals.
Prerequisites
Docker
Docker Compose
Getting Started
Setting Up the Project
Clone the repository to your local machine:

bash
Copy code
git clone https://github.com/yourusername/uav-rental-service.git
cd uav-rental-service
Ensure Docker and Docker Compose are installed on your machine.

Running the Project
Build and start the containers:

bash
Copy code
docker-compose up
Once the containers are up and running, visit http://0.0.0.0:8000/accounts/ to access the application.

Project Structure
landing_page.html: The landing page for the UAV Rental Service.
login.html: The login page for users.
membership.html: The membership settings page for users.
register.html: The registration page for new users.
seller_dashboard.html: The dashboard for sellers to manage their UAVs and rentals.
user_dashboard.html: The dashboard for users to browse available UAVs and manage their rentals.
forms.py: Django forms for user registration and profile updates.
models.py: Django models for CustomUser, UAV, RentalRecord, and UAVListing.
serializers.py: Django REST Framework serializers for user authentication and UAV management.
views.py: Django views for handling user registration, login, UAV management, and rental management.
docker-compose.yml: Docker Compose configuration file for setting up the database and web service.
Dockerfile: Dockerfile for building the web service container.
requirements.txt: List of dependencies for the project.
API Endpoints
User Authentication:

POST /accounts/api/register/ - Register a new user.
POST /accounts/api/login/ - Login a user and obtain an authentication token.
UAV Management:

GET /accounts/api/uavs/ - List UAVs.
POST /accounts/api/uavs/ - Create a new UAV.
PATCH /accounts/api/uavs/{id}/toggle_availability/ - Toggle UAV availability.
POST /accounts/api/uavs/{id}/list_uav/ - List a UAV with a price.
POST /accounts/api/uavs/{id}/unlist_uav/ - Unlist a UAV.
Rental Management:

POST /accounts/api/rent_uav/ - Rent a UAV.
GET /accounts/api/rental_records/ - List rental records for the logged-in user.
POST /accounts/api/rental_records/{id}/update_status/ - Update the status of a rental record.
POST /accounts/api/rentals/{id}/cancel/ - Cancel a pending rental.