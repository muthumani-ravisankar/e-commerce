# E-Commerce API

This project is a  API for a simple e-commerce platform, developed using Flask, and pymongo in monogodb. It provides a comprehensive set of endpoints for user management and implemented with (jwt) token based
authentication and authorization. And implemented the role based access control 

## Features

### User Management

Users can sign up, log in, and have their information securely stored in the database. User passwords are hashed before storage for enhanced security. User can chang their passwords, which are stored and managed in mongodb.

### Roles
Users has a 3 different roles customers,vendors,admins. customer role default to every users signed up. vendor and admin roles are assigned only the admin.

### Products
Admins and Vendors can create, update, and delete the products and a user can  view,list, and order a product with proper authorization header (or) access token. 

### Error Handling

The API includes error handling, providing meaningful feedback to clients when errors occur.

### Configuration
make changes in `config.json` file by add your own mongodb connection string to access database and secret key.
```json
{
    "mongodb_string":"mongodb_connection_string",
    "secret_Key":"your_Secret_key"
}
```

## Installation

```bash
# Clone the repository

# Enter the project directory

# Install Python dependencies
pip install -r requirements.txt

# Travers the blog directory  and
# Run the application
python app.py
```
