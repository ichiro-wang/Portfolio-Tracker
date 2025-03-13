type UserType = {
  id: number;
  name: string;
  email: string;
  profilePic: string;
  bookValue?: number;
  marketValue?: number;
};

type PortfolioType = {
  id: number;
  name: string;
  createdAt: Date;
  bookValue: number;
  marketValue: number;
};

type StockType = {
  id: number;
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
  id: number;
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
