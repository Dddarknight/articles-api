import React from "react";
import { Link, useParams } from "react-router-dom";
import { useCookies } from "react-cookie";
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Typography from '@mui/material/Typography';
import useFetchData from "./Utils";
import { getAuthHeaders } from "./Auth";

const HOST = process.env.REACT_APP_HOST;
const URL = `http://${HOST}:8080/articles/`;

export interface Article {
  id: number;
  title: string;
  content: string;
}

export function ArticleRead() {
  const params = useParams();
  const id = params.id
  const [loading, setLoading] = React.useState(true);
  const [article, setArticle] = React.useState<Article | null>(null);
  const [cookies, setCookie, removeCookie] = useCookies();
  const token = cookies.access_token;
  const headers = getAuthHeaders(token);
  const url = `${URL}${id}`

  useFetchData(url, setArticle, headers, setLoading);

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
          <Button size="small" href={`/articles/${id}/update`}>Update</Button>
          <Button size="small" href={`/articles/${id}/delete`}>Delete</Button>
        </CardActions>
        </Card>
    ) : null}
    </div>
  );
}
