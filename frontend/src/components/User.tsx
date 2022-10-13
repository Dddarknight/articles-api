import React from "react";
import axios from "axios"
import { Link, useParams } from "react-router-dom";
import { useNavigate } from "react-router"
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { fetchToken, authHeaders, deleteToken } from "./Auth";


const theme = createTheme();


export interface User {
  id: number;
  username: string;
  email: string;
  full_name: string;
  is_moderator: boolean;
}

export function User() {
  let params = useParams();
  const id = params.id
  const link_update = '/user/' + id +'/update'
  const link_delete = '/user/' + id +'/delete'

  let [loading, setLoading] = React.useState(true);
  let [user, setUser] = React.useState<User | null>(null);

  React.useEffect(() => {
    setLoading(true);
    const fetchData = async () => {
      const response = await fetch(`http://localhost:8080/users/${id}`);
      const newData = await response.json();
      setUser(newData);
      setLoading(false);
    };

    fetchData();
  }, []);

  return (
    <div>
    <Link to="/">Home</Link>
    {!loading && user ? (
        <Card sx={{ maxWidth: 345 }}>
        <CardContent>
            <Typography gutterBottom variant="h5" component="div">
                {user.username}
            </Typography>
            <Typography variant="body2" color="text.secondary">
                {user.full_name}
            </Typography>
            <Typography variant="body2" color="text.secondary">
                {user.email}
            </Typography>
        </CardContent>
        <CardActions>
        <Button size="small" href={link_update}>Update</Button>
        <Button size="small" href={link_delete}>Delete</Button>
        </CardActions>
        </Card>
    ) : null}
    </div>
  );
}

export function UserUpdate() {
    let params = useParams();
    const id = params.id;
    const navigate = useNavigate();
    const token = String(fetchToken());
    const headers = authHeaders(token);
    const url = 'http://localhost:8080/users/' + id;
  
    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const user_data = {
        'username': String(data.get('username')),
        'email': String(data.get('email')),
        'full_name': String(data.get('full_name')),
        'password': String(data.get('password')),
    };
    await axios.put(url, user_data, headers)
     .then((response) => {
       if(response){
        deleteToken(); 
        navigate("/");
       }
     });
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
            Update user
          </Typography>
          <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <TextField
                  autoComplete="username"
                  name="username"
                  required
                  fullWidth
                  id="username"
                  label="username"
                  autoFocus
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  id="full_name"
                  label="full_name"
                  name="full_name"
                  autoComplete="full_name"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  id="email"
                  label="email"
                  name="email"
                  autoComplete="email"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  name="password"
                  label="password"
                  type="password"
                  id="password"
                  autoComplete="password"
                />
              </Grid>
            </Grid>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Update
            </Button>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}


export function UserDelete() {
    let params = useParams();
    const id = params.id;
    const navigate = useNavigate();
    const token = String(fetchToken());
    const headers = authHeaders(token);
    const url = 'http://localhost:8080/users/' + id;
  
    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    await axios.delete(url, headers)
     .then((response) => {
       if(response){
         navigate("/");
       }
     });
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