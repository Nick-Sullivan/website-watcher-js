"use client";
import { useEffect, useState } from "react";
import WatcherNavbar from "@/components/WatcherNavbar";
import WatcherListGroup from "@/components/WatcherListGroup";
import WatcherView from "@/components/WatcherView";
import { Button } from "flowbite-react";
import { getWatchers, isLoggedIn } from "@/services/watcherApi";
import { useRouter } from "next/navigation";
import LoadingScreen from "@/components/LoadingScreen";

export default function Watchers() {
    const router = useRouter();
    const [isCheckingRedirect, setIsCheckingRedirect] = useState(true);
    const [selection, setSelection] = useState(null);
    const [isSelected, setIsSelected] = useState(false);
    const [listItems, setListItems] = useState([]);

    useEffect(() => {
        if (!isLoggedIn()) {
            console.log("Not logged in, redirecting");
            router.push("/login");
        } else {
            console.log("Logged in");
            setIsCheckingRedirect(false);
        }
    }, []);

    const selectItem = (index) => {
        setSelection(listItems[index]);
        setIsSelected(true);
    };

    const deselectItem = () => {
        setIsSelected(false);
        setSelection(null);
    };

    const downloadList = async () => {
        setListItems([]);
        const watchers = await getWatchers();
        setListItems(watchers);
        // setListItems([
        //     new Watcher("a", "the first", "https://google.com"),
        //     new Watcher("b", "the second", "https://tictoc.com.au"),
        //     new Watcher("c", "the third", "https://unloan.com"),
        //     new Watcher("d", "the fourth", "https://youtube.com"),
        // ]);
    };

    const createBody = () => {
        if (isSelected) {
            return (
                <WatcherView
                    selection={selection}
                    deselectItem={deselectItem}
                />
            );
        } else {
            return <WatcherListGroup items={listItems} onClick={selectItem} />;
        }
    };

    if (isCheckingRedirect) {
        return <LoadingScreen />;
    }

    return (
        <main className="h-screen w-screen bg-slate-100">
            <div className="h-full w-full flex flex-col">
                <WatcherNavbar></WatcherNavbar>
                <div className="h-full flex flex-row">
                    {/* <WatcherSidebar /> */}
                    <Button onClick={downloadList}>Download</Button>
                    <div className="w-full flex flex-col">{createBody()}</div>
                </div>
            </div>
        </main>
    );
}
