'use server';
import { cookies } from "next/headers";


export async function setAuth(token: string) {
    cookies().set('user_token', token);
}

export async function getAuth(token: string = 'user_token') {
    return cookies().get(token);
}