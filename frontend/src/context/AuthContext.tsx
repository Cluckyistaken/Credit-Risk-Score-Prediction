import React, { createContext, useContext, useState, useEffect } from "react";

type User = { id: string; name: string; email: string } | null;

type AuthContextType = {
  user: User;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  register: (name: string, email: string, password: string) => Promise<void>;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User>(null);

  useEffect(() => {
    const raw = localStorage.getItem("cr_user");
    if (raw) setUser(JSON.parse(raw));
  }, []);

  const login = async (email: string, password: string) => {
    // fake login for demo — plug API here
    await new Promise((r) => setTimeout(r, 600));
    const fakeUser = { id: "u1", name: "Karthik", email };
    setUser(fakeUser);
    localStorage.setItem("cr_user", JSON.stringify(fakeUser));
  };

  const register = async (name: string, email: string, password: string) => {
    await new Promise((r) => setTimeout(r, 600));
    const newUser = { id: "u2", name, email };
    setUser(newUser);
    localStorage.setItem("cr_user", JSON.stringify(newUser));
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem("cr_user");
  };

  return <AuthContext.Provider value={{ user, login, logout, register }}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};
