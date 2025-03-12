import { formatCurrency } from "../../utils/formatCurrency";

interface Props {
  portfolio: PortfolioType;
}

const PortfolioRow = ({ portfolio }: Props) => {
  return (
    <>
      <span className="flex items-center font-bold">{portfolio.name}</span>
      <div className="flex flex-col">
        <span className="text-end">
          Book Value: {formatCurrency(portfolio.bookValue)}
        </span>
        <span className="text-end">
          Market Value: {formatCurrency(portfolio.marketValue)}
        </span>
      </div>
    </>
  );
};

export default PortfolioRow;
