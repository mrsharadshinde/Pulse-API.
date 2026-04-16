# Pulse API ⚡
> **The heartbeat of your digital life.**

A high-performance, robust REST API built with FastAPI and PostgreSQL. Pulse serves as the foundational backend infrastructure for a next-generation social ecosystem. It currently supports secure authentication, content publishing, and an interactive voting system utilizing advanced relational database architecture.

## 🛠️ Tech Stack

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (High performance, async-ready)
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Migrations:** Alembic
* **Data Validation:** Pydantic
* **Authentication:** JWT (JSON Web Tokens) & Passlib (Bcrypt hashing)

## ✨ Core Features

* **Secure Authentication:** Complete user registration and login system with JWT Bearer tokens and cryptographically hashed passwords.
* **Content Management (CRUD):** Users can create, read, update, and delete their own posts. Built-in authorization ensures users can only modify data they own.
* **Interactive Voting System:** A robust "Like/Unlike" mechanism built using a many-to-many bridge table and Composite Primary Keys to guarantee data integrity (preventing duplicate votes).
* **Advanced Database Queries:** Utilizes SQLAlchemy `LEFT OUTER JOINS` and `GROUP BY` functions to dynamically calculate post analytics (like counts) on the fly without database de-normalization.
* **Dynamic Search & Pagination:** Feed retrieval supports customizable query parameters including `limit`, `skip`, `sort`, and case-insensitive search filtering (`icontains`).

## 🚀 Local Development Setup

Follow these steps to get the Pulse API running on your local machine.

### 1. Clone the repository
```bash
git clone [https://github.com/mrsharadshinde/Pulse-API..git](https://github.com/mrsharadshinde/Pulse-API..git)
cd pulse-api

2. Create and activate a Virtual Environment
Bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Bash
pip install -r requirements.txt
4. Database Setup
Ensure you have PostgreSQL installed and running.

Create a new database for the project (e.g., pulse_db).

Set up your environment variables (create a .env file in the root directory) with your database credentials and JWT secret key.

5. Run Database Migrations
Use Alembic to push the table structures to your PostgreSQL database:

Bash
alembic upgrade head
6. Start the Server
Bash
uvicorn app.main:app --reload
The API will be available at http://127.0.0.1:8000

📚 API Documentation
Because this API is built with FastAPI, interactive documentation is generated automatically! Once the server is running, you can test all endpoints directly from your browser:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

Primary Endpoints
POST /users - Register a new user

POST /login - Authenticate and receive JWT

GET /posts - Fetch the social feed (with pagination & search)

POST /posts - Publish a new post

POST /vote - Like or unlike a post

🗺️ Future Roadmap (The Super App Vision)
Pulse is designed to eventually scale into a unified social ecosystem combining text, visual, and video media. Upcoming architectural expansions include:

[ ] Automated Testing Suite: Complete coverage using Pytest.

[ ] Dockerization: Containerizing the app and database for seamless deployment.

[ ] Multimedia CDN: S3 bucket integration for image and video hosting.

[ ] Real-Time WebSockets: Enabling live chat and instant notifications.