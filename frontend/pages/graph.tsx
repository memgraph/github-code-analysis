import type { NextPage } from 'next';
import { Button, Container, Grid, TextField, Typography } from '@mui/material';
import React, { FormEvent, useState, useEffect } from 'react';
import axios from 'axios';
import FileTree from '../comps/FileTree';
import { useSession, signIn } from 'next-auth/react';
import NavBar from '../comps/NavBar';

const orgChart = {
  name: 'CEO',
  children: [
    {
      name: 'Manager',
      attributes: {
        department: 'Production',
      },
      children: [
        {
          name: 'Foreman',
          attributes: {
            department: 'Fabrication',
          },
          children: [
            {
              name: 'Worker',
            },
          ],
        },
        {
          name: 'Foreman',
          attributes: {
            department: 'Assembly',
          },
          children: [
            {
              name: 'Worker',
            },
          ],
        },
      ],
    },
  ],
};


const Graph: NextPage = () => {
  const [user, setUser] = useState("");
  const [repo, setRepo] = useState("");
  const [commitSha, setCommitSha] = useState("");
  const [accessToken, setAccessToken] = useState("");

  const session = useSession();


  useEffect(() => {
    if (session.status === "unauthenticated") {
      signIn();
    }

    if (session.status === "authenticated") {
      setUser(session.data.login as string);
      setAccessToken(session.data.accessToken as string);
    }
  } , [session]);

  const handleAPIRequest = async () => {
    var bodyFormData = new FormData();
    bodyFormData.append('user', user);
    bodyFormData.append('repo', repo);
    bodyFormData.append('commit_hash', commitSha);
    bodyFormData.append('access_token', accessToken);

    const result = await axios({
      method: "POST",
      url: process.env.BACKEND_URL,
      data: bodyFormData,
      headers: {"Content-Type": "mutlipart/form-data"}
    })

    console.log(result.data)
  }

  const formSubmit = (e: FormEvent<HTMLFormElement>) => {
    console.log(user, repo)
    e.preventDefault();
    handleAPIRequest();
  }


  return (
    <>
      <form onSubmit={formSubmit}>
        <Grid container
        direction="column"
        justifyContent="center"
        alignItems="center"
        spacing={2}>
          <Grid item lg={5} md={5} sm={5} xs={5}>
              <TextField
                name="user"
                id="outlined"
                label="User"
                onChange={(e) => setUser(e.target.value)}
              />
          </Grid>
          <Grid item lg={5} md={5} sm={5} xs={5}>
              <TextField
                name="repo"
                id="outlined"
                label="Repository"
                onChange={(e) => setRepo(e.target.value)}
              />
          </Grid>
          <Grid item lg={5} md={5} sm={5} xs={5}>
              <TextField
                name="commit_hash"
                id="outlined"
                label="Commit hash"
                onChange={(e) => setCommitSha(e.target.value)}
              />
          </Grid>
          <Grid item lg={5} md={5} sm={5} xs={5}>
              <TextField
                name="access_token"
                id="outlined"
                label="Access token"
                onChange={(e) => setAccessToken(e.target.value)}
              />
          </Grid>
          <Grid item lg={5} md={5} sm={5} xs={5}>
              <Button type="submit" variant="contained">Get filetree</Button>
          </Grid>
        </Grid>
      </form>

      <Container sx={{marginTop: "1rem", height: "50vh"}}>
        <FileTree data={orgChart}></FileTree>
      </Container>

    </>

    
  )
};

export default Graph;
