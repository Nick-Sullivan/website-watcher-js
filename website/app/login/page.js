"use client";
import { useEffect, useState } from "react";
import { Button, Checkbox, Label, TextInput } from "flowbite-react";
import { authenticate, isLoggedIn } from "@/services/watcherApi";
import { useRouter } from "next/navigation";
import LoadingScreen from "@/components/LoadingScreen";
import WatcherNavbar from "@/components/WatcherNavbar";

export default function Login() {
    const router = useRouter();
    const [isCheckingRedirect, setIsCheckingRedirect] = useState(true);

    const [username, setUsername] = useState("nick.dave.sullivan+1@gmail.com");
    const [password, setPassword] = useState("password");
    const [isLoggingIn, setIsLoggingIn] = useState(false);

    useEffect(() => {
        if (isLoggedIn()) {
            console.log("Logged in, redirecting");
            router.push("/watchers");
        } else {
            setIsCheckingRedirect(false);
        }
    }, []);

    const submitLogin = async () => {
        setIsLoggingIn(true);
        const success = await authenticate(username, password);
        if (success) {
            router.push("/watchers");
        }
        setIsLoggingIn(false);
    };

    const changeUsername = (e) => {
        setUsername(e.target.value);
    };

    const changePassword = (e) => {
        setPassword(e.target.value);
    };

    if (isCheckingRedirect) {
        return <LoadingScreen />;
    }

    return (
        <main className="h-screen w-screen bg-slate-100">
            <div className="h-full w-full flex flex-col">
                <WatcherNavbar></WatcherNavbar>

                <form className="flex max-w-md flex-col gap-4">
                    <div>
                        <div className="mb-2 block">
                            <Label htmlFor="email1" value="Your email" />
                        </div>
                        <TextInput
                            defaultValue={username}
                            disabled={isLoggingIn}
                            id="email1"
                            onChange={changeUsername}
                            placeholder="name@flowbite.com"
                            required
                            type="email"
                        />
                    </div>
                    <div>
                        <div className="mb-2 block">
                            <Label htmlFor="password1" value="Your password" />
                        </div>
                        <TextInput
                            defaultValue={password}
                            disabled={isLoggingIn}
                            id="password1"
                            onChange={changePassword}
                            required
                            type="password"
                        />
                    </div>
                    <div className="flex items-center gap-2">
                        <Checkbox id="remember" />
                        <Label htmlFor="remember">Remember me</Label>
                    </div>
                    <Button
                        disabled={isLoggingIn}
                        type="button"
                        onClick={submitLogin}
                    >
                        Submit
                    </Button>
                </form>
            </div>
        </main>
    );
}
