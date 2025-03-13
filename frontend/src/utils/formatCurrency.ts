export const formatCurrency = (dollars: number): string => {
  const isNegative = dollars < 0;
  return `${isNegative ? "-" : ""}$${Math.abs(dollars).toFixed(2)}`;
};
