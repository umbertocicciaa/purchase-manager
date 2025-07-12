# Purchase Management API - Refactored Architecture

This FastAPI application has been refactored following the **Model-Controller-Repository-Service** pattern for better separation of concerns and maintainability.

## Architecture Overview

### 📁 File Structure
```
backend/
├── main.py          # FastAPI application entry point
├── database.py      # Database configuration and connection
├── model.py         # Database models and Pydantic schemas
├── repository.py    # Data access layer
├── service.py       # Business logic layer
├── controller.py    # HTTP request handling (routes)
├── requirements.txt # Python dependencies
└── uploads/         # File storage directory
```

### 🏗️ Pattern Explanation

#### 1. **Model Layer** (`model.py`)
- **Purpose**: Defines data structures
- **Contains**:
  - `PurchaseDB`: SQLAlchemy database model
  - `PurchaseCreate`: Pydantic model for input validation
  - `PurchaseResponse`: Pydantic model for API responses
  - `PurchaseSearchParams`: Pydantic model for search parameters

#### 2. **Repository Layer** (`repository.py`)
- **Purpose**: Data access operations
- **Responsibilities**:
  - Database CRUD operations
  - Query building and execution
  - No business logic
- **Methods**:
  - `create_purchase()`: Insert new purchase
  - `get_purchase_by_id()`: Retrieve single purchase
  - `search_purchases()`: Search with filters
  - `delete_purchase()`: Remove purchase

#### 3. **Service Layer** (`service.py`)
- **Purpose**: Business logic and coordination
- **Responsibilities**:
  - File handling (upload/deletion)
  - Data transformation
  - Business rules enforcement
  - Error handling
- **Methods**:
  - `upload_purchase()`: Handle file upload + database save
  - `search_purchases()`: Format search results
  - `get_purchase_by_id()`: Retrieve and format single purchase
  - `delete_purchase()`: Remove purchase + associated file

#### 4. **Controller Layer** (`controller.py`)
- **Purpose**: HTTP request/response handling
- **Responsibilities**:
  - Request validation
  - Dependency injection
  - HTTP status codes
  - Error response formatting
- **Endpoints**:
  - `POST /upload/`: Upload purchase with receipt
  - `GET /search`: Search purchases (optional CF filter)
  - `GET /purchase/{id}`: Get single purchase
  - `DELETE /purchase/{id}`: Delete purchase

#### 5. **Database Layer** (`database.py`)
- **Purpose**: Database configuration
- **Contains**:
  - Database connection setup
  - Session management
  - Table creation

## 🎯 Benefits of This Architecture

### ✅ **Separation of Concerns**
- Each layer has a single responsibility
- Easy to test individual components
- Clear dependency flow: Controller → Service → Repository → Database

### ✅ **Maintainability**
- Changes in one layer don't affect others
- Easy to add new features
- Simple to modify business logic

### ✅ **Testability**
- Each layer can be unit tested independently
- Easy to mock dependencies
- Clear interfaces between layers

### ✅ **Scalability**
- Easy to add new endpoints
- Simple to extend business logic
- Can easily switch database implementations

## 🚀 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload/` | Upload purchase with receipt file |
| GET | `/search?cf={cf}` | Search purchases (optional CF filter) |
| GET | `/purchase/{id}` | Get purchase by ID |
| DELETE | `/purchase/{id}` | Delete purchase by ID |

## 💡 Key Improvements

1. **Better Error Handling**: Centralized error handling with proper HTTP status codes
2. **File Management**: Automatic cleanup of files when database operations fail
3. **Type Safety**: Strong typing with Pydantic models
4. **Dependency Injection**: Clean dependency management with FastAPI's dependency injection
5. **API Documentation**: Automatic OpenAPI/Swagger documentation
6. **Response Models**: Consistent API response format

## 🔄 Migration from Original Code

The original monolithic `main.py` has been split into multiple focused modules:
- Database models extracted to `model.py`
- Data operations moved to `repository.py` 
- Business logic centralized in `service.py`
- HTTP handling isolated in `controller.py`
- Database config separated to `database.py`

This refactoring maintains the same API functionality while providing a much more maintainable and extensible codebase.
