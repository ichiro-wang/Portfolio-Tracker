type UserType = {
  id: string;
  name: string;
  email: string;
  profilePic: string;
  bookValue: number?;
  marketValue: number?;
};

type PortfolioType = {
  id: string;
  name: string;
  createdAt: Date;
  bookValue: number;
  marketValue: number;
};

type StockType = {
  id: string;
  ticker: string;
  createdAt: string; // ISO date format
  totalQuantity: number;
  closeQuantity: number;
  openQuantity: number;
  averagePrice: number;
  marketPrice: number;
  bookValue: number;
  marketValue: number;
};

type TransactionType = {
  id: string;
  type: "buy" | "sell";
  quantity: number;
  price: number;
  fees?: number;
  date: Date;
};

type SimpleMessageType = {
  message: string;
};

type SimpleErrorType = {
  error: string;
};
