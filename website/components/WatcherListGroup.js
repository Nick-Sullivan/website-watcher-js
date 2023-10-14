import { ListGroup } from "flowbite-react";
import WatcherListItem from "@/components/WatcherListItem";

const WatcherListGroup = ({ items, onClick }) => {
    return (
        <div className="flex-1 p-2">
            <ListGroup>
                {items.map((item, index) => (
                    <WatcherListItem
                        item={item}
                        onClick={() => onClick(index)}
                    />
                ))}
            </ListGroup>
        </div>
    );
};

export default WatcherListGroup;
