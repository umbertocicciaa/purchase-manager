# 🛍️ Purchase Management System

A full-stack web application for managing customer purchases with receipt uploads, built with **FastAPI**, **Streamlit**, and **PostgreSQL**.

![H](static/homepage.jpeg)
![H](static/homepag2.jpeg)
![H](static/purchase-management.jpeg)
![H](static/purchase-management2.jpeg)

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Usage Guide](#-usage-guide)
- [Development](#-development)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🎯 Core Functionality

- **Purchase Upload**: Upload purchase details with PDF receipts
- **Advanced Search**: Search purchases by customer details, product, or date
- **Receipt Management**: Secure file storage and retrieval
- **Data Export**: Export search results to CSV format
- **Real-time Validation**: Client and server-side data validation

### 🔒 Data Management

- **Customer Information**: Store name, surname, codice fiscale, and credit card details
- **Product Details**: Track product names and prices
- **Receipt Storage**: Secure PDF file uploads with unique identifiers
- **Search Filters**: Multi-criteria search functionality

### 🎨 User Experience

- **Modern UI**: Clean, responsive Streamlit interface
- **Form Validation**: Real-time input validation with helpful error messages
- **Success Feedback**: Visual confirmation for completed actions
- **Error Handling**: Graceful error handling with user-friendly messages

## 🏗️ Architecture

This application follows a **clean architecture pattern** with clear separation of concerns:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│   Frontend      │────│    Backend      │────│   Database      │
│   (Streamlit)   │    │   (FastAPI)     │    │  (PostgreSQL)   │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Backend Architecture (FastAPI)

- **Model Layer**: Data models and schemas (SQLAlchemy + Pydantic)
- **Repository Layer**: Data access operations
- **Service Layer**: Business logic and file handling
- **Controller Layer**: HTTP request/response handling

### Frontend Architecture (Streamlit)

- **Components**: Reusable UI components
- **Services**: API communication layer
- **Pages**: Page logic and state management
- **Utils**: Validation and formatting utilities

## 🛠️ Tech Stack

### Backend

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[SQLAlchemy](https://sqlalchemy.org/)** - SQL toolkit and ORM
- **[Pydantic](https://pydantic.dev/)** - Data validation using Python type annotations
- **[PostgreSQL](https://postgresql.org/)** - Advanced open source database
- **[Uvicorn](https://uvicorn.org/)** - Lightning-fast ASGI server

### Frontend

- **[Streamlit](https://streamlit.io/)** - Turns Python scripts into web apps
- **[Requests](https://requests.readthedocs.io/)** - HTTP library for Python

### Infrastructure

- **[Docker](https://docker.com/)** - Containerization platform
- **[Docker Compose](https://docs.docker.com/compose/)** - Multi-container Docker applications

## 📋 Prerequisites

Before running this application, make sure you have:

- **Docker** (version 20.0+)
- **Docker Compose** (version 2.0+)
- **Git** (for cloning the repository)

### Installation Links

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/downloads)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd progetto-sistemi-distribuiti
```

### 2. Start the Application

```bash
# Start all services
docker-compose up

# Or run in background
docker-compose up -d
```

### 3. Access the Application

- **Frontend (Streamlit)**: <http://localhost:8501>
- **Backend API**: <http://localhost:8000>
- **API Documentation**: <http://localhost:8000/docs>
- **Database**: localhost:5434 (postgres/postgres)

### 4. Stop the Application

```bash
docker-compose down
```

## 📁 Project Structure

```
progetto-sistemi-distribuiti/
├── backend/                    # FastAPI Backend
│   ├── main.py                # Application entry point
│   ├── model.py               # Database models & Pydantic schemas
│   ├── repository.py          # Data access layer
│   ├── service.py             # Business logic layer
│   ├── controller.py          # HTTP request handlers
│   ├── database.py            # Database configuration
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Backend container config
│   └── uploads/              # File storage directory
├── frontend/                  # Streamlit Frontend
│   ├── app.py                # Application entry point
│   ├── components.py         # UI components
│   ├── services.py           # API communication
│   ├── pages.py              # Page logic
│   ├── models.py             # Data models
│   ├── utils.py              # Utilities & validation
│   ├── config.py             # Configuration
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile            # Frontend container config
├── docker-compose.yaml       # Multi-container orchestration
└── README.md                 # This file
```

## 📚 API Documentation

### Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `POST` | `/upload/` | Upload purchase with receipt | Form data + PDF file | Success message |
| `GET` | `/search` | Search purchases | Query parameters | Purchase list |
| `GET` | `/purchase/{id}` | Get single purchase | - | Purchase details |
| `DELETE` | `/purchase/{id}` | Delete purchase | - | Success message |
| `GET` | `/docs` | Interactive API docs | - | Swagger UI |

### Example API Calls

#### Upload Purchase

```bash
curl -X POST "http://localhost:8000/upload/" \
  -H "Content-Type: multipart/form-data" \
  -F "customer_name=John" \
  -F "customer_surname=Doe" \
  -F "customer_cf=JOHNDOE80A01H501U" \
  -F "credit_card=1234567890123456" \
  -F "product_name=Laptop" \
  -F "price=999.99" \
  -F "date=2025-01-15" \
  -F "receipt=@receipt.pdf"
```

#### Search Purchases

```bash
curl "http://localhost:8000/search?cf=JOHNDOE80A01H501U"
```

## 📖 Usage Guide

### 1. Upload a Purchase

1. **Navigate** to the frontend at <http://localhost:8501>
2. **Fill out the form** with customer and purchase details:
   - Customer Name, Surname, Codice Fiscale
   - Credit Card number
   - Product name and price
   - Purchase date
3. **Upload a PDF receipt**
4. **Click Submit** to save the purchase

### 2. Search Purchases

1. **Use the search section** to find purchases
2. **Apply filters** by:
   - Customer name or surname
   - Codice Fiscale
   - Credit card number
   - Product name
   - Purchase date
3. **View results** in a formatted table
4. **Export data** to CSV if needed

### 3. Manage Purchases

- **View details** of any purchase in the search results
- **Delete purchases** with confirmation dialogs
- **Export results** for external analysis

## 🔧 Development

### Running in Development Mode

#### Backend Development

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Development

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py --server.port 8501
```

#### Database Setup

```bash
# Start only the database
docker-compose up db

# Connect to database
docker-compose exec db psql -U postgres -d appdb
```

### Environment Variables

Create a `.env` file for local development:

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5434/appdb

# Backend
BACKEND_URL=http://localhost:8000

# File Upload
MAX_FILE_SIZE=10485760  # 10MB
UPLOAD_FOLDER=./uploads
```

### Adding New Features

Follow the established architecture patterns:

1. **Backend**: Model → Repository → Service → Controller → Route
2. **Frontend**: Model → Service → Component → Page → App

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Code Style

- Follow **PEP 8** for Python code
- Use **type hints** for better code documentation
- Add **docstrings** for functions and classes
- Write **tests** for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the [API Documentation](#-api-documentation)
3. Open an issue on GitHub
4. Contact the development team

---

**Made with ❤️ using FastAPI, Streamlit, and PostgreSQL**
