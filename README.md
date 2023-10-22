# Django REST API with PyMongo

This is a Django REST framework project with PyMongo as the database, featuring user Authentication, Throttling, and API endpoints for user management.

Prerequisites

    Python (3.7+)
    Django (3.x)
    Django REST framework
    PyMongo
    Postman (for testing APIs)

# Setup

Clone the repository:


    git clone https://github.com/SourabhKarma/user_login_mongo.git
    cd django_mongo

Create a virtual environment (recommended):


    python -m venv venv
    source venv/bin/activate  # On Windows, use: venv\Scripts\activate

Install dependencies:


    pip install -r requirements.txt

Configure the database settings in settings.py:


# settings.py
    url = "mongodb://localhost:27017"

    client  = pymongo.MongoClient(url)

    db = client[<"add your databse name">]

Configure the collection settings in signup/views.py :


# signup/views.py

    collection = db['< your_collection_name >'] 



Run the development server:


    python manage.py runserver

API Endpoints
User Registration

    Endpoint: /create_user/
    Method: POST
    Description: Register a new user
    Request Body:
        phone_number (string) - User's phone number
        password (string) - User's password
    Response: User registration successful

User Profile

    Endpoint: /profile/
    Method: GET
    Description: Retrieve user profile information
    Request Header:
        Authorization (string) - User's authentication token
    Response: User profile information in JSON format

User Logout

    Endpoint: /logout/
    Method: POST
    Description: Log out the user and clear sessions and token information
    Request Header:
        Authorization (string) - User's authentication token
    Response: Logged out successfully

# Authentication

This project uses Django's built-in authentication system. User passwords are securely hashed using Django's make_password function. Tokens are generated. When a user is created or logs in, a new token is generated and returned.

# Throttling

The project implements rate limiting (throttling) using Django Rest Framework's SimpleRateThrottle. Users are limited to 3 requests per hour per user. Custom rate limits can be set in the UserProfileThrottle class.
Custom Response for Throttle

A custom response for throttling is implemented. When the rate limit is exceeded, a response with a status code of 429 (Too Many Requests) and a custom message is returned.
Using PyMongo

PyMongo is used as the NoSQL database. Custom database functions are implemented to handle user registration, profile retrieval, and logout.

# Error Handling

Custom exception handling is implemented to provide meaningful error messages and responses for different scenarios.
