import { NextPage } from "next";
import { Grid, Typography, TextField, IconButton, InputBase, Divider, Paper } from "@mui/material";
import SearchIcon from '@mui/icons-material/Search';
import CloseIcon from '@mui/icons-material/Close';
import { FormEvent, useState, useEffect, useRef } from "react";
import { useSession, signIn } from "next-auth/react";
import axios from "axios";


const Search : NextPage = () => {
    const session = useSession()
    const oncePerLoad = useRef(false);
    const [search, setSearch] = useState("");
    const [trending, setTrending] = useState(true);

    useEffect(() => {
        if (session.status === "unauthenticated") {
            signIn();
        }

        if (session.status === "authenticated" && !oncePerLoad.current) {
            
            oncePerLoad.current = true;
        }
    }, [session]);

    return (
        <>
            <Grid container justifyContent={"center"} alignItems={"center"} direction={"row"} spacing={1} sx={{mt: "20px"}}>
                <Grid item lg={6} md={6} sm={8} xs={11}>
                <Paper
                    component="form"
                    sx={{ p: '2px 4px', display: 'flex', alignItems: 'center' }}
                    onSubmit={(event: FormEvent) => {
                        event.preventDefault();
                        console.log("ligma")
                    } }
                    >
                    <IconButton sx={{ p: '10px', display: trending ? "none" : "inherit" }} aria-label="clear" onClick={() => {
                        setSearch("");
                        setTrending(true);
                    }}>
                        <CloseIcon />
                    </IconButton>
                    <InputBase
                        sx={{ ml: 1, flex: 1 }}
                        placeholder="Search GitHub Repositories"
                        inputProps={{ 'aria-label': 'search github' }}
                        value={search}
                        onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                            setSearch(event.target.value);
                            if (event.target.value !== "") {
                                setTrending(false);
                            } else {
                                setTrending(true);
                            }
                        }}
                    />
                    <IconButton type="submit" sx={{ p: '10px' }} aria-label="search">
                        <SearchIcon />
                    </IconButton>
                    </Paper>
                </Grid>
            </Grid>
        </>
    )
}

export default Search;