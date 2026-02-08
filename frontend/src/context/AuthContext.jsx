import React, { createContext, useState, useEffect } from "react";
import { authAPI } from "../services/api";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      setUser({ token });
    }
    setLoading(false);
  }, []);

  // Step-1: send username+password, get otp send
  const loginStep1 = async (username, password) => {
    try {
      const response = await authAPI.LoginStep1({ username, password });
      console.log("OTP sent successfully:", response.data);
      return {
        success: true,
        username: response.data.username,
        message: response.data.message,
        email: response.data.email
      };
    } catch (e) {
      console.error("Login Step-1 failed:", e);
      throw e;
    }
  };

  // Step-2: send username+otp, get tokens
  const loginStep2 = async (username, otp) => {
    try {
      const response = await authAPI.LoginStep2({ username, otp });

      const accessToken = response.data.access;
      const refreshToken = response.data.refresh;

      // save token
      localStorage.setItem("access_token", accessToken);
      localStorage.setItem("refresh_token", refreshToken);

      setUser({ token: accessToken });

      console.log("Login successful");
      return { success: true };
    } catch (e) {
      console.error("Login Step-2 failed:", e);
      throw e;
    }
  };

  const register = async (username, email, password) => {
    try {
      const response = await authAPI.register({
        username,
        email,
        password,
      });
      console.log("Registration successful:", response.data);
    } catch (e) {
      console.error("Registration failed:", e);
      throw e;
    }
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{ user, loginStep1, loginStep2, register, logout, loading }}
    >
      {children}
    </AuthContext.Provider>
  );
};
