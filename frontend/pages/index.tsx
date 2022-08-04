import type { NextPage } from "next";
import { Button, Container, Grid, TextField, Typography } from "@mui/material";

import { useSession, signIn, signOut } from "next-auth/react";


const Index: NextPage = () => {
    const {data: session} = useSession();

    return (
        <Container>
            {session && <Typography>{session.login as string}</Typography>}
            {session && <Button variant={"contained"} color={"primary"} onClick={() => signOut()}>Sign out</Button>}
            {!session && <Button variant={"contained"} color={"primary"} onClick={() => signIn()}>Login</Button>}
        </Container>
    );
}


export default Index;