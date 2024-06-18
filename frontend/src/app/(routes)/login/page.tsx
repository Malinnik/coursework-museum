'use client';
import { login, register } from "@/utils/auth";
import React from "react";

const AuthPage = () => {
	
	const [username, setUsername] = React.useState("");
	const [password, setPassword] = React.useState("");
	const [result, setResult] = React.useState("");

	async function createUser() {
		setResult( await register({username, password}));
	}

	async function log_in_system() {
		setResult(await login({username, password}))
		
	}


	
	
	return (
		<div className="h-full w-full bg-slate-100">
			<h1>Test Page</h1>
			<a href="/" className="text-3xl text-cyan-600 font-bold underline hover:text-blue-600">Text</a>
			<div className=" rounded-md bg-slate-400 border-black border-2 p-2 pl-10 pr-10">
				<p className="mt-5">username: <input type="text" onChange={e => setUsername(e.target.value)}/></p>
				<p className="mt-5">password: <input type="password" onChange={e => setPassword(e.target.value)}/></p>
				
				<button onClick={createUser} className="mt-7 rounded-lg border-4 border-blue-500 bg-blue-500 p-4 hover:border-blue-700 hover:bg-blue-700 hover:text-white active:bg-blue-900 active:border-white">Sign Up</button>
        		<button onClick={log_in_system} className="mt-7 rounded-lg border-4 border-blue-500 bg-blue-500 p-4 hover:border-blue-700 hover:bg-blue-700 hover:text-white active:bg-blue-900 active:border-white">Login</button>
			</div>
			<pre>{JSON.stringify(result, null, 2)}</pre>
		</div>
	);
}

export default AuthPage;