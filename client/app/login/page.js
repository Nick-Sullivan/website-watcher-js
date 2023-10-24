"use client";
import { useEffect, useState } from "react";
import { Button, Checkbox, Label, TextInput } from "flowbite-react";
import { toast, Toaster } from "sonner";
import { useRouter } from "next/navigation";
import { authenticate } from "@/services/auth";
import WatcherNavbar from "@/components/WatcherNavbar";

export default function Login() {
    const router = useRouter();
    const [username, setUsername] = useState("nick.dave.sullivan@gmail.com");
    const [password, setPassword] = useState("password");
    const [isLoggingIn, setIsLoggingIn] = useState(true);

    useEffect(() => {
        // Only enable the button after hydration, otherwise browser tests can click them too fast
        setIsLoggingIn(false);
    }, []);

    const submitLogin = async () => {
        setIsLoggingIn(true);
        const errorMessage = await authenticate(username, password);
        if (errorMessage == "") {
            router.push("/watchers");
        } else {
            toast.error(errorMessage);
        }

        setIsLoggingIn(false);
    };

    const changeUsername = (e) => {
        setUsername(e.target.value);
    };

    const changePassword = (e) => {
        setPassword(e.target.value);
    };

    return (
        <main className="h-screen w-screen bg-slate-100">
            <div className="h-full w-full flex flex-col">
                <Toaster richColors position="top-center" />
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
                        isProcessing={isLoggingIn}
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
