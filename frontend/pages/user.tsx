import { NextPage } from "next";
import { useSession, signIn } from "next-auth/react";
import { useEffect, useRef, useState } from "react";
import axios from "axios";
import { Box, List, ListItem, ListItemAvatar, Avatar, ListItemText, Grid, Paper, Divider, Typography, Chip, Backdrop, CircularProgress, IconButton, ButtonGroup, Snackbar, Alert, Input, InputLabel, InputAdornment } from "@mui/material";
import PublicIcon from '@mui/icons-material/Public';
import VisibilityIcon from '@mui/icons-material/Visibility';
import StarIcon from '@mui/icons-material/Star';
import SearchIcon from '@mui/icons-material/Search';
import React from "react";


interface Repo {
    name: string,
    full_name: string,
    public: boolean,
}



const User: NextPage = () => {
    const session = useSession()
    const [data, setData] = useState<Repo[]>([]);
    const [repos, setRepos] = useState<Repo[]>([]);
    const [starredRepos, setStarredRepos] = useState<Repo[]>([]);
    const [open, setOpen] = useState(true);
    const [snackOpen, setSnackOpen] = useState(false);
    const oncePerLoad = useRef(false)

    const [filter, setFilter] = useState([true, false, false, false])

    const search = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value
        const filtered = repos.filter(repo => repo.full_name.toLowerCase().includes(value.toLocaleLowerCase()))
        setData(filtered)
    }


    useEffect(() => {
        if (session.status === "unauthenticated") {
            signIn();
        }

        if (session.status === "authenticated" && !oncePerLoad.current) {
            const getUserRepos = async () => {
                var bodyFormData = new FormData();
                bodyFormData.append('access_token', session.data.access_token as string);

                const result = await axios({
                    method: "POST",
                    url: "http://127.0.0.1:5000/repos",
                    data: bodyFormData,
                    headers: {"Content-Type": "mutlipart/form-data"}
                })

                console.log(result)
                setOpen(false);

                if (result.status === 200) {
                    setData(result.data.repos)
                    setRepos(result.data.repos)
                    setStarredRepos(result.data.starred)
                } else {
                    setSnackOpen(true)
                }
            }

            getUserRepos()

            oncePerLoad.current = true
            
        }
    }, [session]);

    return (
        <>
            <Backdrop
                sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
                open={open}>
                <CircularProgress color="inherit" />
            </Backdrop>

            <Snackbar open={snackOpen} autoHideDuration={5000}>
                <Alert severity="error">An error occured while getting repository data!</Alert>
            </Snackbar>

            <Grid container justifyContent={"center"} sx={{mt: "20px", mb:"5px"}}>
                <Grid item lg={6} md={8} sm={8} xs={11}>
                    <Grid container justifyContent={"space-between"} alignContent={"end"}>
                        <Grid item lg={6} md={6} sm={6} xs={6}>
                            <ButtonGroup size={"small"} variant="outlined" aria-label="outlined button group">
                                <IconButton><PublicIcon color={filter[0] ? "primary" : "inherit"} /></IconButton>
                                <IconButton><VisibilityIcon color={filter[1] ? "primary" : "inherit"}/></IconButton>
                                <IconButton><StarIcon color={filter[2] ? "primary" : "inherit"}/></IconButton>
                            </ButtonGroup>
                        </Grid>
                        <Grid item lg={6} md={6} sm={6} xs={6}>
                            <Box sx={{display: "flex", justifyContent: "flex-end", alignItems: "flex-end"}}>
                                <Input
                                    id="standard-adornment-password"
                                    type={'text'}
                                    endAdornment={
                                    <InputAdornment position="end">
                                        <IconButton
                                        aria-label="toggle password visibility"
                                        >
                                            <SearchIcon />
                                        </IconButton>
                                    </InputAdornment>
                                    }
                                    placeholder="Search"
                                    onChange={search}
                                />
                            </Box>
                        </Grid>
                    </Grid>
                    
                </Grid>
            </Grid>

            <Grid container justifyContent={"center"} alignContent={"center"}>
                <Grid item lg={6} md={8} sm={8} xs={11}>
                    <Paper elevation={2}>
                        <List sx={{ width: '100%', bgcolor: 'white', pt: "0", pb: "0" }}>
                            {data.map((repo, index) => (
                                <React.Fragment key={index}>
                                    <ListItem button>
                                        <ListItemText 
                                            primary={
                                                <Typography variant={"body1"} noWrap={true} textAlign={"left"}>{repo.full_name} <Chip size={"small"} label={repo.public ? "Public": "Private"} variant="outlined" component={"span"}/></Typography>
                                            } 
                                            secondary="Jan 9, 2014" />
                                    </ListItem>

                                    {index !== data.length - 1 && <Divider variant="middle" component="li" />}
                                </React.Fragment>
                                
                                
                            ))}
                        </List>
                    </Paper>
                    
                </Grid>
            </Grid>
        </>
    )
}


export default User;