from datetime import datetime
from enum import Enum
from backend.flasktracker import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


# a user class that can contain several portfolios
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile_pic = db.Column(
        db.String(255),
        nullable=False,
        default="https://cdn.nba.com/headshots/nba/latest/1040x760/2544.png",
    )

    portfolios = db.relationship(
        "Portfolio",
        back_populates="owner",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="Portfolio.created_at",
    )

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "portfolios": [portfolio.to_json() for portfolio in self.portfolios],
            "createdAt": self.created_at.isoformat(),
        }

    @staticmethod
    def set_password(password):
        return bcrypt.generate_password_hash(password).decode("utf-8")

    def validate_password(self, password):
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

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    owner = db.relationship("User", back_populates="portfolios")

    stocks = db.relationship(
        "Stock",
        back_populates="portfolio",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="Stock.created_at",
    )

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "stocks": [stock.to_json() for stock in self.stocks],
            "createdAt": self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"Portfolio('{self.name}')"


# Stock wrapper class to prevent repeated API calls
class StockWrapper(db.Model):
    __tablename__ = "stock_wrappers"

    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(255), nullable=False)
    market_cache = db.Column(db.Float)

    updated_at = db.Column(db.DateTime)

    stocks = db.relationship(
        "Stock", back_populates="wrapper", lazy=True, cascade="all, delete-orphan"
    )

    def to_json(self):
        return {
            "id": self.id,
            "ticker": self.ticker,
            "marketCache": self.market_cache if self.market_cache else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
            # "stocks": [stock.to_json() for stock in self.stocks],
        }

    def __repr__(self):
        return f"StockWrapper('{self.ticker}', '{self.marketCache}')"


# These are the stocks within a portfolio
# They are wrapped by a StockWrapper to prevent repeated API calls
# Each stock can have several transactions
class Stock(db.Model):
    __tablename__ = "stocks"

    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(255), nullable=False)

    portfolio_id = db.Column(db.Integer, db.ForeignKey("portfolios.id"), nullable=False)
    portfolio = db.relationship("Portfolio", back_populates="stocks")

    wrapper_id = db.Column(
        db.Integer, db.ForeignKey("stock_wrappers.id"), nullable=False
    )
    wrapper = db.relationship("StockWrapper", back_populates="stocks")

    transactions = db.relationship(
        "Transaction",
        back_populates="stock",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="Transaction.date",
    )

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def to_json(self):
        return {
            "id": self.id,
            "ticker": self.ticker,
            "wrapper": self.wrapper.to_json() if self.wrapper else None,
            "transactions": [
                transaction.to_json() for transaction in self.transactions
            ],
            "createdAt": self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"Stock('{self.ticker}')"


class TransactionType(Enum):
    BUY = "buy"
    SELL = "sell"


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(TransactionType), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    quantity = db.Column(db.Float, nullable=False, default=0)
    price = db.Column(db.Float, nullable=False, default=0)
    fees = db.Column(db.Float, nullable=False, default=0)

    stock_id = db.Column(db.Integer, db.ForeignKey("stocks.id"), nullable=False)
    stock = db.relationship("Stock", back_populates="transactions")

    def to_json(self):
        return {
            "id": self.id,
            "type": self.type,
            "date": self.date.isoformat(),
            "quantity": self.quantity,
            "price": self.price,
            "fees": self.fees,
        }

    def __repr__(self):
        return f"Transaction('{self.type}', '{self.quantity}', '{self.price}')"
