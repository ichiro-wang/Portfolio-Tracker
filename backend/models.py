from datetime import datetime
from enum import Enum
from flasktracker import db

# a user class that can contain several portfolios
class User(db.Model):
  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key=True)
  fullName = db.Column(db.String(255), nullable=False)
  email = db.Column(db.String(255), unique=True, nullable=False)
  password = db.Column(db.String(255), nullable=False)
  
  portfolios = db.relationship("Portfolio", back_populates="owner", lazy=True, cascade="all, delete-orphan", order_by="Portfolio.createdAt")

  createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
  
  def __repr__(self):
    return f"User('{self.fullName}', '{self.email}')"
  
# A portfolio class which contains the stocks that the user owns
class Portfolio(db.Model):
  __tablename__ = "portfolios"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  
  ownerId = db.Column(db.Integer, db.ForeignKey("users.id"))
  owner = db.relationship("User", back_populates="portfolios")
  
  stocks = db.relationship("Stock", back_populates="portfolio", lazy=True, cascade="all, delete-orphan", order_by="Stock.createdAt")
  
  createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
  
  def __repr__(self):
    return f"Portfolio('{self.name}')"

  
# Stock wrapper class to prevent repeated API calls
class StockWrapper(db.Model):
  __tablename__ = "stockWrappers"

  id = db.Column(db.Integer, primary_key=True)
  ticker = db.Column(db.String(255), nullable=False)
  marketCache = db.Column(db.Float)
  
  updatedAt = db.Column(db.DateTime)
  
  stocks = db.relationship("Stock", back_populates="wrapper", lazy=True, cascade="all, delete-orphan")
  
  def __repr__(self):
    return f"StockWrapper('{self.ticker}', '{self.marketCache}')"

  
# These are the stocks within a portfolio
# They are wrapped by a StockWrapper to prevent repeated API calls
# Each stock can have several transactions
class Stock(db.Model):
  __tablename__ = "stocks"
  
  id = db.Column(db.Integer, primary_key=True)
  ticker = db.Column(db.String(255), nullable=False)
  
  portfolioId = db.Column(db.Integer, db.ForeignKey("portfolios.id"), nullable=False)
  portfolio = db.relationship("Portfolio", back_populates="stocks")
  
  wrapperId = db.Column(db.Integer, db.ForeignKey("stockWrappers.id"), nullable=False)
  wrapper = db.relationship("StockWrapper", back_populates="stocks")
  
  transactions = db.relationship("Transaction", back_populates="stock", lazy=True, cascade="all, delete-orphan", order_by="Transaction.date")
  
  createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)

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
  
  stockId = db.Column(db.Integer, db.ForeignKey("stocks.id"), nullable=False)
  stock = db.relationship("Stock", back_populates="transactions")
  
  def __repr__(self):
    return f"Transaction('{self.type}', '{self.quantity}', '{self.price}')"


