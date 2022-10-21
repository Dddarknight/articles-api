import React from "react";
import { useNavigate } from "react-router"
import { useCookies } from "react-cookie";
import axios from "axios"
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import { createTheme, ThemeProvider } from '@mui/material/styles';

const HOST = process.env.REACT_APP_HOST;
const URL = `http://${HOST}:8080/token`

const theme = createTheme();

export function Login(){
  const navigate = useNavigate();
  const [cookies, setCookie, removeCookie] = useCookies();
  const token = cookies.access_token;
  if (token) {
    return (
      <p>You are logged in</p>
    )
  };

  const login = async (event: React.FormEvent<HTMLFormElement>)=> {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const username = String(data.get('username'));
    const requestOptions = new URLSearchParams();
    requestOptions.append('username', username);
    requestOptions.append('password', String(data.get('password')));
    const response = await axios.post(URL, requestOptions)
    if (response.data.access_token) {
      setCookie('access_token', response.data.access_token, {maxAge: 900});
      navigate("/");
    };
  };
 
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