"use client";
import { useEffect, useState } from "react";
import { Button, Modal, Spinner } from "flowbite-react";
import { getWatchers } from "@/services/watcherApi";
import WatcherNavbar from "@/components/WatcherNavbar";
import WatcherDetail from "@/components/pages/WatcherDetail";
import WatcherList from "@/components/pages/WatcherList";
import WatcherCreationModal from "@/components/pages/WatcherCreationModal";
import AuthGuard from "@/components/AuthGuard";

export default function WatcherPage() {
    const [isAuthorising, setIsAuthorising] = useState(true);
    const [isListDownloading, setIsListDownloading] = useState(true);
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

    const deselectWatcher = async (reload) => {
        setIsSelected(false);
        setSelectedWatcher(null);
        if (reload) {
            await downloadList();
        }
    };

    const downloadList = async () => {
        setIsListDownloading(true);
        setWatcherList([]);
        // await new Promise((r) => setTimeout(r, 2000));
        const watchers = await getWatchers();
        setWatcherList(watchers);
        setIsListDownloading(false);
    };

    const onWatcherCreated = async () => {
        await downloadList();
    };

    const createPage = () => {
        if (isSelected) {
            return (
                <WatcherDetail
                    watcher={selectedWatcher}
                    deselectWatcher={deselectWatcher}
                />
            );
        }
        if (isListDownloading) {
            return (
                <div className="flex flex-1 justify-center items-center">
                    <Spinner size="xl" />
                </div>
            );
        }
        return (
            <>
                <WatcherCreationModal
                    onCreate={onWatcherCreated}
                ></WatcherCreationModal>
                <WatcherList items={watcherList} onClick={selectWatcher} />
            </>
        );
    };

    return (
        <AuthGuard onComplete={() => setIsAuthorising(false)}>
            <main className="h-screen w-screen bg-slate-100 flex flex-col">
                <WatcherNavbar></WatcherNavbar>
                <div className="flex flex-1 flex-row overflow-y-auto bg-slate-100">
                    {/* <WatcherSidebar /> */}
                    {createPage()}
                </div>
            </main>
        </AuthGuard>
    );
}
