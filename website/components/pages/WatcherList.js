import { ListGroup } from "flowbite-react";
import WatcherListItem from "@/components/WatcherListItem";

const WatcherList = ({ items, onClick }) => {
    return (
        <>
            <div className="w-1/3 overflow-y-auto">
                <ListGroup>
                    {items.map((item, index) => (
                        <WatcherListItem
                            key={index}
                            item={item}
                            onClick={() => onClick(index)}
                        />
                    ))}
                </ListGroup>
            </div>
        </>
    );
};
export default WatcherList;
