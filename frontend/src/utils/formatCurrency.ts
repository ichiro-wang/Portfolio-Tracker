export const formatCurrency = (dollars: number): string => {
  return `$${Number(dollars).toFixed(2)}`;
};
