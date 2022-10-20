import React from "react";
import { useNavigate } from "react-router"
import { useCookies } from "react-cookie";
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';

const theme = createTheme();

export function Logout(){
  const navigate = useNavigate();
  const [cookies, setCookie, removeCookie] = useCookies();

  const logout = async (event: React.FormEvent<HTMLFormElement>)=> {
    event.preventDefault();
    removeCookie('access_token'); 
    navigate("/");
  };

  return (
    <ThemeProvider theme={theme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box component="form" onSubmit={logout} noValidate sx={{ mt: 1 }}>
        <Button
          type="submit"
          fullWidth
          variant="contained"
          sx={{ mt: 3, mb: 2 }}
        >
            Logout
        </Button>
        </Box>
      </Container>
    </ThemeProvider>
);
};