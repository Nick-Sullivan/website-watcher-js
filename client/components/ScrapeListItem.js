import { Card } from "flowbite-react";

const ScrapeListItem = ({ heading, subheading, isSelected, onClick }) => {
    const cardClass = isSelected ? "bg-slate-200" : "";
    const headingClass = isSelected ? "font-bold" : "";

    return (
        <Card className={cardClass} href="#" onClick={onClick}>
            <h5 className={`text-gray-900 ${headingClass}`}>{heading}</h5>
            {/* <p className="font-normal text-xs text-gray-700">{subheading}</p> */}
        </Card>
    );
};

export default ScrapeListItem;
