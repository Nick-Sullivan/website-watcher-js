import { useState } from "react";
import { Button } from "flowbite-react";
import { Scrape } from "@/models/Scrape";
import { Spinner } from "flowbite-react";
import Image from "next/image";
import ScrapeListGroup from "@/components/ScrapeListGroup";
import WatcherListItem from "@/components/WatcherListItem";

const WatcherView = ({ selection, deselectItem }) => {
    const [isImageLoading, setIsImageLoading] = useState(false);
    const [selectedId, setSelectedId] = useState(null);
    const [image, setImage] = useState("/images/profile.jpg");
    const [scrapes, setScrapes] = useState([
        new Scrape("a", "2023-10-13"),
        new Scrape("b", "2023-10-12"),
        new Scrape("c", "2023-10-11"),
        new Scrape("d", "2023-10-10"),
    ]);

    const loadImage = async (index) => {
        setIsImageLoading(true);
        setImage("");
        setSelectedId(scrapes[index].id);
        await new Promise((r) => setTimeout(r, 2000));
        setImage("/images/profile.jpg");
        setIsImageLoading(false);
    };

    const ImageView = () => {
        const height = 1440;
        const width = 1440;
        if (isImageLoading) {
            return (
                <div className="h-full flex justify-center items-center">
                    <Spinner size="xl" />
                </div>
            );
        } else {
            return (
                <div className="object-center">
                    <Image
                        priority
                        src={image}
                        height={height}
                        width={width}
                        style={{ width: "100%", height: "auto" }}
                        alt=""
                    />
                </div>
            );
        }
    };

    return (
        <>
            <Button onClick={deselectItem}>Back</Button>
            <WatcherListItem item={selection} onClick={null} isHover={false} />
            <div className="h-full flex flex-row">
                <dev className="w-full">
                    <ScrapeListGroup
                        items={scrapes}
                        selectedId={selectedId}
                        onClick={loadImage}
                    />
                </dev>
                <dev className="w-full">
                    <ImageView />
                </dev>
            </div>
        </>
    );
};
export default WatcherView;
