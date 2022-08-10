import { NextPage } from "next";
import { useRouter } from "next/router";
import { signIn, useSession } from "next-auth/react";
import { useEffect } from "react";


const Repo : NextPage = () => {
    const router = useRouter()
    const session = useSession()

    useEffect(() => {
        if (session.status === "unauthenticated") {
            signIn();
        }
    }, [session])

    return (
        <div>
            <h1>{router.query.username} / {router.query.repo}</h1>
        </div>
    )
}

export default Repo;