type UserType = {
  id: string;
  name: string;
  email: string;
  profilePic: string;
  bookValue: number?;
  marketValue: number?;
};

type SimpleMessageType = {
  message: string;
};

type SimpleErrorType = {
  error: string;
};

type PortfolioType = {
  id: string;
  name: string;
  createdAt: Date;
  bookValue: number;
  marketValue: number;
};
