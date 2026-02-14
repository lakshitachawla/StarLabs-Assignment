# 🏋️ Fitness Studio Booking API

A high-performance and secure **REST API** built with **FastAPI** and **MySQL** to manage fitness studio operations.
This system handles user authentication, class scheduling, and real-time booking management with strict adherence to **IST timezone requirements**.

---

## 🌟 Key Features

* **JWT Authentication**
  Secure token-based authentication using `python-jose` and password hashing with `bcrypt`.

* **Atomic Slot Management**
  Prevents overbooking by validating available slots before processing booking transactions.

* **IST Timezone Integration**
  All class schedules and bookings are stored and managed in **India Standard Time (IST)**.

* **Scalable Architecture**
  Modular structure combining:

  * Database Models
  * Pydantic Schemas
  * API Routes & Business Logic

* **Auto-Generated API Docs**
  Swagger/OpenAPI documentation available automatically.

---

## 🛠️ Tech Stack

| Component        | Technology           |
| ---------------- | -------------------- |
| Backend          | Python 3.12, FastAPI |
| Database         | MySQL                |
| ORM              | SQLAlchemy           |
| Security         | JWT (HS256), Bcrypt  |
| Validation       | Pydantic             |
| Timezone Support | PyTZ                 |

---

## 📋 System Architecture

The API follows a clean **Request → Validation → Persistence** flow:

1. **Request Validation**
   Incoming JSON requests are validated using Pydantic models.

2. **Security Layer**
   Dependency Injection ensures only authenticated users can access protected endpoints.

3. **Database Persistence**
   SQLAlchemy ORM manages MySQL transactions and commits changes safely.

---

## 🚀 Getting Started

### 1. Prerequisites

Ensure you have:

* Python **3.12+**
* MySQL Server running locally (`localhost`)

---

### 2. Database Setup

Login to your MySQL terminal and run:

```sql
CREATE DATABASE fitness_db;
```

---

### 3. Install Dependencies

Install all required packages:

```bash
pip install fastapi uvicorn sqlalchemy pymysql cryptography \
python-jose[cryptography] bcrypt pytz pydantic[email]
```

---

### 4. Run the Application

1. Save the project code in a file named:

```bash
main.py
```

2. Start the FastAPI development server:

```bash
uvicorn main:app --reload
```

---

### 5. Access API Documentation

Once the server is running, open:

* Swagger UI (Interactive Docs):
  [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

* OpenAPI JSON Schema:
  [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

---

## 🔐 Highlights

* FastAPI-powered high-performance backend
* Secure JWT authentication system
* Direct Bcrypt hashing (avoids passlib conflicts)
* IST-based scheduling and booking support
* Atomic slot decrement logic to prevent overbooking

---

## 👤 Author

**Lakshita Chawla**
Python Backend Developer Candidate
