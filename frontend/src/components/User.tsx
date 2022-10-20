import React from "react";
import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Typography from '@mui/material/Typography';
import useFetchData from "./Utils";

const URL = 'http://localhost:8080/users/'

export interface User {
  id: number;
  username: string;
  email: string;
  full_name: string;
  is_moderator: boolean;
}

export function UserRead() {
  const params = useParams();
  const id = params.id
  const [user, setUser] = useState<User | null>(null);
  const url = `${URL}${id}`
  const headers = {}
  const [loading, setLoading] = useState(true);

  useFetchData(url, setUser, headers, setLoading);

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
        <Button size="small" href={`/user/${id}/update`}>Update</Button>
        <Button size="small" href={`/user/${id}/delete`}>Delete</Button>
        </CardActions>
        </Card>
    ) : null}
    </div>
  );
}
