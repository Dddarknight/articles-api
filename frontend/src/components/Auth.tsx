export const authHeaders = (token: string)=>{
    return {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    };
  }

export const setToken = (token: string)=>{

    localStorage.setItem('token', token)
}

export const fetchToken = ()=>{

    return localStorage.getItem('token')
}

export const deleteToken = ()=>{

    localStorage.removeItem('token')
}
