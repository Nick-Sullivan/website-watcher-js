import { useState } from "react";
import { Button, Card, ListGroup } from "flowbite-react";
import { Scrape } from "@/models/Scrape";
import { Spinner } from "flowbite-react";
import Image from "next/image";
import { HiOutlineArrowLeft } from "react-icons/hi";
import ScrapeListItem from "@/components/ScrapeListItem";

const WatcherDetail = ({ selection, deselectItem }) => {
    const [isImageLoading, setIsImageLoading] = useState(false);
    const [selectedId, setSelectedId] = useState(null);
    const [image, setImage] = useState("/images/profile.jpg");
    const [scrapes, setScrapes] = useState([
        new Scrape("a", "2023-10-13"),
        new Scrape("b", "2023-10-12"),
        new Scrape("c", "2023-10-11"),
        new Scrape("d", "2023-10-10"),
        new Scrape("e", "2023-10-10"),
        new Scrape("f", "2023-10-10"),
        new Scrape("g", "2023-10-10"),
        new Scrape("h", "2023-10-10"),
        new Scrape("i", "2023-10-10"),
        new Scrape("j", "2023-10-10"),
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
            return <Spinner size="xl" />;
        } else {
            return (
                <Image
                    priority
                    src={image}
                    height={height}
                    width={width}
                    // style={{ width: "100%", height: "auto" }}
                    alt=""
                />
            );
        }
    };

    return (
        <div className="flex w-full">
            <div className="flex w-1/3 flex-col">
                <Card className="bg-gray-200">
                    <div className="flex flex-row">
                        <Button
                            onClick={deselectItem}
                            color="gray"
                            className="w-10"
                        >
                            <HiOutlineArrowLeft></HiOutlineArrowLeft>
                        </Button>
                        <div className="flex-col px-5">
                            <h5 className="flex justify-center font-bold text-gray-900">
                                {selection.name}
                            </h5>
                            <p className="flex justify-center text-gray-700">
                                {selection.url}
                            </p>
                        </div>
                    </div>
                </Card>
                <div className="flex-col overflow-y-auto">
                    <ListGroup>
                        {scrapes.map((item, index) => (
                            <ScrapeListItem
                                key={index}
                                heading={item.name}
                                subheading={""}
                                isSelected={selectedId == item.id}
                                onClick={() => loadImage(index)}
                            />
                        ))}
                    </ListGroup>
                </div>
            </div>

            <div className="flex flex-1 overflow-auto justify-center items-center">
                <ImageView />
            </div>
        </div>
    );
};
export default WatcherDetail;
