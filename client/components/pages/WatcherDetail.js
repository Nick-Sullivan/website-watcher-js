import { useEffect, useState } from "react";
import { Button, Card, ListGroup } from "flowbite-react";
import { Scrape } from "@/models/Scrape";
import { Spinner } from "flowbite-react";
import Image from "next/image";
import {
    HiOutlineArrowLeft,
    HiOutlineZoomIn,
    HiOutlineZoomOut,
} from "react-icons/hi";
import ScrapeListItem from "@/components/ScrapeListItem";
import { getScrapes, getScreenshot } from "@/services/scrapeApi";

const WatcherDetail = ({ watcher, deselectWatcher }) => {
    const [isImageLoading, setIsImageLoading] = useState(false);
    const [isListDownloading, setIsListDownloading] = useState(true);
    const [selectedScrapeId, setSelectedScrapeId] = useState(null);
    const [image, setImage] = useState("");
    // const [image, setImage] = useState("/images/profile.jpg");
    const [scrapeList, setScrapeList] = useState([]);

    useEffect(() => {
        console.log("downloading screenshots");
        downloadScrapes();
    }, []);

    const downloadScrapes = async () => {
        setIsListDownloading(true);
        setScrapeList([]);
        const scrapeResult = await getScrapes(watcher.id);
        setScrapeList(scrapeResult);
        setIsListDownloading(false);
    };

    const loadImage = async (index) => {
        setIsImageLoading(true);
        setImage("");
        setSelectedScrapeId(scrapeList[index].id);
        const screenshotUrl = await getScreenshot(
            watcher.id,
            scrapeList[index].id
        );
        setImage(screenshotUrl);
        setIsImageLoading(false);
    };

    const ScrapeListView = () => {
        if (isListDownloading) {
            return (
                <div className="flex flex-1 justify-center items-center">
                    <Spinner size="xl" />
                </div>
            );
        }

        return (
            <div className="flex-col overflow-y-auto">
                <ListGroup>
                    {scrapeList.map((item, index) => (
                        <ScrapeListItem
                            key={index}
                            heading={item.getDate()}
                            subheading={item.getTime()}
                            isSelected={selectedScrapeId == item.id}
                            onClick={() => loadImage(index)}
                        />
                    ))}
                </ListGroup>
            </div>
        );
    };

    const ImageView = () => {
        const height = 1440;
        const width = 1440;
        if (isImageLoading) {
            return <Spinner size="xl" />;
        }
        if (image == "") {
            return <div></div>;
        }
        return (
            <div
                className="flex flex-col h-full"
                style={{ position: "relative" }}
            >
                {/* <div className="flex flex-row">
                    <Button color="gray">
                        <HiOutlineZoomIn className="h-6 w-6"></HiOutlineZoomIn>
                    </Button>
                    <Button color="gray">
                        <HiOutlineZoomOut className="h-6 w-6"></HiOutlineZoomOut>
                    </Button>
                </div> */}
                <div className="overflow-auto">
                    <Image
                        // className="w-full"
                        priority
                        src={image}
                        width={height}
                        height={width}
                        // fill={true}
                        // sizes="100vw"
                        // style={{ object-fit: "contain" }}
                        style={{ objectFit: "contain" }}
                        // style={{ width: "100%", height: "auto" }} // optional
                        alt=""
                    />
                </div>
            </div>
        );
    };

    return (
        <div className="flex w-full">
            <div className="flex w-1/3 flex-col">
                <Card className="bg-white">
                    <div className="flex flex-row">
                        <Button
                            onClick={deselectWatcher}
                            color="gray"
                            className="w-10"
                        >
                            <HiOutlineArrowLeft></HiOutlineArrowLeft>
                        </Button>
                        <div className="flex-col px-5">
                            <h5 className="flex justify-center font-bold text-gray-900">
                                {watcher.name}
                            </h5>
                            <p className="flex justify-center text-gray-700">
                                {watcher.url}
                            </p>
                        </div>
                    </div>
                </Card>
                <ScrapeListView></ScrapeListView>
            </div>

            <div className="flex flex-1 overflow-auto justify-center items-center">
                <ImageView />
            </div>
        </div>
    );
};
export default WatcherDetail;
