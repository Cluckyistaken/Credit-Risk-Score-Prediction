// simple fetch wrapper for backend API calls
export type ApiMethod = "GET" | "POST" | "PUT" | "DELETE";

const API_BASE = import.meta.env.VITE_API_URL ?? "";

async function request<T>(path: string, method: ApiMethod = "GET", data?: any): Promise<T> {
  const headers: Record<string,string> = {
    "Content-Type": "application/json"
  };

  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: data ? JSON.stringify(data) : undefined
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || res.statusText);
  }
  return res.json() as Promise<T>;
}

export const api = {
  get: <T>(p: string) => request<T>(p, "GET"),
  post: <T>(p: string, d?: any) => request<T>(p, "POST", d),
  put: <T>(p: string, d?: any) => request<T>(p, "PUT", d),
  del: <T>(p: string) => request<T>(p, "DELETE")
};
