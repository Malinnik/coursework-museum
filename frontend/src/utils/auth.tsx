import { redirect } from "next/navigation";
import { getAuth, setAuth } from "./cookie";

type User = {
	username: string;
	password: string;
    fullname: string;
}


export async function register(user: User)  {
    const result = await fetch('/api/v1/users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(user),
    })

    return result.json()
}

export async function login(user: User) {
    const result = await fetch('/api/v1/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(user),
    })

    if (result.ok) {
        // Set token to Cookie
        result.json().then(data => {
           setAuth(data.user_token)
        })
    }
    else {
        return result.json()
    }

    return await getAuth()
}



export async function checkAuth() {

    let token = await getAuth();
    console.log(token)

    const result = await fetch('/api/v1/check',{
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': String(token)
        },
    });

    console.log(result)

    if (result.ok){
        console.log('ok')
        return true;
    }
    
    console.log('redirect')
    return false;
}

