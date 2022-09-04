import '../styles/globals.css'
import type { AppProps } from 'next/app'
import { SessionProvider } from "next-auth/react"
import NavBar from '../comps/NavBar';
import { createTheme, ThemeProvider } from "@mui/material/styles";

const theme = createTheme({
    palette: {
        primary: {
            main: "#8671E1",
            light: "#8671E150",
            contrastText: "#fff"
        },
        secondary: {
            main: "#76A7F4",
            contrastText: "#fff"
        },
        info : {
            main: "#6B8CE6",
            contrastText: "#fff"
        },
        warning : {
            main: "#BCB6F6",
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
