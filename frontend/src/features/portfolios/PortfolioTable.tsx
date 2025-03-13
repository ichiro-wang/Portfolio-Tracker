import Menus from "../../components/Menus";
import Table from "../../components/Table";
import StockRow from "../stocks/StockRow";
import { useGetPortfolio } from "./useGetPortfolio";

const PortfolioTable = () => {
  const { data, isLoading } = useGetPortfolio();

  return (
    <Table columns="1fr 1fr 1fr 1fr 1fr 1fr 1fr 0.3fr">
      <Table.Header>
        <h1 className="">Ticker</h1>
        <h1 className="text-end">Quantity</h1>
        <h1 className="text-end">Avg<br />Price</h1>
        <h1 className="text-end">Mkt<br />Price</h1>
        <h1 className="text-end">Book<br />Value</h1>
        <h1 className="text-end">Mkt<br />Value</h1>
        <h1 className="text-end">Open<br />P&L</h1>
        <h1>{/* this row is empty for options */}</h1>
      </Table.Header>
      <Menus>
        <Table.Body
          data={data?.stocks}
          render={(stock) => {
            return (
              <StockRow key={stock.id} stock={stock}>
                <StockRow.StockDetails />
                <StockRow.TransactionDetails />
              </StockRow>
            );
          }}
          noDataMessage="No stocks. Start by adding a transaction."
          isLoading={isLoading}
        />
      </Menus>
    </Table>
  );
};

export default PortfolioTable;
