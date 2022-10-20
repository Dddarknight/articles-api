import React from "react";
import axios from "axios"
import { useParams } from "react-router-dom";
import { useNavigate } from "react-router";
import { useCookies } from "react-cookie";
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import Typography from '@mui/material/Typography';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { getAuthHeaders } from "./Auth";

const theme = createTheme();

const URL = 'http://localhost:8080/users/'

export function UserDelete() {
  let params = useParams();
  const id = params.id;
  const navigate = useNavigate();

  const [cookies, setCookie, removeCookie] = useCookies();
  const token = cookies.access_token;
  const headers = getAuthHeaders(token);
  
  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    try {
        await axios.delete(`${URL}${id}`, headers);
        removeCookie('access_token', { path: '/' });
      } catch (error) {
        console.error(error);
    };
    navigate("/");
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
            Delete user
          </Typography>
          <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
            
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Delete
            </Button>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}
