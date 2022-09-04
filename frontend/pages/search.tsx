import { NextPage, NextPageContext } from "next";
import { Snackbar, Alert, Grid, List, Container, Skeleton, Typography, CircularProgress, IconButton, InputBase, Divider, Paper, Collapse, Card, CardContent, CardActions, Box, CardActionArea, Backdrop, ListItem, ListItemText } from "@mui/material";
import SearchIcon from '@mui/icons-material/Search';
import CloseIcon from '@mui/icons-material/Close';
import GitHub from "@mui/icons-material/GitHub";
import React, { FormEvent, useState, useEffect, useRef } from "react";
import { useSession, signIn } from "next-auth/react";
import axios from "axios";
import { LoadingButton } from "@mui/lab";
import { useRouter } from "next/router";


interface TrendingRepository {
    full_name: string,
    description: string,
    stars: number,
    stars_today: number,
    language: string,
    github_url: string,
}


interface SearchResult {
    full_name: string,
    description: string,
    stars: number,
    language: string,
    github_url: string,
}


const numberOfTrendingRepositories = 24;

const loadingTrendingItems: JSX.Element[] = []
for (let i = 0; i < numberOfTrendingRepositories; i++) {
    loadingTrendingItems.push(
        <Grid item lg={4} md={6} sm={6} xs={11} key={i}>
            <Card>
                <CardContent sx={{height: "250px"}}>
                    <Skeleton variant={"rectangular"} width={"40%"} height={"15px"} />
                    <Skeleton sx={{mt: "10px"}} variant={"rectangular"} width={"70%"} height={"25px"} />
                    <Skeleton sx={{mt: "10px"}} variant={"rectangular"} width={"50%"} height={"15px"} />
                    <Skeleton sx={{mt: "15px"}} variant={"rectangular"} width={"100%"} height={"100px"} />
                </CardContent>
                <CardActions sx={{mt: "20px"}}>
                    <Grid container justifyContent={"center"} alignItems={"center"} direction={"row"} spacing={1}>
                        <Grid item lg={12}>
                            <Box sx={{display: "flex", justifyContent: "center", alignItems: "center"}}><LoadingButton disableRipple sx={{backgroundColor: "transparent", "&.MuiButtonBase-root:hover": {bgcolor: "transparent"}}} color="inherit" size="large" loading={true} variant="text"> <GitHub /> </LoadingButton></Box>
                        </Grid>
                    </Grid>
                </CardActions>
            </Card>
        </Grid>
    )
}


