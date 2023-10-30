import { useEffect, useState } from "react";
import { Button, Card, Dropdown, ListGroup } from "flowbite-react";
import { Scrape } from "@/models/Scrape";
import { Modal, Spinner } from "flowbite-react";
import Image from "next/image";
import {
    HiOutlineArrowLeft,
    HiExclamation,
    HiDotsHorizontal,
} from "react-icons/hi";
import ScrapeListItem from "@/components/ScrapeListItem";
import { getScrapes, getScreenshot } from "@/services/scrapeApi";
import { deleteWatcher } from "@/services/watcherApi";

const WatcherDetail = ({ watcher, deselectWatcher }) => {
    const [isImageLoading, setIsImageLoading] = useState(false);
    const [isListDownloading, setIsListDownloading] = useState(true);
    const [selectedScrapeId, setSelectedScrapeId] = useState(null);
    const [image, setImage] = useState("");
    // const [image, setImage] = useState("/images/profile.jpg");
    const [scrapeList, setScrapeList] = useState([]);
    const [openModal, setOpenModal] = useState();
    const props = { openModal, setOpenModal };

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
        setSelectedScrapeId(scrapeList[index].id);
        if (scrapeList[index].image === null) {
            setIsImageLoading(true);
            setImage("");
            const screenshotUrl = await getScreenshot(
                watcher.id,
                scrapeList[index].id
            );
            scrapeList[index].image = screenshotUrl;
        }
        setImage(scrapeList[index].image);
        setIsImageLoading(false);
    };

    const deleteWatcherReq = async () => {
        console.log("Deleting watcher");
        console.log(watcher);
        await deleteWatcher(watcher.id);
        await deselectWatcher(true);
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
        const height = 700;
        const width = 700;
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
                <Card className="bg-white overflow-y-auto">
                    <div className="flex flex-row">
                        <Button
                            onClick={() => deselectWatcher(false)}
                            color="gray"
                            className="w-10 flex-none"
                        >
                            <HiOutlineArrowLeft></HiOutlineArrowLeft>
                        </Button>
                        <div className="flex flex-col flex-1 px-5">
                            <h5
                                className="flex justify-center font-bold text-gray-900"
                                data-testid="name"
                            >
                                {watcher.name}
                            </h5>
                            <p
                                className="flex justify-center text-xs text-gray-700"
                                data-testid="url"
                            >
                                {watcher.url}
                            </p>
                        </div>
                        <div className="flex flex-none justify-end">
                            <Dropdown
                                placement="right"
                                renderTrigger={() => (
                                    <span>
                                        <HiDotsHorizontal />
                                    </span>
                                )}
                            >
                                <Dropdown.Item>Edit</Dropdown.Item>
                                <Dropdown.Item
                                    className="text-red-500"
                                    onClick={() =>
                                        props.setOpenModal("dismissible")
                                    }
                                >
                                    Delete
                                </Dropdown.Item>
                            </Dropdown>
                        </div>
                    </div>

                    <Modal
                        dismissible
                        show={props.openModal === "dismissible"}
                        onClose={() => props.setOpenModal(undefined)}
                    >
                        <Modal.Header>
                            <div className="flex flex-row items-center text-red-500">
                                <HiExclamation />
                                Warning
                            </div>
                        </Modal.Header>
                        <Modal.Body>
                            <div className="space-y-6">
                                <p className="text-base leading-relaxed text-gray-500 dark:text-gray-400">
                                    Deleting a watcher will delete all
                                    snapshots. This cannot be undone.
                                </p>
                            </div>
                        </Modal.Body>
                        <Modal.Footer>
                            <Button
                                color="warning"
                                // disabled={isCreatingWatcher}
                                // isProcessing={isCreatingWatcher}
                                onClick={deleteWatcherReq}
                            >
                                Delete
                            </Button>
                            <Button
                                color="gray"
                                // disabled={isCreatingWatcher}
                                onClick={() => props.setOpenModal(undefined)}
                            >
                                Cancel
                            </Button>
                        </Modal.Footer>
                    </Modal>
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
