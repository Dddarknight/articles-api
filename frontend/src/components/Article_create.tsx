import React from "react";
import axios from "axios";
import { getAuthHeaders } from "./Auth"
import { useNavigate } from "react-router";
import { useCookies } from "react-cookie";
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import Grid from '@mui/material/Grid';
import TextareaAutosize from '@mui/base/TextareaAutosize';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import { createTheme, ThemeProvider } from '@mui/material/styles';


const theme = createTheme();

const HOST = process.env.REACT_APP_HOST;
const URL = `http://${HOST}:8080/articles/create`;

export function ArticleCreate() {
    const navigate = useNavigate();
    const [cookies, setCookie, removeCookie] = useCookies();
    const token = cookies.access_token;
    const headers = getAuthHeaders(token);

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
      event.preventDefault();
      const data = new FormData(event.currentTarget);
      const article_data = {
        'title': String(data.get('title')),
        'content': String(data.get('content')),
      };
      const response = await axios.post(URL, article_data, headers);
      if (response) navigate("/articles");
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
            Create article
          </Typography>
          <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <TextField
                  autoComplete="title"
                  name="title"
                  required
                  fullWidth
                  id="title"
                  label="title"
                  autoFocus
                />
              </Grid>
              <Grid item xs={12}>
                <TextareaAutosize
                  required
                  id="content"
                  name="content"
                  autoComplete="content"
                  minRows={20}
                  style={{ width: 400 }}
                />
              </Grid>
            </Grid>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Create
            </Button>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}
