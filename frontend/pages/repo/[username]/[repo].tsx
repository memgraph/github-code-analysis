import { NextPage } from "next";
import { useRouter } from "next/router";
import { signIn, useSession } from "next-auth/react";
import React, { useEffect, useRef, useState } from "react";
import axios from "axios";
import {Backdrop, CircularProgress, Grid, Typography, Paper, List, ListItem, ListItemText, Box, Button, Menu, MenuItem, Divider, Tooltip, Fab, Stack} from "@mui/material";
import LoadingButton from "@mui/lab/LoadingButton";
import RefreshIcon from "@mui/icons-material/Refresh";
import ArchiveIcon from '@mui/icons-material/Archive';
import FileCopyIcon from '@mui/icons-material/FileCopy';
import MoreHorizIcon from '@mui/icons-material/MoreHoriz';
import EditIcon from '@mui/icons-material/Edit';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import FileTree from "../../../comps/FileTree";
import NetworkGraph from "../../../comps/NetworkGraph";


interface Branch {
    name: string,
    commit_id: string,
}

interface Commit {
    commit_id: string,
    message: string,
    timestamp: number,
}

interface Graphs {
    [key: string]: {
        name: string,
        data: any,
    }
}

const noDataView = (
    <Box sx={{width:"100%", minHeight: "50vh", height: "100%"}}>
        <Grid container justifyContent={'center'} alignContent={'center'} spacing={0} sx={{height: "100%"}}>
            <Grid item xs={11}>
                <Typography textAlign={"center"} variant={"h5"}>
                    No data found
                </Typography>
                <Typography textAlign={"center"} variant={"body1"}>
                    Try refreshing the graph by pressing the button on the bottom right corner.
                </Typography>

            </Grid>
        </Grid>
    </Box>
)

