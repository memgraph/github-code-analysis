import '../styles/globals.css'
import type { AppProps } from 'next/app'
import { SessionProvider } from "next-auth/react"
import NavBar from '../comps/NavBar';
import { createTheme, ThemeProvider } from "@mui/material/styles";

const theme = createTheme({
    palette: {
        primary: {
            main: "#FB6E00",
            contrastText: "#fff"
        },
        secondary: {
            main: "#8C0082",
            contrastText: "#000"
        },
        info : {
            main: "#E5E5E5",
            contrastText: "#000"
        },
        warning : {
            main: "#211D1F",
            contrastText: "#fff"
        }
    }
})

function MyApp({ Component, pageProps: {session, ...pageProps} }: AppProps) {
  return (
      <ThemeProvider theme={theme}>
          <div className={"pattern"}></div>
            <SessionProvider session={session}>
                <NavBar />
                <Component {...pageProps} />
            </SessionProvider>
      </ThemeProvider>
    
  );
}

export default MyApp
