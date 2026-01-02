# CSV Statistics API

A FastAPI-based REST API for uploading CSV files, analyzing their statistical properties, and storing/retrieving the results from a PostgreSQL database.

## Features

### CSV File Upload and Processing
Upload CSV files through a REST API endpoint. The system automatically validates the file format, reads the data, and extracts statistical information from numeric columns. Supports file validation, error handling, and automatic data parsing.

### Statistical Analysis
Automatically calculates comprehensive statistics for all numeric columns in uploaded CSV files. Computes count, mean, minimum, maximum, and standard deviation for each numeric column, providing detailed insights into the data distribution.

### Database Storage
Persists CSV file statistics and metadata to a PostgreSQL database for long-term storage and retrieval. Stores file names, row/column counts, statistical data, and timestamps for each processed CSV file.

### Retrieve All Statistics
Fetch all stored CSV statistics with pagination support using skip and limit parameters. Returns a list of all processed CSV files with their complete statistical information, enabling easy browsing and analysis of historical data.

### Retrieve Statistics by ID
Get specific CSV file statistics by providing the unique record ID. Returns detailed information for a single processed file, including all calculated statistics and metadata, with proper error handling for non-existent records.

### Docker Containerization
Fully containerized application using Docker and Docker Compose for easy deployment and environment consistency. Includes separate containers for the API service and PostgreSQL database, with automatic service orchestration and volume management.

## Technology Stack

### Backend Framework
- **FastAPI** - Modern, fast web framework for building APIs with automatic OpenAPI documentation
- **Uvicorn** - ASGI server for running FastAPI applications

### Database
- **PostgreSQL** - Relational database for persistent storage
- **SQLAlchemy** - Python SQL toolkit and ORM for database operations
- **psycopg2** - PostgreSQL adapter for Python

### Data Processing
- **Pandas** - Data manipulation and analysis library for CSV processing
- **NumPy** - Numerical computing library (dependency of Pandas)

### Validation & Serialization
- **Pydantic** - Data validation using Python type annotations

### Deployment
- **Docker** - Containerization platform
- **Docker Compose** - Multi-container Docker application orchestration

### Environment Management
- **python-dotenv** - Environment variable management from .env files

### Language
- **Python 3.11** - Programming language

## Project Setup

### Prerequisites
- Python 3.11 or higher
- Docker and Docker Compose installed
- PostgreSQL (if running without Docker)

### Environment Variables
Create a `.env` file in the project root with the following variables:

```env
DB_HOST=db
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
```

### Setup Instructions

#### Option 1: Using Docker (Recommended)

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd csv-stats
   ```

2. **Create the `.env` file** with your database credentials (see Environment Variables section above).

3. **Build and start the containers**:
   ```bash
   docker-compose up --build
   ```

4. **The API will be available at**:
   - API: `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`
   - Alternative Docs: `http://localhost:8000/redoc`

#### Option 2: Local Development Setup

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database** and update the `.env` file with your local database credentials.

5. **Run the application**:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **The API will be available at**:
   - API: `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`

### Useful Commands

#### Docker Commands
```bash
# Start services in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop services and remove volumes
docker-compose down -v

# Rebuild containers
docker-compose up --build
```

#### Database Commands (if running locally)
```bash
# Access PostgreSQL container shell
docker exec -it postgres_container psql -U your_database_user -d your_database_name

# View database tables
\dt

# Exit PostgreSQL shell
\q
```

## API Endpoints

- **POST** `/api/upload-csv/` - Upload and process a CSV file
- **GET** `/api/csv-stats/` - Retrieve all CSV statistics (supports `skip` and `limit` query parameters)
- **GET** `/api/csv-stats/{stats_id}` - Retrieve specific CSV statistics by ID

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

