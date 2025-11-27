export const formatCurrency = (n: number) =>
  n.toLocaleString("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 });

export const short = (s: string, len = 25) => (s.length > len ? s.slice(0, len - 1) + "…" : s);
