import React from "react";
import axios from "axios";
import { Link, useParams } from "react-router-dom";
import { fetchToken, authHeaders } from "./Auth"
import { useNavigate } from "react-router"
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import TextareaAutosize from '@mui/base/TextareaAutosize';
import { createTheme, ThemeProvider } from '@mui/material/styles';


const theme = createTheme();


export interface Article {
  title: string;
  content: string;
}

export function Article() {
  let params = useParams();
  const id = params.id
  const link_update = '/article/' + id +'/update'
  const link_delete = '/article/' + id +'/delete'
  
  let [loading, setLoading] = React.useState(true);
  let [article, setArticle] = React.useState<Article | null>(null);
  const token = String(fetchToken());
  const headers = authHeaders(token);
  console.log(headers);
    
    React.useEffect(() => {
    setLoading(true);
    const fetchData = async () => {
      const response = await fetch(`http://localhost:8080/articles/${id}`, headers);
      const newData = await response.json();
      setArticle(newData);
      setLoading(false);
    };

    fetchData();
  }, []);

  return (
    <div>
    <Link to="/">Home</Link>
    {!loading && article ? (
        <Card sx={{ maxWidth: 345 }}>
        <CardContent>
            <Typography gutterBottom variant="h5" component="div">
                {article.title}
            </Typography>
            <Typography variant="body2" color="text.secondary">
                {article.content}
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


export function ArticleUpdate() {
    let params = useParams();
    const id = params.id;
    const navigate = useNavigate();
    const token = String(fetchToken());
    const headers = authHeaders(token);
    const url = 'http://localhost:8080/articles/' + id;
  
    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const article_data = {
        'title': String(data.get('title')),
        'content': String(data.get('content')),
    };
    await axios.put(url, article_data, headers)
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
            Update article
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
                  minRows={3}
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
              Update
            </Button>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}


export function ArticleDelete() {
    let params = useParams();
    const id = params.id;
    const navigate = useNavigate();
    const token = String(fetchToken());
    const headers = authHeaders(token);
    const url = 'http://localhost:8080/articles/' + id;
  
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
            Delete article
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