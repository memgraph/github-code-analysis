import { NextPage } from "next";
import { useRouter } from "next/router";
import { useSession, signIn } from "next-auth/react";
import { useEffect, useRef, useState } from "react";
import axios from "axios";
import { Zoom, Grow, Box, List, ListItem, ListItemText, Grid, Paper, Divider, Typography, Chip, Backdrop, CircularProgress, IconButton, ButtonGroup, Snackbar, Alert, Input, InputAdornment} from "@mui/material";
import LoadingButton  from "@mui/lab/LoadingButton";
import PublicIcon from '@mui/icons-material/Public';
import VisibilityIcon from '@mui/icons-material/Visibility';
import StarIcon from '@mui/icons-material/Star';
import SearchIcon from '@mui/icons-material/Search';
import PersonIcon from '@mui/icons-material/Person';
import GitHubIcon from '@mui/icons-material/GitHub';
import RefreshIcon from '@mui/icons-material/Refresh';
import React from "react";


interface Repo {
    name: string,
    full_name: string,
    public: boolean,
    updated_at: string,
    languages: string[],
    github_url: string,
}


const Repos: NextPage = () => {
    const session = useSession()
    const router = useRouter()
    const [data, setData] = useState<Repo[]>([]);
    const [repos, setRepos] = useState<Repo[]>([]);
    const [starredRepos, setStarredRepos] = useState<Repo[]>([]);
    const [searchData, setSearchData] = useState<Repo[]>([]);
    const [open, setOpen] = useState(true);
    const [snackOpen, setSnackOpen] = useState(false);
    const [refreshLoading, setRefreshLoading] = useState(false);

    const oncePerLoad = useRef(false)

    const [filter, setFilter] = useState([true, false, false, false])

    const setFilterTo = (index: number) => {
        const newFilter = []
        for (let i = 0; i < filter.length; i++) {
            newFilter.push(false)
        }
        newFilter[index] = true
        setFilter(newFilter)
    }

    const filterAll = () => {
        setFilterTo(0)
        setSearchData(repos)
        setData(repos)
    }

    const filterPersonal = () => {
        if (session.data) {
            setFilterTo(1)
            const filterData = repos.filter(repo => repo.full_name.includes((session.data.login as string)+"/"))
            setSearchData(filterData)
            setData(filterData)
        }
    }

    const filterPrivate = () => {
        setFilterTo(2)
        const filterData = repos.filter(repo => !repo.public)
        setSearchData(filterData)
        setData(filterData)
    }

    const filterStarred = () => {
        setFilterTo(3)
        setSearchData(starredRepos)
        setData(starredRepos)
    }

    const search = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value
        const filtered = searchData.filter(repo => repo.full_name.toLowerCase().includes(value.toLocaleLowerCase()))
        setData(filtered)
    }

    console.log(session)

    useEffect(() => {
        if (session.status === "unauthenticated") {
            signIn();
        }

        if (session.status === "authenticated" && !oncePerLoad.current) {
            const getUserRepos = async () => {
                var bodyFormData = new FormData();
                bodyFormData.append('access_token', session.data.access_token as string);
                bodyFormData.append('login', session.data.login as string);

                try {
                    const result = await axios({
                        method: "POST",
                        url: process.env.BACKEND_URL + "/repos",
                        data: bodyFormData,
                        headers: {"Content-Type": "mutlipart/form-data"}
                    })

                    setOpen(false);
                    setRefreshLoading(false);
    
                    if (result.status === 200) {
                        setData(result.data.repos)
                        setSearchData(result.data.repos)
                        setRepos(result.data.repos)
                        setStarredRepos(result.data.starred)
                        setFilterTo(0)
                    } else {
                        setSnackOpen(true)
                    }

                } catch {
                    setOpen(false)
                    setSnackOpen(true)
                    setRefreshLoading(false);
                    signIn()
                    return                     
                }
            }

            getUserRepos()

            oncePerLoad.current = true
            
        }
    }, [session]);


    const refresh = () => {
        if (session.status === "authenticated") {
            setRefreshLoading(true)
            const getUserRepos = async () => {
                var bodyFormData = new FormData();
                bodyFormData.append('access_token', session.data.access_token as string);
                bodyFormData.append('login', session.data.login as string);

                try {
                    const result = await axios({
                        method: "POST",
                        url: process.env.BACKEND_URL + "/refresh-repos",
                        data: bodyFormData,
                        headers: {"Content-Type": "mutlipart/form-data"}
                    })

                    setOpen(false);
                    setRefreshLoading(false)
        
                    if (result.status === 200) {
                        setData(result.data.repos)
                        setSearchData(result.data.repos)
                        setRepos(result.data.repos)
                        setStarredRepos(result.data.starred)
                        setFilterTo(0)
                    } else {
                        setSnackOpen(true)
                    }

                } catch {
                    setRefreshLoading(true)
                    setOpen(false)
                    setSnackOpen(true)
                    return                     
                }
            }

            getUserRepos()
        }
    }

    return (
        <>
            <Backdrop
                sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
                open={open}>
                <CircularProgress color="inherit" />
            </Backdrop>

            <Snackbar open={snackOpen} autoHideDuration={5000} onClose={() => setSnackOpen(false)}>
                <Alert severity="error">An error occurred while getting repository data!</Alert>
            </Snackbar>
            <Box>

            </Box>
            <Grow in={!open}>
                <Grid container justifyContent={"center"} sx={{mt: "40px", mb:"5px"}}>
                    <Grid item lg={6} md={8} sm={8} xs={11}>
                        <Grid container justifyContent={"space-between"} alignContent={"end"}>
                            <Grid item lg={6} md={6} sm={6} xs={6}>
                                <ButtonGroup size={"small"} variant="outlined" aria-label="outlined button group">
                                    <IconButton onClick={() => filterAll()}><PublicIcon color={filter[0] ? "primary" : "secondary"} /></IconButton>
                                    <IconButton onClick={() => filterPersonal()}><PersonIcon color={filter[1] ? "primary" : "secondary"} /></IconButton>
                                    <IconButton onClick={() => filterPrivate()}><VisibilityIcon color={filter[2] ? "primary" : "secondary"} /></IconButton>
                                    <IconButton onClick={() => filterStarred()}><StarIcon color={filter[3] ? "primary" : "secondary"} /></IconButton>
                                </ButtonGroup>
                            </Grid>
                            <Grid item lg={6} md={6} sm={6} xs={6}>
                                <Box sx={{display: "flex", justifyContent: "flex-end", alignItems: "flex-end"}}>
                                    <Input
                                        id="standard-adornment-password"
                                        type={'text'}
                                        color={"primary"}
                                        endAdornment={
                                        <InputAdornment position="end">
                                            <IconButton
                                            aria-label="toggle password visibility"
                                            color={"primary"}
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
            </Grow>

            <Zoom in={!open}>
                <Grid container justifyContent={"center"} alignContent={"center"}>
                    <Grid item lg={6} md={8} sm={10} xs={11} sx={{borderRadius: "10px"}}>
                        <Paper elevation={2} >
                            <List sx={{ maxHeight: "75vh", overflow: "auto", width: '100%', bgcolor: 'white', pt: "0", pb: "0" }}>
                                <ListItem button onClick={() => refresh()}>
                                    <Grid container justifyContent={"center"} alignContent={"center"}>
                                        <Grid item lg={6} md={6} sm={6} xs={6}>
                                            <Box textAlign={"center"}><LoadingButton disableRipple sx={{backgroundColor: "transparent", "&.MuiButtonBase-root:hover": {bgcolor: "transparent"}}} color="primary" size="large" loading={refreshLoading} variant="text"> <RefreshIcon /> </LoadingButton></Box>

                                        </Grid>
                                    </Grid>

                                </ListItem>
                                {data.map((repo, index) => (
                                    <React.Fragment key={index}>
                                        <ListItem button secondaryAction={
                                            <>
                                                <Box sx={{display: {xs: "none", sm: "inline-block"}}}>
                                                    {repo.languages.map((language, lang_index) => {
                                                        let style = {mr: "5px", color: "white"}
                                                        if (lang_index > 3) {
                                                            style = {mr: "5px", display: {sm: "none", md: "none", lg: "inline-flex", color: "white"}} as any
                                                        }
                                                        if(lang_index > 3) {
                                                            return <React.Fragment key={lang_index}></React.Fragment>
                                                        }
                                                        return <Chip key={lang_index} color={"primary"} size="small" label={language} sx={style} />
                                                    })}
                                                </Box>
                                                <IconButton color={"secondary"} edge="end" href={repo.github_url}><GitHubIcon /></IconButton>
                                            </>
                                        }>
                                            <ListItemText
                                                onClick={() => router.push("/repo/"+repo.full_name)}
                                                primary={
                                                    <Typography variant={"body1"} noWrap={false} textAlign={"left"}>{repo.full_name} <Chip size={"small"} label={repo.public ? "Public": "Private"} color={"primary"} variant="outlined" component={"span"}/></Typography>
                                                }
                                                secondary={
                                                    <Box sx={{pt: {xs: "5px", sm: 0}, display: "inline-block"}} component="span">
                                                        <Typography variant="body2" component={"span"} sx={{mr: "5px"}}>{repo.updated_at}</Typography>
                                                        <Box sx={{display: {xs: "inline-block", sm: "none"}}} component="span">
                                                            {repo.languages.map((language, lang_index) => {
                                                                if (lang_index > 1) {
                                                                    return <React.Fragment key={lang_index}></React.Fragment>
                                                                }

                                                                if (lang_index > 0) {
                                                                    return <Chip key={lang_index} color={"primary"} variant="filled" size="small" label={language} component="span" sx={{ml: "5px", color: "white"}}/>
                                                                }

                                                                return <Chip key={lang_index} color={"primary"} variant="filled" size="small" label={language} component="span" sx={{color: "white"}}/>
                                                            })}
                                                        </Box>
                                                    </Box>

                                                } />
                                        </ListItem>

                                        {index !== data.length - 1 && <Divider variant="middle" component="li" />}
                                    </React.Fragment>


                                ))}
                            </List>
                        </Paper>
                    </Grid>
                </Grid>
            </Zoom>
        </>
    )
}


export default Repos;