import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { isLoggedIn } from "@/services/auth";
import LoadingScreen from "./LoadingScreen";

const AuthGuard = ({ onComplete, children }) => {
    const router = useRouter();
    const [isCheckingRedirect, setIsCheckingRedirect] = useState(true);

    useEffect(() => {
        if (!isLoggedIn()) {
            router.push("/login");
        } else {
            onComplete();
            setIsCheckingRedirect(false);
        }
    }, []);

    if (isCheckingRedirect) {
        return <LoadingScreen />;
    }

    return <>{children}</>;
};

export default AuthGuard;
