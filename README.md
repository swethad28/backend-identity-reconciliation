# Backend Identity Reconciliation API

This project solves identity reconciliation for Zamazon.com shoppers by linking customer contact data (email and phone) across multiple purchases. Built as part of the Cloud & Backend Development, it uses a smart API to unify fragmented customer identities into a single source of truth.

---

##  Features

-  Create new contacts intelligently
-  Link emails/phones across purchases to a single customer
-  Maintains primary/secondary contact logic
-  Built using **FastAPI**, **SQLAlchemy**, and **SQLite**
-  Easy to test locally with `curl` or Postman

---

##  Tech Stack

| Tool         | Purpose                          |
|--------------|----------------------------------|
| Python 3.11+ | Backend language                 |
| FastAPI      | REST API framework               |
| SQLAlchemy   | ORM for database interaction     |
| SQLite       | Local database                   |
| Uvicorn      | ASGI server for running FastAPI  |
| Pydantic     | Data validation with email support |

---

##  Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/moonrider-identity-api.git
cd moonrider-identity-api
```
### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/Scripts/activate    # Windows Git Bash
```
### 3. Install Required Packages
```bash
pip install -r requirements.txt
```
### 4. Start the API Server
```bash
uvicorn main:app --reload
```
Server will be running at:
 http://127.0.0.1:8000

 How It Works

Accepts a POST request with the following JSON:

json
{
  "email": "example@zamazon.com",
  "phoneNumber": "1234567890"
}

The backend:
1. Checks if contact already exists
2. Merges data if matching contact is found
3. Creates primary/secondary contacts as needed
4. Returns a unified identity profile

Sample Test Cases
1. New Contact

```bash
curl -X POST http://127.0.0.1:8000/identify \
  -H "Content-Type: application/json" \
  -d '{"email": "doc1@zamazon.com", "phoneNumber": "1234567890"}'
```
Response:
json
{
  "primaryContactId": 1,
  "emails": ["doc1@zamazon.com"],
  "phoneNumbers": ["1234567890"],
  "secondaryContactIds": []
}

 2. Same Email, New Phone

```bash
curl -X POST http://127.0.0.1:8000/identify \
  -H "Content-Type: application/json" \
  -d '{"email": "doc1@zamazon.com", "phoneNumber": "9998887777"}'
```
Response:
json
{
  "primaryContactId": 1,
  "emails": ["doc1@zamazon.com"],
  "phoneNumbers": ["1234567890", "9998887777"],
  "secondaryContactIds": [2]
}

3. Same Phone, New Email

```bash
curl -X POST http://127.0.0.1:8000/identify \
  -H "Content-Type: application/json" \
  -d '{"email": "chandra@hiddenlab.com", "phoneNumber": "1234567890"}'
```
Response:
json
{
  "primaryContactId": 1,
  "emails": ["doc1@zamazon.com", "chandra@hiddenlab.com"],
  "phoneNumbers": ["1234567890", "9998887777"],
  "secondaryContactIds": [2, 3]
}

Requirements
Install all required packages with:

```bash
pip install -r requirements.txt
```


