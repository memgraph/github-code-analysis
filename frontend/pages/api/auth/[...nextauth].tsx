import { Session, User, Awaitable } from 'next-auth/core/types'; 
import { JWT } from 'next-auth/jwt';
import NextAuth from "next-auth";
import GithubProvider from "next-auth/providers/github";
import axios from 'axios';


async function refreshAccessToken(token: JWT): Promise<JWT> {
    try {
        const url =
            "https://github.com/login/oauth/access_token?" +
            new URLSearchParams({
                client_id: process.env.GITHUB_CLIENT_ID as string,
                client_secret: process.env.GITHUB_CLIENT_SECRET as string,
                grant_type: "refresh_token",
                refresh_token: token.refresh_token as string,
            })
        
        const response = await axios.post(url);
  
      if (response.data && response.data.includes("error")) {
        throw response.data
      }

      const refresh_data: { [key: string]: string } = {}

      response.data.split("&").forEach((element: string) => {
        const [key, value] = element.split("=");
        refresh_data[key] = value;
      })
  
      return {
        ...token,
        access_token: refresh_data.access_token,
        access_token_expires: Date.now() + parseInt(refresh_data.expires_in) * 1000 as Number,
        refresh_token: refresh_data.refresh_token ?? token.refreshToken,
      }
    } catch (error) {
      console.log("error", error)
  
      return {
        ...token,
        error: "RefreshAccessTokenError",
      }
    }
  }


export default NextAuth({
    secret: process.env.AUTH_SECRET,
    providers: [
        GithubProvider({
            clientId: process.env.GITHUB_CLIENT_ID as string,
            clientSecret: process.env.GITHUB_CLIENT_SECRET as string,
            authorization: { params: { scope: 'repo read:org read:packages read:project read:repo_hook read:user' } },
        })
    ],
    session: { strategy: "jwt" },
    callbacks: {
        jwt: ({ token, user, account, profile, isNewUser }): Awaitable<JWT> => {
            if (account && user && profile) {
                return {
                  access_token: account.access_token as string,
                  access_token_expires: (account.expires_at ?? ((Date.now() + 8 * 3600 * 1000)/1000) * 1000) as Number,
                  refresh_token: account.refresh_token as string,
                  login: profile.login as string,
                  avatar_url: profile.avatar_url as string,
                }
            }
            
            if (token.access_token_expires) {
                if (Date.now() < (token.access_token_expires as Number)) {
                    return token
                }
            }
        
            return refreshAccessToken(token)
        },
        session: (params: {session: Session, user: User, token: JWT}): Awaitable<Session> => {
            const session = params.session;
            
            if (session && params.token && params.token.access_token) {
                session.login = params.token.login;
                session.access_token = params.token.access_token;
                session.avatar_url = params.token.avatar_url;
            }
            return session;
        }
      },
});
