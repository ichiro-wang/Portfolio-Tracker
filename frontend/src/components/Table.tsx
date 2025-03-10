import { createContext, ReactNode, useContext } from "react";

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
      <div role="table">{children}</div>
    </TableContext.Provider>
  );
};

interface RowProps {
  children: ReactNode;
}

const TableRow = ({ children }: RowProps) => {
  const context = useContext(TableContext);
  if (!context) {
    throw new Error("Table Header used outside Table");
  }

  return (
    <div style={{ display: "grid", gridTemplateColumns: context.columns }}>
      {children}
    </div>
  );
};

const Header = ({ children }: RowProps) => {
  const context = useContext(TableContext);
  if (!context) {
    throw new Error("Table Header used outside Table");
  }

  return <TableRow>{children}</TableRow>;
};

const Row = ({ children }: RowProps) => {
  const context = useContext(TableContext);
  if (!context) {
    throw new Error("Table Header used outside Table");
  }

  return <TableRow>{children}</TableRow>;
};

interface BodyProps<T> {
  data: T[];
  render: (data: T) => ReactNode;
}

const Body = <T,>({ data, render }: BodyProps<T>) => {
  if (data.length === 0) return <span>No data to show</span>;

  return <div>{data.map(render)}</div>;
};

Table.Header = Header;
Table.Row = Row;
Table.Body = Body;

export default Table;