const Repo : NextPage = () => {
    const router = useRouter()
    const session = useSession()
    const oncePerLoad = useRef(false)
    const [error, setError] = useState<null | string>(null)
    const [initialLoading, setInitialLoading] = useState(true)
    const [branchesLoading, setBranchesLoading] = useState(false)
    const [branches, setBranches] = useState<Branch[]>([])
    const [commits, setCommits] = useState<Commit[]>([])
    const [commitsLoading, setCommitsLoading] = useState(false)
    const [selectedCommit, setSelectedCommit] = useState<null | string>(null)
    const [selectedBranch, setSelectedBranch] = useState<string | null>(null)
    const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
    const open = Boolean(anchorEl);
    const handleClick = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };

    const [anchorElGraphs, setAnchorElGraphs] = React.useState<null | HTMLElement>(null);
    const openGraphs = Boolean(anchorElGraphs);
    const handleClickGraphs = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorElGraphs(event.currentTarget);
    };
    const handleCloseGraphs = () => {
        setAnchorElGraphs(null);
    };

    const [graphData, setGraphData] = useState<{[key: string]: Graphs} | undefined>(undefined)
    const [graphStatus, setGraphStatus] = useState<string | undefined>(undefined)
    const [isNew, setIsNew] = useState<boolean>(false)
    const isAlreadyLoading = useRef(false)
    const [selectedGraph, setSelectedGraph] = useState<string | null>(null)
    const [graphLoading, setGraphLoading] = useState(false)
    const [graphView, setGraphView] = useState<any>(null)

    let refreshGraphs: NodeJS.Timer
    const { username, repo } = router.query

    const getCommits = async (branch: string) => {
        if (session.status === "authenticated") {
            setError(null)
            setInitialLoading(true)
            try {
                const bodyFormData = new FormData();
                bodyFormData.append("access_token", session.data.access_token as string);
                bodyFormData.append('login', session.data.login as string);
                bodyFormData.append("full_name", `${username}/${repo}`);
                bodyFormData.append("branch", branch);

                const result = await axios.post(`${process.env.BACKEND_URL}/get_commits`, bodyFormData)

                if (result.status === 404) {
                    setError("Branch not found")
                    setInitialLoading(false)
                    return false
                }

                if (result.status !== 200) {
                    setError("Invalid branch")
                    setInitialLoading(false)
                    return false
                }


                setCommits(result.data)
                setSelectedCommit(result.data[0].commit_id)
                setInitialLoading(false)
            } catch (error) {
                setError("Error while getting commits")
                setInitialLoading(false)
                signIn()
            }
        }
    }

    const getBranches = async () => {
        if (session.status === "authenticated") {
            try {
                const bodyFormData = new FormData();
                bodyFormData.append("access_token", session.data.access_token as string);
                bodyFormData.append('login', session.data.login as string);
                bodyFormData.append("full_name", `${username}/${repo}`);

                const result = await axios.post(process.env.BACKEND_URL + "/get_branches", bodyFormData)
                console.log("result", result.data)


                if (result.status === 404) {
                    setError("Repository not found")
                    setInitialLoading(false)
                    return false
                }

                if (result.status !== 200) {
                    setError("Invalid repository")
                    setInitialLoading(false)
                    return false
                }

                setBranches(result.data.branches)
                setInitialLoading(false)
                setError(null)
                setSelectedBranch(result.data.default_branch)
                return true
            } catch (error) {
                setInitialLoading(false)
                setError("Error getting repository data")
                signIn()
                return false
            }
        }
    }

    const refreshBranches = async () => {
        setBranchesLoading(true)
        if (session.status === "authenticated") {
            setBranchesLoading(true)

            try {
                const bodyFormData = new FormData();
                bodyFormData.append("access_token", session.data.access_token as string);
                bodyFormData.append('login', session.data.login as string);
                bodyFormData.append("full_name", `${username}/${repo}`);

                const result = await axios.post(process.env.BACKEND_URL + "/refresh_branches", bodyFormData)
                console.log("result", result.data)


                if (result.status === 404) {
                    setError("Repository not found")
                    setBranchesLoading(false)
                    return false
                }

                if (result.status !== 200) {
                    setError("Invalid repository")
                    setBranchesLoading(false)
                    return false
                }

                setError(null)
                setBranches(result.data.branches)
                setSelectedBranch(result.data.default_branch)
                setBranchesLoading(false)
            } catch (error) {
                setBranchesLoading(false)
                setError("Error getting repository data")
                signIn()
                return false
            }
        }
    }

    const refreshCommits = async () => {
        setCommitsLoading(true)
        if (session.status === "authenticated") {

            try {
                const bodyFormData = new FormData();
                bodyFormData.append("access_token", session.data.access_token as string);
                bodyFormData.append('login', session.data.login as string);
                bodyFormData.append("full_name", `${username}/${repo}`);
                bodyFormData.append("branch", selectedBranch as string);

                const result = await axios.post(process.env.BACKEND_URL + "/refresh_commits", bodyFormData)
                console.log("result", result.data)

                if (result.status === 404) {
                    setError("Repository not found")
                    setCommitsLoading(false)
                    return false
                }

                if (result.status !== 200) {
                    setError("Invalid repository")
                    setCommitsLoading(false)
                    return false
                }

                setError(null)
                setCommits(result.data)
                setCommitsLoading(false)
                setSelectedCommit(result.data[0].commit_id)
            } catch (error) {
                setCommitsLoading(false)
                setError("Error getting repository data")
                signIn()
                return false
            }
        }
    }

    const getGraphs = async (branch: string, commit: string) => {
        if (session.status === "authenticated") {
            setError(null)
            setGraphLoading(true)
            try {
                const bodyFormData = new FormData();
                bodyFormData.append("access_token", session.data.access_token as string);
                bodyFormData.append('login', session.data.login as string);
                bodyFormData.append("full_name", `${username}/${repo}`);
                bodyFormData.append("commit", commit);
                bodyFormData.append("branch", branch);

                const result = await axios.post(process.env.BACKEND_URL + "/get_graphs", bodyFormData)
                console.log("result", result.data)

                if (result.status === 404) {
                    setError("Graphs not found")
                    setInitialLoading(false)
                    setGraphLoading(false)
                    return false
                }

                if (result.status !== 200) {
                    setError("Invalid call")
                    setInitialLoading(false)
                    setGraphLoading(false)
                    return false
                }

                setGraphData(result.data.data)
                setGraphStatus(result.data.status)
                setInitialLoading(false)
                setGraphLoading(false)
            } catch (error) {
                setError("Error while getting graphs")
                setInitialLoading(false)
                setGraphLoading(false)
                signIn()
            }
        }
    }

    const createGraphForBranch = async (branch: string | null) => {
        if (session.status === "authenticated" && branch !== null) {0
            setError(null)
            setInitialLoading(true)
            try {
                const bodyFormData = new FormData();
                bodyFormData.append("access_token", session.data.access_token as string);
                bodyFormData.append('login', session.data.login as string);
                bodyFormData.append("full_name", `${username}/${repo}`);
                bodyFormData.append("branch", branch);

                const result = await axios.post(process.env.BACKEND_URL + "/start_graph_builder", bodyFormData)
                console.log("result", result.data)

                if (result.status === 404) {
                    setError("Graphs not found")
                    setInitialLoading(false)
                    return false
                }

                if (result.status !== 200) {
                    setError("Invalid call")
                    setInitialLoading(false)
                    return false
                }

                setGraphStatus("loading")
                setIsNew(false)
                setInitialLoading(false)
            } catch (error) {
                setError("Error while getting graphs")
                setInitialLoading(false)
                signIn()
            }
        }
    }

    const graphStateUpdater = () => {
        if (graphStatus === "new") {
            setIsNew(true)
        } else if (graphStatus === "loading" && !isAlreadyLoading.current) {
            isAlreadyLoading.current = true
            refreshGraphs = setInterval(() => {
                // @ts-ignore
                if (graphStatus === "ready" || graphStatus === "new") {
                    isAlreadyLoading.current = false
                    clearInterval(refreshGraphs)
                }

                if (session.status === "authenticated" && selectedBranch && selectedCommit) {
                    getGraphs(selectedBranch, selectedCommit)
                }
            }, 10000)
        } else if (graphStatus === "ready") {
            setIsNew(false)
        }
    }

    useEffect(() => {
        graphStateUpdater()

        return () => {
            clearInterval(refreshGraphs)
        }
    }, [graphStatus])

    useEffect(() => {

        if (selectedCommit && selectedBranch) {
            getGraphs(selectedBranch, selectedCommit)
        }
    }, [selectedCommit])

    useEffect(() => {

        if (selectedBranch) {
            getCommits(selectedBranch)
        }
    }, [selectedBranch])

    useEffect(() => {
        if (session.status === "unauthenticated") {
            signIn();
        }

        if (!oncePerLoad.current && session.status === "authenticated") {
            oncePerLoad.current = true

            if (!username || !repo) {
                setInitialLoading(false)
                setError("Invalid repository")
                return
            }

            getBranches()
        }
    }, [router.query, session])

    useEffect(() => {
        setGraphView(noDataView)
        if (!graphData) return

        if (!selectedGraph && graphData) {
            setSelectedGraph(Object.keys(graphData)[0])
        }

        if (selectedGraph === "File Tree") {
            if (!graphData["File Tree"]) {
                setGraphView(noDataView)
                return () => {}
            }
            setGraphView(<FileTree data={graphData ? graphData["File Tree"] : undefined} />)
        }

        if (selectedGraph === "Dependencies") {
            if (!graphData["Dependencies"]) {
                setGraphView(noDataView)
                return
            }
            setGraphView(<NetworkGraph data={graphData ? graphData["Dependencies"] : undefined} />)
        }

    }, [graphData, selectedGraph, selectedCommit])

    return (
        <>
            <Backdrop
                sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
                open={initialLoading}>
                <CircularProgress color="inherit" />
            </Backdrop>

            <Menu
                id="branches-menu"
                MenuListProps={{
                    'aria-labelledby': 'branches-button',
                }}
                anchorEl={anchorEl}
                open={open}
                onClose={handleClose}
                sx={{maxHeight: "40vh", maxWidth: "400px"}}>
                <MenuItem>
                    <Grid container justifyContent={"center"} alignContent={"center"}>
                        <Grid item lg={12} md={12} sm={12} xs={12}>
                            <Box textAlign={"center"}><LoadingButton disableRipple sx={{backgroundColor: "transparent", "&.MuiButtonBase-root:hover": {bgcolor: "transparent"}}} color="primary" size="small" loading={branchesLoading} variant="text" onClick={() => refreshBranches()}> <RefreshIcon /> </LoadingButton></Box>
                        </Grid>
                    </Grid>
                </MenuItem>
                {branches.map((branch, index) => (
                    <MenuItem onClick={() => {
                        setSelectedBranch(branch.name)
                        handleClose()
                    }}
                              disableRipple key={index} selected={branch.name === selectedBranch}>
                        <Typography variant={"body1"} noWrap={true}>
                            {branch.name}
                        </Typography>
                    </MenuItem>
                ))}
            </Menu>

            <Menu
                id="graphs-menu"
                MenuListProps={{
                    'aria-labelledby': 'graphs-button',
                }}
                anchorEl={anchorElGraphs}
                open={openGraphs}
                onClose={handleCloseGraphs}
                sx={{maxHeight: "40vh"}}>
                {Object.keys(graphData ?? {}).map((graph, index) => (
                    <MenuItem onClick={() => {
                        setSelectedGraph(graph)
                        handleCloseGraphs()
                    }}
                              disableRipple key={index} selected={graph === selectedGraph}>
                        <Typography variant={"body1"} noWrap={true}>
                            {graph}
                        </Typography>
                    </MenuItem>
                ))}
            </Menu>


            <React.Fragment>
                <Grid container justifyContent={"center"} alignContent={"center"} spacing={3}>
                    <Grid item xs={12}>
                        <Typography variant="h4" align="center" sx={{mt: "20px"}}>
                            {username} / {repo}
                        </Typography>
                    </Grid>
                </Grid>

                <Grid container justifyContent={"center"} alignContent={"center"} spacing={3} sx={{mt: "10px", mb: "10px"}}>
                    <Grid item lg={11} md={11} sm={11} xs={11}>
                        <Grid container justifyContent={"space-between"} alignContent={"center"} spacing={3}>
                            <Grid item lg={6} md={6} sm={6} xs={6}>
                                <Box sx={{display: "flex", justifyContent: "flex-start"}}>
                                    <Button id={"branches-button"}
                                            variant={'contained'} color={'primary'} aria-controls={open ? 'branches-menu' : undefined}
                                            aria-haspopup="true"
                                            aria-expanded={open ? 'true' : undefined}
                                            disableElevation
                                            onClick={handleClick}
                                            size={"small"}
                                            endIcon={<KeyboardArrowDownIcon />}> Branches </Button>
                                </Box>
                            </Grid>
                            <Grid item lg={6} md={6} sm={6} xs={6} sx={{display: isNew ? "none" : "block"}}>
                                <Box sx={{display: "flex", justifyContent: "flex-end"}}>
                                    <Button id={"graphs-button"}
                                            variant={'contained'} color={'primary'} aria-controls={open ? 'graphs-menu' : undefined}
                                            aria-haspopup="true"
                                            aria-expanded={openGraphs ? 'true' : undefined}
                                            disableElevation
                                            onClick={handleClickGraphs}
                                            size={"small"}
                                            endIcon={<KeyboardArrowDownIcon />}> Graphs </Button>
                                </Box>
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>

                <Grid container justifyContent={"center"} alignContent={"center"} spacing={3} sx={{mb: "10px"}}>
                    <Grid item xs={11}>
                        <Paper elevation={3} >
                            <Grid container justifyContent={'center'} alignContent={'center'} spacing={0} sx={{borderRadius: "10px"}}>
                                <Grid item lg={2} md={3} sm={12} xs={12} sx={{boxShadow: {sm: "rgb(251, 110, 0, 1) 0 0.95px 1px", md: "rgb(251, 110, 0, 1) 0.95px 0 1px"}, backgroundColor: "#BCB6F605"}}>

                                        <List sx={{pt: "0", pb: "0", overflow: "auto", height: "70vh"}}>
                                            <ListItem>
                                                <Grid container justifyContent={"center"} alignContent={"center"}>
                                                    <Grid item lg={6} md={6} sm={6} xs={6}>
                                                        <Box textAlign={"center"}><Typography variant={"body1"} noWrap={true}> Commits </Typography></Box>
                                                    </Grid>
                                                </Grid>
                                            </ListItem>
                                            <Divider sx={{backgroundColor: "#FB6E00"}} />
                                            <ListItem button onClick={() => refreshCommits()}>
                                                <Grid container justifyContent={"center"} alignContent={"center"}>
                                                    <Grid item lg={6} md={6} sm={6} xs={6}>
                                                        <Box textAlign={"center"}><LoadingButton disableRipple sx={{backgroundColor: "transparent", "&.MuiButtonBase-root:hover": {bgcolor: "transparent"}}} color="primary" size="small" variant="text" loading={commitsLoading}> <RefreshIcon /> </LoadingButton></Box>
                                                    </Grid>
                                                </Grid>

                                            </ListItem>
                                            {commits.map((commit, index) => (
                                                <ListItem button onClick={() => {setSelectedCommit(commit.commit_id)}} key={index} selected={commit.commit_id === selectedCommit}>
                                                    <Tooltip title={

                                                            <Box component={"span"} sx={{display: "block", overflow: "auto", maxHeight: "90vh"}}>
                                                                {commit.message}
                                                            </Box>

                                                    } key={index} placement={"right-end"} arrow={true}>
                                                        <Typography variant={"body2"} textAlign={"center"} noWrap={true}>
                                                            {commit.message}
                                                        </Typography>
                                                    </Tooltip>
                                                </ListItem>
                                            ))}
                                        </List>

                                </Grid>

                                <Grid item lg={10} md={9} sm={12} xs={12} sx={{position: "relative", display: isNew ? "none" : "block"}}>
                                    <Fab component={"div"} color={"secondary"} size={"medium"} sx={{position: "absolute", bottom: "10px", right: "10px"}}>
                                        <LoadingButton sx={{color: "white", ".MuiLoadingButton-loadingIndicator": {color: "white"}, "&.MuiButtonBase-root:hover": {bgcolor: "transparent"}}} variant={"text"} loading={graphLoading} onClick={() => {
                                            if (selectedBranch && selectedCommit) getGraphs(selectedBranch, selectedCommit)
                                        }}>
                                            <RefreshIcon />
                                        </LoadingButton>

                                    </Fab>
                                    {graphView}

                                </Grid>

                                <Grid item lg={10} md={9} sm={12} xs={12} sx={{position: "relative", display: isNew ? "block" : "none", minHeight: "40vh"}}>
                                    <Stack direction="column"
                                           justifyContent="center"
                                           alignItems="center"
                                           spacing={2}
                                            sx={{height: "100%"}}>
                                        <Typography variant={"h5"}>
                                            No graphs found for this commit
                                        </Typography>
                                        <Button variant={"contained"} color={"primary"} onClick={() => createGraphForBranch(selectedBranch)}>
                                            Generate Graphs
                                        </Button>
                                    </Stack>


                                </Grid>

                            </Grid>
                        </Paper>
                    </Grid>
                </Grid>
            </React.Fragment>


        </>

    )
}
// {graphData && graphData["Dependencies"] && graphData["Dependencies"]?.nodes && <NetworkGraph data={graphData ? graphData["Dependencies"] : undefined} />}
// <FileTree data={graphData ? graphData["File Tree"] : undefined} />

export default Repo;