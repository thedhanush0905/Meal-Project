# Meal Project — Smart Meal Finder

Full-stack application to fetch meals from TheMealDB, compute ingredient counts and total calories, and provide AI-powered meal suggestions.

---

## Table of Contents

- Overview  
- Features  
- System Architecture  
- Tech Stack  
- Repository Structure  
- Data Flow  
- API Endpoints  
- Authentication Flow  
- Getting Started  
- Environment Variables  
- Development & Deployment  
- Git Workflow  
- License  

---

## Overview

This project allows users to:

- Sign up and log in securely (JWT authentication)  
- Search meals from TheMealDB  
- View meal details  
- Calculate ingredient-wise calories  
- Calculate total meal calories  
- Find meal with least ingredients  
- Ask AI-powered meal queries  
- Manage user profile  

All communication flows through the backend for security and clean architecture.

---

## Features

### Authentication

- User Signup  
- User Login  
- JWT-based authentication  
- Protected routes  

### Meal Features

- Search meals  
- View meal list  
- View single meal details  
- Find least ingredient meal  
- Calculate per-ingredient calories  
- Calculate total meal calories  

### AI Features

- Suggest low calorie meals  
- Suggest least ingredient meals  
- Smart nutrition-based queries  

### User

- View profile  
- Update profile  

---

## System Architecture

```
React Frontend
        ↓
Spring Boot Backend
        ↓
 ┌──────────────────┬──────────────────┐
 │ TheMealDB API    │ Nutrition API    │
 └──────────────────┴──────────────────┘
        ↓
Python FastAPI AI Service
```

Important:

- Frontend never calls AI directly.  
- Backend acts as central controller.  
- All services communicate via REST APIs (JSON).  

---

## Tech Stack

### Frontend

- ReactJS  
- TailwindCSS  
- Axios  
- React Router  

### Backend

- Java Spring Boot  
- Spring Security (JWT)  
- REST APIs  
- JPA / Hibernate  

### AI Service

- Python  
- FastAPI  

### External APIs

- TheMealDB API  
- Nutrition API (for calories)  

---

## Repository Structure

### Top Level

```
meal-project/
│
├── frontend/
├── backend/
├── ai/
└── README.md
```

---

### Frontend Structure

```
frontend/src/
│
├── components/
│   ├── Navbar.jsx
│   ├── Footer.jsx
│   ├── MealCard.jsx
│
├── pages/
│   ├── Login.jsx
│   ├── Signup.jsx
│   ├── Dashboard.jsx
│   ├── MealList.jsx
│   ├── MealDetail.jsx
│   ├── Profile.jsx
│   ├── AIQuery.jsx
│
├── services/
│   └── api.js
│
├── context/
│   └── AuthContext.jsx
│
├── App.jsx
└── main.jsx
```

---

### Backend Structure

```
backend/src/main/java/com/mealproject/
│
├── controller/
│   ├── AuthController.java
│   ├── MealController.java
│   ├── UserController.java
│   ├── AIController.java
│
├── service/
│   ├── AuthService.java
│   ├── MealService.java
│   ├── UserService.java
│
├── repository/
│   └── UserRepository.java
│
├── model/
│   ├── User.java
│   ├── Meal.java
│
├── config/
│   ├── SecurityConfig.java
│   └── JwtFilter.java
│
└── MealProjectApplication.java
```

---

### AI Service Structure

```
ai/
│
├── main.py
├── routes/
│   └── ai_routes.py
├── services/
│   └── meal_ai_service.py
└── requirements.txt
```

---

## Data Flow

### 1. Authentication Flow

Frontend → `/api/auth/signup`  
Frontend → `/api/auth/login`  

Backend → Generate JWT  

Frontend → Store JWT  

JWT required for protected endpoints.

---

### 2. Meal Search Flow

Frontend → `/api/meals?search=Arrabiata`  

Backend → Calls TheMealDB  

Backend → Returns meal list  

---

### 3. Least Ingredient Flow

Frontend → `/api/meals/least-ingredients`  

Backend → Counts non-empty ingredients  

Backend → Returns meal with minimum ingredients  

---

### 4. Calorie Calculation Flow

Backend fetches meal from TheMealDB  

Extracts:  
- `strIngredient1–20`  
- `strMeasure1–20`  

Backend calls Nutrition API for each ingredient  

Backend calculates `totalCalories`  

Backend returns:

```json
{
  "mealName": "Meal Name",
  "ingredients": [
    { "name": "Ingredient", "measure": "100g", "calories": 120 }
  ],
  "totalCalories": 450
}
```

Frontend displays:

- Ingredient name  
- Ingredient calories  
- Total calories  

---

### 5. AI Query Flow

Frontend → `/api/ai/query`  

Backend:
- Validates JWT  
- Forwards query to AI service  

AI service:
- Processes user query  
- May call backend logic  
- Returns suggestion  

Backend → Frontend  

---

## API Endpoints

### Auth

- `POST /api/auth/signup`  
- `POST /api/auth/login`  

### User

- `GET /api/user/profile`  
- `PUT /api/user/profile`  

### Meals

- `GET /api/meals`  
- `GET /api/meals/{id}`  
- `GET /api/meals/least-ingredients`  
- `GET /api/meals/{id}/calories`  

### AI

- `POST /api/ai/query`  

Example body:

```json
{
  "query": "Suggest meal under 500 calories"
}
```

---

## Getting Started

### Prerequisites

- Java 17+  
- Node 16+  
- Python 3.11+  
- Maven / Gradle  

---

### Clone Project

```bash
git clone <repo-url>
cd meal-project
```

---

### Run Frontend

```bash
cd frontend
npm install
npm run dev
```

---

### Run Backend

```bash
cd backend
./mvnw spring-boot:run
```

---

### Run AI Service

```bash
cd ai
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

---

## Environment Variables

### Backend

- JWT_SECRET  
- NUTRITION_API_KEY  
- AI_SERVICE_URL  
- SPRING_DATASOURCE_URL  
- SPRING_DATASOURCE_USERNAME  
- SPRING_DATASOURCE_PASSWORD  

### Frontend

- VITE_API_BASE_URL  

### AI Service

- OPENAI_API_KEY  

---

## Git Workflow

### Branches

- main (protected)  
- frontend  
- backend  
- ai  

### Rules

- Never push directly to main  
- Always create Pull Request  
- Pull latest main before starting work  
- Fix conflicts locally if they occur  

---

## License

This project is licensed under the MIT License.