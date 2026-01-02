from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime


class CSVFileStatsResponse(BaseModel):
    id: int
    file_name: str
    row_count: int
    column_count: int
    numeric_statistics: Dict[str, Any]
    created_at: datetime

    class Config:
        orm_mode = True
