# Portfolio Tracker

## Description

- A web application designed for investors to manage their portfolios efficiently. Users can track stock performance in real-time, manage transactions, and gain insights into their investments.

## Features

- User authentication and profile management.
- Management of investment portfolios, stocks, and transactions.
- Live tracking of stock prices and portfolio performance.
- Transaction management, including records of buying/selling stocks and profit/loss calculations.

## Tech Stack

### Backend:

- Python, Flask
  - Flask Login for session management
- Database:
  - PostgreSQL for relational data
  - Firebase for user profile pictures
- ORM: SQLAlchemy

### Frontend:

- React (TypeScript)
  - React Router for handling routes
  - React Query for managing remote state
  - Compound Component Pattern (Example [here](frontend/src/components/Modal.tsx))
  - Render Props Pattern (Example [here](frontend/src/components/Table.tsx))
- Styling: Tailwind CSS

## Testing

- Testing to be done
  - pytest, Postman for backend
  - Jest, React Testing Library for frontend
  - Cypress for E2E
- Originally used pytest for all testing before refactoring to react frontend
