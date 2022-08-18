import type { NextPage } from "next";
import { Button, Container, Grid, TextField, Typography } from "@mui/material";
import NavBar from "../comps/NavBar";
import { useSession, signIn, signOut } from "next-auth/react";


const Index: NextPage = () => {
    const session = useSession();
    console.log("session", session);

    return (
        <>
            <Container maxWidth={"lg"} sx={{mt: "10px"}}>
                <Grid container justifyContent={"center"} alignItems={"center"} direction={"row"} spacing={1}>
                    <Grid item lg={12}>
                        <Typography variant={"h4"} noWrap={true} textAlign={"center"} component="div">
                            Welcome to the Github Code Analyser
                        </Typography>
                    </Grid>
                    <Grid item sm>
                        <Typography variant={"body2"} noWrap={true} textAlign={"center"} component="div">
                            This is a simple tool to analyse the codebase of a Github repository.
                        </Typography>
                    </Grid>
                </Grid>
            </Container>
                            
        </>
    );
}


export default Index;