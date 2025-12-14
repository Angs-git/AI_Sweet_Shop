# Sweet Shop Management System 🍬

A full-stack Sweet Shop Management System built as part of a technical kata.  
The application allows users to browse, search, and purchase sweets, while admin users can securely manage inventory.

This project demonstrates backend API design, authentication, role-based access control, frontend integration, and modern development practices.

---

## 🚀 Features

### Authentication & Authorization
- User login using JWT (OAuth2 Password Flow)
- Secure, token-based authentication
- Role-based access control (Admin vs User)

### Sweets Management
- View all available sweets
- Search sweets by name, category, and price range
- Purchase sweets (inventory updates automatically)

### Admin Capabilities
- Add new sweets
- Delete existing sweets
- Inventory protected by admin-only access

### Frontend
- Clean and responsive React UI
- Login screen
- Dashboard for viewing and searching sweets
- Admin-only UI for inventory management

---

## 🛠 Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication
- OAuth2 Password Flow

### Frontend
- React (Vite)
- JavaScript
- Fetch API
- Custom CSS

### Testing & Tools
- Pytest
- Swagger UI
- Git & GitHub

---

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register`
- `POST /api/auth/login`

### Sweets (Protected)
- `GET /api/sweets`
- `GET /api/sweets/search`
- `POST /api/sweets` (Admin only)
- `DELETE /api/sweets/{id}` (Admin only)
- `POST /api/sweets/{id}/purchase`

---

## ⚙️ Setup Instructions

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/Angs-git/AI_Sweet_Shop.git
cd ai-sweet-shop/backend
