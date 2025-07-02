# E-Commerce API with Flask, SQLAlchemy, and JWT Authentication

## Overview
This project is a RESTful API for managing an e-commerce platform. It supports user authentication, product and order management, and relationships between users, orders, and products. The API includes JWT-based authentication for secure access.

## Features
- **User Management**: Create, retrieve, update, and delete users.
- **Product Management**: Manage products with pagination.
- **Order Management**: Create orders, associate products with orders, calculate total costs, and retrieve user-specific orders.
- **JWT Authentication**: Protects endpoints and ensures secure API usage.
- **Pagination**: Integrated pagination for user and product listings.

## Requirements
- Python 3.9+
- MySQL Database
- Virtual Environment with Flask and other dependencies installed.

## Dependencies
Install dependencies using `pip install -r requirements.txt`. Below are the key dependencies:
- `Flask`
- `Flask-SQLAlchemy`
- `Flask-Marshmallow`
- `Flask-JWT-Extended`
- `mysql-connector-python`

## Installation
1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Set up a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Update the database configuration in `app.py`:
    ```python
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://<USER>:<PASSWORD>@<HOST>/<DATABASE>'
    ```

5. Initialize the database:
    ```bash
    python
    >>> from app import db
    >>> db.create_all()
    ```

6. Run the application:
    ```bash
    python app.py
    ```

## API Endpoints

### Authentication
- **POST `/login`**
  - Input:
    ```json
    {
      "email": "user@example.com"
    }
    ```
  - Output:
    ```json
    {
      "access_token": "<JWT-TOKEN>"
    }
    ```

### User Endpoints
- **GET `/users`** (JWT Protected, Pagination Supported)
- **GET `/users/<id>`** (JWT Protected)
- **POST `/users`**
  - Input:
    ```json
    {
      "name": "John Doe",
      "address": "123 Main St",
      "email": "john@example.com"
    }
    ```
- **PUT `/users/<id>`** (JWT Protected)
- **DELETE `/users/<id>`** (JWT Protected)

### Product Endpoints
- **GET `/products`** (JWT Protected, Pagination Supported)
- **GET `/products/<id>`** (JWT Protected)
- **POST `/products`** (JWT Protected)
  - Input:
    ```json
    {
      "product_name": "Sample Product",
      "price": 100.50
    }
    ```
- **PUT `/products/<id>`** (JWT Protected)
- **DELETE `/products/<id>`** (JWT Protected)

### Order Endpoints
- **POST `/orders`** (JWT Protected)
  - Input:
    ```json
    {
      "user_id": 1
    }
    ```
- **PUT `/orders/<order_id>/add_product/<product_id>`** (JWT Protected)
- **DELETE `/orders/<order_id>/remove_product/<product_id>`** (JWT Protected)
- **GET `/orders/user/<user_id>`** (JWT Protected)
- **GET `/orders/<order_id>/products`** (JWT Protected)
- **GET `/orders/<order_id>/total`** (JWT Protected)
- **GET `/orders/user/<user_id>/latest`** (JWT Protected)

## Testing the API
1. Use a tool like Postman or curl to test the API.
2. Authenticate first by using the `/login` endpoint to get a JWT token.
3. Add the JWT token to the `Authorization` header for protected endpoints:
    ```
    Authorization: Bearer <JWT-TOKEN>
    ```

## Example Workflow
1. **Create a user**:
    ```bash
    curl -X POST http://localhost:5000/users -H "Content-Type: application/json" -d '{"name": "Alice", "email": "alice@example.com", "address": "123 Wonderland"}'
    ```

2. **Login to get a token**:
    ```bash
    curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d '{"email": "alice@example.com"}'
    ```

3. **Use the token for protected routes**:
    ```bash
    curl -X GET http://localhost:5000/users -H "Authorization: Bearer <JWT-TOKEN>"
    ```

## Database Schema
- **User**: `id`, `name`, `address`, `email`
- **Product**: `id`, `product_name`, `price`
- **Order**: `id`, `order_date`, `user_id`
- **OrderProduct**: `order_id`, `product_id`