const Search = () => {
    const session = useSession()
    const router = useRouter()
    const [search, setSearch] = useState<undefined | string>("");
    const [query, setQuery] = useState<undefined | string>(undefined);
    const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
    const [searchLoading, setSearchLoading] = useState(false);
    const [trending, setTrending] = useState(false);
    const [showCloseButton, setShowCloseButton] = useState(false);
    const [trendingLoading, setTrendingLoading] = useState(false);
    const [trendingData, setTrendingData] = useState<TrendingRepository[]>([]);
    const [snackOpen, setSnackOpen] = useState(false);

    const { q } = router.query as { q: string }
    const loadTrending = useRef(true);

    const getSearchResults = async () => {
        if (session.status === "authenticated") {
            const bodyFormData = new FormData();
            bodyFormData.append('access_token', session.data.access_token as string);
            bodyFormData.append('login', session.data.login as string);
            bodyFormData.append('query', q as string);

            try {
                const result = await axios({
                    method: "POST",
                    url: process.env.BACKEND_URL + "/search_repos",
                    data: bodyFormData,
                })

                setSearchResults(result.data);
                setSearchLoading(false);
            } catch {
                setSearchLoading(false);
                setSnackOpen(true);
                signIn();
            }
        }
    }

    const getTrendingRepositories = async () => {
        if (session.status === "authenticated") {
            try {
                const bodyFormData = new FormData();
                bodyFormData.append('access_token', session.data.access_token as string);
                bodyFormData.append('login', session.data.login as string);
                const result = await axios({
                    method: "POST",
                    url: process.env.BACKEND_URL + "/trending_repos",
                    data: bodyFormData,
                })
                setTrendingData(result.data);
                setTrendingLoading(false);
            } catch {
                setTrendingLoading(false);
                setSnackOpen(true);
                signIn();
            }
        }
    }

    useEffect(() => {
        if (session.status === "authenticated") {
            console.log("bitch", q, search)
            if (q !== undefined) {
                if (q !== query) {
                    loadTrending.current = true
                    setSearch(q);
                    setQuery(q)
                    setSearchLoading(true);
                    setShowCloseButton(true);
                    setTrending(false);
                    setTrendingLoading(false)
                    getSearchResults();
                }
            } else if (loadTrending.current) {
                loadTrending.current = false
                setSearch("");
                setSearchLoading(false);
                setShowCloseButton(false);
                setSearchResults([]);
                setTrending(true);
                setTrendingLoading(true);
                getTrendingRepositories();
            }
        }
    }, [router.query, session])

    useEffect(() => {
        if (session.status === "unauthenticated") {
            signIn()
        }
    } , [session])


    const searchFunction = async (event: FormEvent) => {
        event.preventDefault();

        if (session.status === "authenticated" && (search ?? "").length > 0) {
            await router.push({
                pathname: "/search",
                query: {
                    q: search
                }
            });
        }
    }

    return (
        <>
            <Snackbar open={snackOpen} autoHideDuration={5000} onClose={() => setSnackOpen(false)}>
                <Alert severity="error">An error occurred while getting repository data!</Alert>
            </Snackbar>

            <Grid container justifyContent={"center"} alignItems={"center"} direction={"row"} spacing={1} sx={{mt: "20px"}}>
                <Grid item lg={6} md={6} sm={8} xs={11}>
                <Paper
                    component="form"
                    sx={{ p: '2px 4px', display: 'flex', alignItems: 'center' }}
                    onSubmit={searchFunction}
                    >
                    <Collapse orientation="horizontal" in={showCloseButton}>
                        <IconButton sx={{ p: '10px'}} aria-label="clear" onClick={() => {
                            setSearch("");
                            setShowCloseButton(false);
                        }}>
                            <CloseIcon />
                        </IconButton>
                    </Collapse>
                    <InputBase
                        sx={{ ml: 1, flex: 1 }}
                        placeholder="Search GitHub Repositories"
                        inputProps={{ 'aria-label': 'search github' }}
                        name={"search"}
                        value={search}
                        autoFocus
                        onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                            setSearch(event.target.value);
                            if (event.target.value === "") {
                                setShowCloseButton(false)
                            } else {
                                setShowCloseButton(true)
                            }
                        }}
                    />
                    <IconButton type="submit" sx={{ p: '10px' }} aria-label="search">
                        <SearchIcon />
                    </IconButton>
                    </Paper>
                </Grid>
            </Grid>
            <Container sx={{mt:"50px", mb: "50px"}}>
                <Grid container justifyContent={"center"} alignItems={"center"} direction={"row"} spacing={3}>
                    {trendingLoading && loadingTrendingItems.map((item) => item)}

                    {trending && trendingData.map((repo: TrendingRepository, index) => (
                        <Grid item lg={4} md={6} sm={6} xs={11} key={index}>
                            <Card>
                                <CardActionArea onClick={() => router.push("/repo/"+repo.full_name)}>
                                    <CardContent sx={{height: "250px", overflow: "hidden"}}>
                                        <Typography variant="body2">Stars today: {repo.stars_today}</Typography>
                                        <Typography sx={{wordWrap: "break-word"}} variant="h5">{repo.full_name}</Typography>
                                        {repo.language && <Typography variant="body2" sx={{mt: "5px"}}>Programming language: {repo.language}</Typography>}
                                        <Typography variant="body1" sx={{mt: "15px", wordWrap: "break-word", overflow: "hidden"}}>{repo.description}</Typography>
                                    </CardContent>
                                </CardActionArea>
                                <CardActionArea component="a" href={repo.github_url} sx={{pt: "7px", pb: "7px"}}>
                                    <CardActions>
                                        <Grid container justifyContent={"center"} alignItems={"center"} direction={"row"} spacing={1}>
                                            <Grid item lg={12}>
                                                <Box sx={{display: "flex", justifyContent: "center", alignItems: "center"}}><GitHub color={"primary"} /></Box>
                                            </Grid>
                                        </Grid>
                                    </CardActions>
                                </CardActionArea>
                            </Card>
                        </Grid>
                    ))}
                </Grid>
                
                <Backdrop sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }} open={searchLoading}><CircularProgress color="inherit" /></Backdrop>
                <Paper elevation={2} >
                    <List sx={{pb: 0, pt: 0}}>
                        {searchResults.map((repo: SearchResult, index) => (
                            <React.Fragment key={index}>
                                <ListItem button  secondaryAction={
                                    <>
                                        <IconButton edge="end" href={repo.github_url}><GitHub color={"primary"} /></IconButton>
                                    </>
                                }>
                                    <ListItemText onClick={() => router.push("/repo/"+repo.full_name)} primary={repo.full_name} secondary={
                                        <>
                                            <Typography variant="body2" component="span" sx={{color: "text.secondary"}}>{repo.description}</Typography>
                                            <Typography variant="body2" component="span" sx={{color: "text.secondary", display: "block"}}>Language: {repo.language}</Typography>
                                        </>

                                    } />
                                </ListItem>
                                <Divider />
                            </React.Fragment>


                        ))}

                    </List>
                </Paper>
            </Container>
        </>
    )
}


export default Search;