from datetime import datetime, timedelta
from enum import Enum
from flasktracker import db, bcrypt, login_manager
from flasktracker.utils.get_stock_details import get_stock_details
from sqlalchemy.orm import Mapped
from flask_login import UserMixin
from dotenv import load_dotenv
import os

load_dotenv()


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


# a user class that can contain several portfolios
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(255), nullable=False)
    email: Mapped[str] = db.Column(db.String(255), unique=True, nullable=False)
    password: Mapped[str] = db.Column(db.String(255), nullable=False)
    profile_pic: Mapped[str] = db.Column(
        db.String(255),
        nullable=False,
        default=os.getenv("DEFAULT_PICTURE"),
    )

    portfolios: Mapped[list["Portfolio"]] = db.relationship(
        "Portfolio",
        back_populates="owner",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="Portfolio.created_at",
    )

    @property
    def book_value(self):
        return sum(p.book_value for p in self.portfolios)

    @property
    def market_value(self):
        return sum(p.market_value for p in self.portfolios)

    created_at: Mapped[datetime] = db.Column(
        db.DateTime, nullable=False, default=datetime.now
    )

    def to_json(self, include_properties=False) -> dict:
        res = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "profilePic": self.profile_pic,
            "createdAt": self.created_at.isoformat(),
        }
        if include_properties:
            res.update({"bookValue": self.book_value, "marketValue": self.market_value})
        return res

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.generate_password_hash(password).decode("utf-8")

    def validate_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password, password)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"


# A portfolio class which contains the stocks that the user owns
class Portfolio(db.Model):
    __tablename__ = "portfolios"

    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(255), nullable=False)

    owner_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey("users.id"))
    owner: Mapped["User"] = db.relationship("User", back_populates="portfolios")

    stocks: Mapped[list["Stock"]] = db.relationship(
        "Stock",
        back_populates="portfolio",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="Stock.created_at",
    )

    created_at: Mapped[datetime] = db.Column(
        db.DateTime, nullable=False, default=datetime.now
    )

    @property
    def book_value(self):
        return sum(s.book_value for s in self.stocks)

    @property
    def market_value(self):
        return sum(s.market_value for s in self.stocks)

    def to_json(self, include_properties=False):
        res = {
            "id": self.id,
            "name": self.name,
            "createdAt": self.created_at.isoformat(),
        }
        if include_properties:
            res.update({"bookValue": self.book_value, "marketValue": self.market_value})
        return res

    def __repr__(self):
        return f"Portfolio('{self.name}')"


# Stock wrapper class to prevent repeated API calls
class StockWrapper(db.Model):
    __tablename__ = "stock_wrappers"

    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    ticker: Mapped[str] = db.Column(db.String(255), nullable=False)
    market_cache: Mapped[float] = db.Column(db.Float)

    updated_at: Mapped[datetime] = db.Column(db.DateTime)

    stocks: Mapped[list["Stock"]] = db.relationship(
        "Stock", back_populates="wrapper", lazy=True, cascade="all, delete-orphan"
    )

    def _update_cache(self):
        if not self.updated_at or self.updated_at < datetime.now() - timedelta(hours=8):
            data = get_stock_details(self.ticker)
            if data.get("error"):
                self.market_cache = 0.0
            else:
                self.market_cache = data.get("price")
                self.updated_at = datetime.now()
            db.session.commit()

    @property
    def market_price(self) -> float:
        self._update_cache()
        return self.market_cache

    def to_json(self):
        return {
            "id": self.id,
            "ticker": self.ticker,
            "marketPrice": self.market_cache if self.market_cache else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"StockWrapper('{self.ticker}', '{self.market_cache}')"


# These are the stocks within a portfolio
# They are wrapped by a StockWrapper to prevent repeated API calls
# Each stock can have several transactions
class Stock(db.Model):
    __tablename__ = "stocks"

    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    ticker: Mapped[str] = db.Column(db.String(255), nullable=False)

    portfolio_id: Mapped[int] = db.Column(
        db.Integer, db.ForeignKey("portfolios.id"), nullable=False
    )
    portfolio: Mapped["Portfolio"] = db.relationship(
        "Portfolio", back_populates="stocks"
    )

    wrapper_id: Mapped[int] = db.Column(
        db.Integer, db.ForeignKey("stock_wrappers.id"), nullable=False
    )
    wrapper: Mapped["StockWrapper"] = db.relationship(
        "StockWrapper", back_populates="stocks"
    )

    transactions: Mapped[list["Transaction"]] = db.relationship(
        "Transaction",
        back_populates="stock",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="Transaction.date",
    )

    created_at: Mapped[datetime] = db.Column(
        db.DateTime, nullable=False, default=datetime.now
    )

    @property
    def total_quantity(self):
        return sum(
            t.quantity for t in self.transactions if t.type == TransactionType.BUY
        )

    @property
    def close_quantity(self):
        return sum(
            t.quantity for t in self.transactions if t.type == TransactionType.SELL
        )

    @property
    def open_quantity(self):
        return self.total_quantity - self.close_quantity

    @property
    def average_price(self):
        return (
            sum(
                (t.quantity * t.price)
                for t in self.transactions
                if t.type == TransactionType.BUY
            )
            / self.total_quantity
            if self.total_quantity > 0
            else 0
        )

    @property
    def market_price(self):
        return self.wrapper.market_price

    @property
    def book_value(self):
        total = 0.0
        for t in self.transactions:
            transaction_cost = t.quantity * t.price
            total = (
                total + transaction_cost
                if t.type == TransactionType.BUY
                else total - transaction_cost
            )
        return total

    @property
    def market_value(self):
        return self.market_price * self.open_quantity

    def to_json(self, include_properties=False):
        res = {
            "id": self.id,
            "ticker": self.ticker,
            "wrapper": self.wrapper.to_json() if self.wrapper else None,
            "createdAt": self.created_at.isoformat(),
        }
        if include_properties:
            res.update(
                {
                    "totalQuantity": self.total_quantity,
                    "closeQuantity": self.close_quantity,
                    "openQuantity": self.open_quantity,
                    "averagePrice": self.average_price,
                    "marketPrice": self.market_price,
                    "bookValue": self.book_value,
                    "marketValue": self.market_value,
                }
            )
        return res

    def __repr__(self):
        return f"Stock('{self.ticker}')"


class TransactionType(Enum):
    BUY = "buy"
    SELL = "sell"


class Transaction(db.Model):
    __tablename__ = "transactions"

    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    type: Mapped["TransactionType"] = db.Column(
        db.Enum(TransactionType), nullable=False
    )
    date: Mapped[datetime] = db.Column(
        db.DateTime, nullable=False, default=datetime.now
    )
    quantity: Mapped[float] = db.Column(db.Float, nullable=False, default=0)
    price: Mapped[float] = db.Column(db.Float, nullable=False, default=0)
    fees: Mapped[float] = db.Column(db.Float, nullable=False, default=0)

    stock_id: Mapped[int] = db.Column(
        db.Integer, db.ForeignKey("stocks.id"), nullable=False
    )
    stock: Mapped["Stock"] = db.relationship("Stock", back_populates="transactions")

    def to_json(self):
        return {
            "id": self.id,
            "type": self.type.value,
            "date": self.date.isoformat(),
            "quantity": self.quantity,
            "price": self.price,
            "fees": self.fees,
        }

    def __repr__(self):
        return f"Transaction('{self.type}', '{self.quantity}', '{self.price}')"
