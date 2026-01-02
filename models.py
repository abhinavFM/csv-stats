from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from database import Base


class CSVFileStats(Base):
    __tablename__ = "csv_file_stats"

    id = Column(Integer, primary_key=True, index=True)

    file_name = Column(String, nullable=False)
    row_count = Column(Integer, nullable=False)
    column_count = Column(Integer, nullable=False)
    numeric_statistics = Column(JSON, nullable=False) # Stores per-column statistics (mean, min, max, std, etc.)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return (
            f"<CSVFileStats(id={self.id}, "
            f"file_name='{self.file_name}', "
            f"rows={self.row_count}, "
            f"columns={self.column_count})>"
        )