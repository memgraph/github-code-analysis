import { AppBar, Box, Typography, Container, Toolbar, Menu, MenuItem, Button, IconButton, Tooltip, Avatar, Grid } from "@mui/material";
import MenuIcon from '@mui/icons-material/Menu';
import { useState } from "react";
import { useSession, signIn, signOut } from "next-auth/react";
import Link from "next/link";
import { useRouter } from "next/router";
import { useTheme } from '@mui/material/styles';


const pages = [ {title: "Repositories", link: "/repos", authenticated: true}, 
                {title: "Search", link: "/search", authenticated: true}];


const NavBar = () => {
    const session = useSession();
    const router = useRouter();
    const theme = useTheme();

    const [anchorElNav, setAnchorElNav] = useState<null | HTMLElement>(null);

    const handleOpenNavMenu = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorElNav(event.currentTarget);
    };
    const handleOpenUserMenu = (event: React.MouseEvent<HTMLElement>) => {
        signOut({redirect: true, callbackUrl: "/"});
    };

    const handleCloseNavMenu = () => {
        setAnchorElNav(null);
    };

    const showPages = pages.filter(page => {
        if (page.authenticated) {
            return session.status === "authenticated";
        } else {
            return true;
        }
    });


    let username = ""
    let avatar_url = ""
    if (session.status === "authenticated") {
        username = session.data.login as string;
        avatar_url = session.data.avatar_url as string;
    }

    const loggedInMenu = (
        <>
            <Tooltip title="Click to logout" onClick={handleOpenUserMenu}>
                <Grid container justifyContent={"center"} alignItems={"center"} direction={"row"} spacing={1}>
                    <Grid item sm>
                        <Avatar alt="User Avatar" src={avatar_url} />
                    </Grid>
                    <Grid item lg sx={{display: {xs: "none", sm: "block"}}}>
                        <Typography sx={{fontWeight: "bold"}} variant={"body2"} noWrap={true} textAlign={"center"} component="div">{username}</Typography>
                    </Grid>
                </Grid>
            
            </Tooltip>
        </>
    )

    return (
        // @ts-ignore
        <AppBar position="static" color={"warning"}>
            <Container maxWidth="xl">
                <Toolbar disableGutters>
                <Box sx={{display: { xs: 'none', md: 'flex' }, mr: 4, cursor: "pointer"}}>
                    <Link href={"/"}><img src={"/logos/logo_dark.svg"} alt={"logo"} style={{height: "50px", width: "50px"}}/></Link>
                </Box>

                <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
                    <IconButton
                    size="large"
                    aria-label="account of current user"
                    aria-controls="menu-appbar"
                    aria-haspopup="true"
                    onClick={handleOpenNavMenu}
                    color="inherit"
                    >
                    <MenuIcon />
                    </IconButton>
                    <Menu
                    id="menu-appbar"
                    anchorEl={anchorElNav}
                    anchorOrigin={{
                        vertical: 'bottom',
                        horizontal: 'left',
                    }}
                    keepMounted
                    transformOrigin={{
                        vertical: 'top',
                        horizontal: 'left',
                    }}
                    open={Boolean(anchorElNav)}
                    onClose={handleCloseNavMenu}
                    sx={{
                        display: { xs: 'block', md: 'none' },
                    }}
                    >
                    {showPages.map((page) => (
                        <Link key={page.title} href={page.link}>
                            <MenuItem key={page.title} onClick={handleCloseNavMenu}>
                            <Typography textAlign="center" color={"black"}>{page.title}</Typography>
                            </MenuItem>
                        </Link>
                    ))}
                    </Menu>
                </Box>
                <Box sx={{display: { xs: 'flex', md: 'none' }, flexGrow: 1, mr: 1, cursor: "pointer"}}>
                    <Link href={"/"}><img src={"/logos/logo_dark.svg"} alt={"logo"} style={{height: "50px", width: "50px"}}/></Link>
                </Box>
                <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
                    {showPages.map((page) => (
                    <Link key={page.title} href={page.link}>
                        <Button
                            key={page.title}
                            onClick={handleCloseNavMenu}
                            sx={{ my: 2, display: 'block', color: "white" }}
                        >
                            {page.title}
                        </Button>
                    </Link>
                    ))}
                </Box>

                <Box sx={{ flexGrow: 0, mt: "3px", mb: "3px" }}>
                    {session.status === "authenticated" ? loggedInMenu : <Button variant="outlined" color="inherit" onClick={() => {signIn()}}>Login</Button>}
                </Box>
                </Toolbar>
            </Container>
        </AppBar>

    );
}


export default NavBar;