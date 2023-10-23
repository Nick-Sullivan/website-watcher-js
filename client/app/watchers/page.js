"use client";
import { useEffect, useState } from "react";
import { Button } from "flowbite-react";
import { getWatchers } from "@/services/watcherApi";
import WatcherNavbar from "@/components/WatcherNavbar";
import WatcherDetail from "@/components/pages/WatcherDetail";
import WatcherList from "@/components/pages/WatcherList";
import AuthGuard from "@/components/AuthGuard";

export default function Watchers() {
    const [isAuthorising, setIsAuthorising] = useState(true);
    const [selectedWatcher, setSelectedWatcher] = useState(null);
    const [isSelected, setIsSelected] = useState(false);
    const [watcherList, setWatcherList] = useState([]);

    useEffect(() => {
        if (isAuthorising) {
            return;
        }
        downloadList();
    }, [isAuthorising]);

    const selectWatcher = (index) => {
        setSelectedWatcher(watcherList[index]);
        setIsSelected(true);
    };

    const deselectWatcher = () => {
        setIsSelected(false);
        setSelectedWatcher(null);
    };

    const downloadList = async () => {
        setWatcherList([]);
        const watchers = await getWatchers();
        setWatcherList(watchers);
    };

    const createPage = () => {
        if (isSelected) {
            return (
                <WatcherDetail
                    watcher={selectedWatcher}
                    deselectWatcher={deselectWatcher}
                />
            );
        } else {
            return <WatcherList items={watcherList} onClick={selectWatcher} />;
        }
    };

    return (
        <AuthGuard onComplete={() => setIsAuthorising(false)}>
            <main className="h-screen w-screen bg-slate-100 flex flex-col">
                <WatcherNavbar></WatcherNavbar>
                <div className="flex flex-1 flex-row overflow-y-auto bg-red-100">
                    {/* <WatcherSidebar /> */}
                    {createPage()}
                </div>
            </main>
        </AuthGuard>
    );
}
