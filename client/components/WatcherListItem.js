import { Card } from "flowbite-react";
import { ListGroup } from "flowbite-react";

const WatcherListItem = ({ item, onClick, isHover = true }) => {
    return (
        // <ListGroup.Item>{item.name}</ListGroup.Item>
        <Card href={isHover ? "#" : null} onClick={onClick} key={item.id}>
            <h5 className="font-bold text-gray-900">{item.name}</h5>
            <p className="font-normal text-gray-700">{item.url}</p>
        </Card>
    );
};

export default WatcherListItem;
