import { Card } from "flowbite-react";

const WatcherListItem = ({ item, onClick, isHover = true }) => {
    return (
        <Card href={isHover ? "#" : null} onClick={onClick} key={item.id}>
            <h5 className="font-bold text-gray-900">{item.name}</h5>
            <p className="font-normal text-gray-700">{item.url}</p>
        </Card>
    );
};

export default WatcherListItem;
