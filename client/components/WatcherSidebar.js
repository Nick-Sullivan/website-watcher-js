import { Sidebar } from "flowbite-react";
import { HiCog, HiEye, HiHome } from "react-icons/hi";

const WatcherSidebar = ({}) => {
    return (
        <div className="flex-none">
            <Sidebar>
                <Sidebar.Items>
                    <Sidebar.ItemGroup>
                        <Sidebar.Item href="#" icon={HiHome}>
                            Home
                        </Sidebar.Item>
                        <Sidebar.Item href="#" icon={HiEye}>
                            Watchers
                        </Sidebar.Item>
                        <Sidebar.Item href="#" icon={HiCog}>
                            Settings
                        </Sidebar.Item>
                    </Sidebar.ItemGroup>
                </Sidebar.Items>
            </Sidebar>
        </div>
    );
};

export default WatcherSidebar;
