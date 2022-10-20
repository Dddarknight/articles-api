
import React from "react";
import * as ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { UserRead } from "./components/User";
import { UsersRead } from "./components/Users";
import { UserUpdate } from "./components/User_update";
import { UserDelete } from "./components/User_delete";
import { Home } from "./components/Home";
import { ArticleRead } from "./components/Article";
import { ArticlesRead } from "./components/Articles";
import { ArticleCreate } from "./components/Article_create";
import { ArticleUpdate } from "./components/Article_update";
import { ArticleDelete } from "./components/Article_delete";
import { Login } from './components/Login';
import { Logout } from './components/Logout';
import { SignUp } from "./components/SignUp";
import { IsAuthenticated } from "./components/Utils";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="/sign-up" element={<SignUp />} />
        <Route path="/users" element={<UsersRead />} />
        <Route
          path="/user/:id"
          element={
            IsAuthenticated() ? (
              <UserRead />
            ) : (
            <Navigate replace to={"/login"} />
            )
          } />
        <Route
          path="/user/:id/update"
          element={
            IsAuthenticated() ? (
              <UserUpdate />
            ) : (
            <Navigate replace to={"/login"} />
            )
          } />
        <Route
          path="/user/:id/delete"
          element={
            IsAuthenticated() ? (
              <UserDelete />
            ) : (
            <Navigate replace to={"/login"} />
            )
          } />
        <Route
          path="/articles/:id"
          element={
            IsAuthenticated() ? (
              <ArticleRead />
            ) : (
            <Navigate replace to={"/login"} />
            )
          } />
        <Route
          path="/articles"
          element={
            IsAuthenticated() ? (
              <ArticlesRead />
            ) : (
            <Navigate replace to={"/login"} />
            )
          } />
        <Route
          path="/articles/create"
          element={
            IsAuthenticated() ? (
              <ArticleCreate />
            ) : (
            <Navigate replace to={"/login"} />
            )
          } />
        <Route
          path="/articles/:id/update"
          element={
            IsAuthenticated() ? (
              <ArticleUpdate />
            ) : (
            <Navigate replace to={"/login"} />
            )
          } />
        <Route
          path="/articles/:id/delete"
          element={
            IsAuthenticated() ? (
              <ArticleDelete />
            ) : (
            <Navigate replace to={"/login"} />
            )
          } />
      </Routes>
    </BrowserRouter>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root")!);
root.render(<App />);