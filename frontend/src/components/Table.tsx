import { createContext, ReactNode, useContext } from "react";
import Loader from "./Loader";

interface TableContextProps {
  columns: string;
}

const TableContext = createContext<TableContextProps | undefined>(undefined);

interface TableProps {
  columns: string;
  children: ReactNode;
}

const Table = ({ columns, children }: TableProps) => {
  return (
    <TableContext.Provider value={{ columns }}>
      <div role="table" className="w-full">
        {children}
      </div>
    </TableContext.Provider>
  );
};

interface RowProps {
  className?: string;
  children: ReactNode;
}

const TableRow = ({ className, children }: RowProps) => {
  const context = useContext(TableContext);
  if (!context) {
    throw new Error("Table component used outside Table");
  }

  return (
    <div
      className={`grid gap-2 ${className}`}
      style={{ gridTemplateColumns: `${context.columns}` }}
    >
      {children}
    </div>
  );
};

const Header = ({ className, children }: RowProps) => {
  const context = useContext(TableContext);
  if (!context) {
    throw new Error("Table component used outside Table");
  }

  return <TableRow className={`font-bold ${className}`}>{children}</TableRow>;
};

const Row = ({ className, children }: RowProps) => {
  const context = useContext(TableContext);
  if (!context) {
    throw new Error("Table component used outside Table");
  }

  return <TableRow className={`text-sm ${className}`}>{children}</TableRow>;
};

interface BodyProps<T> {
  data: T[] | undefined;
  render: (data: T) => ReactNode;
  noDataMessage: string;
  isLoading?: boolean;
}

const Body = <T,>({ data, render, noDataMessage, isLoading }: BodyProps<T>) => {
  if (isLoading) {
    return <Loader />;
  }

  if (!data) {
    return <h1>No data</h1>;
  }

  if (data.length === 0) return <span>{noDataMessage}</span>;

  return <div>{data.map(render)}</div>;
};

Table.Header = Header;
Table.Row = Row;
Table.Body = Body;

export default Table;
