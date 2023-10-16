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
    const [selection, setSelection] = useState(null);
    const [isSelected, setIsSelected] = useState(false);
    const [listItems, setListItems] = useState([]);

    useEffect(() => {
        if (isAuthorising) {
            return;
        }
        console.log("downloading items");
        downloadList();
    }, [isAuthorising]);

    const selectItem = (index) => {
        console.log("Selecting item");
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
    };

    const createPage = () => {
        if (isSelected) {
            return (
                <WatcherDetail
                    selection={selection}
                    deselectItem={deselectItem}
                />
            );
        } else {
            return <WatcherList items={listItems} onClick={selectItem} />;
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
