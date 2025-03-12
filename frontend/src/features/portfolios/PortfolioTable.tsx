import Table from "../../components/Table";
import StockRow from "../../hooks/StockRow";
import { useGetPortfolio } from "./useGetPortfolio";

const PortfolioTable = () => {
  const { data, isLoading } = useGetPortfolio();

  if (!data) {
    return <span>Portfolio Table used in wrong place</span>;
  }

  return (
    <Table columns="1fr 1fr 1fr 1fr 1fr 1fr 0.3fr">
      <Table.Header>
        <h1 className="">Ticker</h1>
        <h1 className="text-end">Avg Price</h1>
        <h1 className="text-end">Mkt Price</h1>
        <h1 className="text-end">Book Value</h1>
        <h1 className="text-end">Mkt Value</h1>
        <h1 className="text-end">Open P&L</h1>
        <h1>{/* this row is empty for options */}</h1>
      </Table.Header>
      <Table.Body
        data={data.stocks}
        render={(stock) => {
          return <StockRow key={stock.id} stock={stock} />;
        }}
        noDataMessage="No stocks. Start by adding a transaction."
        isLoading={isLoading}
      />
    </Table>
  );
};

export default PortfolioTable;
