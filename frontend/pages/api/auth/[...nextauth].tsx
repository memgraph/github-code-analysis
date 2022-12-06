import { Session, User, Awaitable } from 'next-auth/core/types'; 
import { JWT } from 'next-auth/jwt';
import NextAuth from "next-auth";
import GithubProvider from "next-auth/providers/github";
import axios from 'axios';
import FormData from 'form-data';


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
          refresh_token: refresh_data.refresh_token ?? token.refresh_token,
        }
    } catch (error) {
      console.log("error")
  
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
        jwt: async ({ token, user, account, profile, isNewUser }): Promise<JWT> => {
            if (account && profile) {
                return {
                  access_token: account.access_token as string,
                  access_token_expires: (account.expires_at ?? ((Date.now() + 8 * 3600 * 1000)/1000) * 1000) as Number,
                  refresh_token: account.refresh_token as string,
                  login: profile.login as string,
                  avatar_url: profile.avatar_url as string,
                }
            }
            
            if (token.access_token_expires) {
                if (Date.now() / 1000 < (token.access_token_expires as Number)) {
                    return token
                }
            }
        
            return refreshAccessToken(token)
        },
        session: async (params: {session: Session, user: User, token: JWT}): Promise<Session> => {
            const session = params.session;
            
            if (session && params.token && params.token.access_token) {
                session.login = params.token.login;
                session.access_token = params.token.access_token;
                session.avatar_url = params.token.avatar_url;
            }
            return session;
        },
        signIn: async ({ user, account, profile, email, credentials }): Promise<boolean> => {
            try {

              var bodyFormData = new FormData();
              bodyFormData.append("access_token", account.access_token);
              bodyFormData.append('login', profile.login as string);
              bodyFormData.append('secret_key', process.env.SECRET_REGISTRATION_KEY as string);

              const result = await axios({
                  method: "POST",
                  url: process.env.NEXTAUTH_BACKEND_URL + "/user/register",
                  data: bodyFormData,
                  headers: {"Content-Type": "mutlipart/form-data"}
              })
              
              if (result.data.login) {
                return true
              }

            } catch (error) {
              console.log("error")
            }
            
            return false;
        }
      },

});
