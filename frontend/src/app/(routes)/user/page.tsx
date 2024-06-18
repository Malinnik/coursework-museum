'use client';
import { checkAuth } from "@/utils/auth";
import { useRouter } from "next/navigation";
import React, { useEffect, useState } from "react";

const AuthPage = () => {
	
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        // Выполнить fetch или другую функцию при загрузке страницы
        if (isAuthenticated) return;
        
        let result= checkAuth();
        if (!result) {
            const { push } = useRouter();
            push('/login');
        }
        setIsAuthenticated(true);

        // Убедитесь, что вы не вызываете fetch при каждом рендере, добавив зависимость
        // от isAuthenticated, чтобы useEffect выполнялся только при изменении isAuthenticated
    }), [];
	
	
	
	return (
		<div className="h-full w-full bg-slate-100">
            User Page
			
		</div>
	);
}

export default AuthPage;