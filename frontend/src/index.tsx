
import React from "react";
import * as ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { User, UserUpdate, UserDelete } from "./components/User";
import { Home } from "./components/Home";
import { Article, ArticleCreate, ArticleUpdate, ArticleDelete } from "./components/Article";
import { Login } from './components/Login';
import { SignUp } from "./components/SignUp";
import { Users } from "./components/Users";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/sign-up" element={<SignUp />} />
        <Route path="/users" element={<Users />} />
        <Route path="/user/:id" element={<User />} />
        <Route path="/user/:id/update" element={<UserUpdate />} />
        <Route path="/user/:id/delete" element={<UserDelete />} />
        <Route path="/articles/:id" element={<Article />} />
        <Route path="/articles/create" element={<ArticleCreate />} />
        <Route path="/articles/:id/update" element={<ArticleUpdate />} />
        <Route path="/articles/:id/delete" element={<ArticleDelete />} />
      </Routes>
    </BrowserRouter>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root")!);
root.render(<App />);