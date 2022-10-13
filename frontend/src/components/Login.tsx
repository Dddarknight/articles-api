import React from "react";
import { useNavigate } from "react-router"
import { fetchToken, setToken } from "./Auth"
import axios from "axios"
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import { createTheme, ThemeProvider } from '@mui/material/styles';

const theme = createTheme();

export function Login(){
  const navigate = useNavigate();
  const token = fetchToken();
  if(token !== null){
    return(
        <p>You are logged in</p>
  )};
  const login = async (event: React.FormEvent<HTMLFormElement>)=> {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
        const username = String(data.get('username'));
        const requestOptions = new URLSearchParams();
        requestOptions.append('username', username);
        requestOptions.append('password', String(data.get('password')));
        await axios.post('http://localhost:8080/token', requestOptions)
         .then((response) => {
           if(response.data.access_token){
             setToken(response.data.access_token);
             navigate("/");
           }
         })
         .catch((error) => {
           console.log(error,'error');
         });
     }
 
    return (
        <ThemeProvider theme={theme}>

        <Container component="main" maxWidth="xs">
          <CssBaseline />
          <Box
            sx={{
              marginTop: 8,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
            <Typography component="h1" variant="h5">
              Login
            </Typography>
            <Box component="form" onSubmit={login} noValidate sx={{ mt: 1 }}>
              <TextField
                margin="normal"
                required
                fullWidth
                id="username"
                label="username"
                name="username"
                autoComplete="username"
                autoFocus
              />
              <TextField
                margin="normal"
                required
                fullWidth
                name="password"
                label="password"
                type="password"
                id="password"
                autoComplete="password"
              />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
              >
                Sign In
              </Button>
    </Box>
    </Box>
    </Container>
    </ThemeProvider>
);
        }