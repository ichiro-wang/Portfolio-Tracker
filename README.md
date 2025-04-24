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
  - Models [here](backend/flasktracker/models.py)

### Frontend:

- React (TypeScript)
  - React Router for handling routes
  - React Query for managing remote state
  - Compound Component Pattern (Example [here](frontend/src/components/Modal.tsx))
  - Render Props Pattern (Example [here](frontend/src/components/Table.tsx))
- Styling: Tailwind CSS

## Testing

- Backend: pytest ([here](backend/tests/))

## Deployment

- Deployed using Render [here](https://portfolio-tracker-klvl.onrender.com)
- Note: Third-Party stock API has a daily limit, so market prices may not be fully updated

## App Screenshots
![image](https://github.com/user-attachments/assets/ae9b14d0-fdd2-40e0-af44-a1692ad31a81)
![image](https://github.com/user-attachments/assets/880b1638-2468-40da-a148-73bc402dc771)
![image](https://github.com/user-attachments/assets/a9100695-db90-4dc9-a9f8-9574d3b2ffa2)


