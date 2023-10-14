import { ListGroup } from "flowbite-react";
import ScrapeListItem from "@/components/ScrapeListItem";

const ScrapeListGroup = ({ items, selectedId, onClick }) => {
    return (
        <div className="flex-1 p-2">
            <ListGroup>
                {items.map((item, index) => (
                    <ScrapeListItem
                        index={index}
                        heading={item.name}
                        subheading={""}
                        isSelected={selectedId == item.id}
                        onClick={() => onClick(index)}
                    />
                ))}
            </ListGroup>
        </div>
    );
};

export default ScrapeListGroup;
