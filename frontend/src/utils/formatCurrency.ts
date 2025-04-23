export const formatCurrency = (dollars: number | undefined): string => {
  if (dollars === undefined) {
    return "$0.00"
  }
  const isNegative = dollars < 0;
  return `${isNegative ? "-" : ""}$${Math.abs(dollars).toFixed(2)}`;
};
