# Portfolio Tracker

## Description

- This is a web app designed to help users manage their investment portfolios.
- Track multiple portfolios, and track the performance of each portfolio
- Track a portfolio's underlying stocks, and manage transactions such as buying or selling stocks.

## Features

- User authentication and profile management.
- Management of investment portfolios, stocks, and transactions.
- Live tracking of stock prices and portfolio performance.
- Transaction management, including records of buying/selling stocks and profit/loss calculations.

## Tech Stack

### Backend:

- Python, Flask
- ORM: SQLAlchemy

### Frontend:

- React (TypeScript)
  - React Router for handling routes
  - React Query for managing remote state
  - Compound Component Pattern (Example [here](frontend/src/components/Modal.tsx))
  - Render Props Pattern (Example [here](frontend/src/components/Table.tsx))
- Styling: Tailwind CSS

### Database:

- PostgreSQL
- Firebase for image files

## Testing

- Testing to be done
  - pytest, Postman for backend
- Originally used pytest before refactor
