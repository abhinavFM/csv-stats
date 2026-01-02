from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
import pandas as pd
from io import BytesIO
from sqlalchemy.orm import Session

from models import CSVFileStats
from database import Base, engine, SessionLocal
from schemas import CSVFileStatsResponse
from typing import List

import models               # <-- IMPORTANT (forces model registration)

app = FastAPI(title="CSV Statistics API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ CREATE TABLES ON STARTUP
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)


@app.post("/api/upload-csv/")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Validate file type
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are allowed")

        try:
            contents = await file.read()
            df = pd.read_csv(BytesIO(contents))
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error reading CSV file: {str(e)}"
            )

        if df.empty:
            raise HTTPException(status_code=400, detail="CSV file is empty")

        # Select numeric columns
        numeric_df = df.select_dtypes(include="number")

        if numeric_df.empty:
            raise HTTPException(
                status_code=400,
                detail="No numeric columns found in CSV file"
            )

        # Basic statistics
        stats = {
            "row_count": len(df),
            "column_count": len(df.columns),
            "numeric_statistics": {}
        }

        for column in numeric_df.columns:
            stats["numeric_statistics"][column] = {
                "count": int(numeric_df[column].count()),
                "mean": float(numeric_df[column].mean()),
                "min": float(numeric_df[column].min()),
                "max": float(numeric_df[column].max()),
                "std": float(numeric_df[column].std())
            }

        csv_file_stats = CSVFileStats(
            file_name=file.filename,
            row_count=stats["row_count"],
            column_count=stats["column_count"],
            numeric_statistics=stats["numeric_statistics"]
        )
        db.add(csv_file_stats)
        db.commit()
        db.refresh(csv_file_stats)

        return stats
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/api/csv-stats/", response_model=List[CSVFileStatsResponse])
async def get_all_csv_stats(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all CSV file statistics from the database.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return (default: 100)
    """
    csv_stats = db.query(CSVFileStats).offset(skip).limit(limit).all()
    return csv_stats


@app.get("/api/csv-stats/{stats_id}", response_model=CSVFileStatsResponse)
async def get_csv_stats_by_id(stats_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific CSV file statistics by ID.
    
    - **stats_id**: The ID of the CSV file statistics record
    """
    csv_stats = db.query(CSVFileStats).filter(CSVFileStats.id == stats_id).first()
    if csv_stats is None:
        raise HTTPException(status_code=404, detail=f"CSV statistics with ID {stats_id} not found")
    return csv_stats