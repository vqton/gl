from app.extensions import db
from app.models.base import BaseModel


class FixedAsset(BaseModel):
    __tablename__ = "fixed_assets"

    asset_code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    asset_name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    original_cost = db.Column(db.Numeric(18, 2), nullable=False)
    residual_value = db.Column(db.Numeric(18, 2), default=0)
    depreciation_method = db.Column(db.String(30), default="straight_line")
    useful_life_years = db.Column(db.Integer, nullable=False)
    acquisition_date = db.Column(db.Date, nullable=False)
    depreciation_start_date = db.Column(db.Date, nullable=True)
    location = db.Column(db.String(100), default="")
    responsible_person = db.Column(db.String(100), default="")
    status = db.Column(db.String(20), default="active", nullable=False)
    accumulated_depreciation = db.Column(db.Numeric(18, 2), default=0)

    @property
    def net_book_value(self):
        return self.original_cost - self.accumulated_depreciation

    @property
    def monthly_depreciation(self):
        if self.depreciation_method == "straight_line":
            return (self.original_cost - self.residual_value) / (self.useful_life_years * 12)
        return 0

    def __repr__(self):
        return f"<FixedAsset {self.asset_code} - {self.asset_name}>"
