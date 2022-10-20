import { useNavigate } from "react-router";
import { useState, useEffect } from "react";
import { useCookies } from "react-cookie";

export default function useFetchData (
    url: string,
    setObject: any,
    headers: any,
    setLoading: (bool: boolean) => void,
    ) {
      const navigate = useNavigate();
      useEffect(() => {
        async function fetchNewData() {
          setLoading(true);
          const response = await fetch(url, headers);
          const newData = await response.json();
          if (response.status !== 200) navigate('/');
          setObject(newData);
          setLoading(false);
        };

        fetchNewData();
          }, []); 
};

export const useDeleteCookie = () => {
  const [cookies, setCookie, removeCookie] = useCookies();
  removeCookie('access_token'); 
};


export const IsAuthenticated = () => {
    
    const [cookies, setCookie, removeCookie] = useCookies();
    const token = cookies.access_token;
    if (!token) {
        return false;
    };
    return true;
};