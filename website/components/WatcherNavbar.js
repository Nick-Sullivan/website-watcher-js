import { Navbar } from "flowbite-react";
import Image from "next/image";

const WatcherNavbar = ({}) => {
    return (
        <Navbar fluid rounded>
            <Navbar.Brand href="https://100percentofthetimehotspaghetti.com">
                <Image
                    alt="Flowbite logo"
                    height={32}
                    src="https://flowbite.com/docs/images/logo.svg"
                    width={32}
                    style={{ width: 32, height: 32 }}
                />
                <span className="self-center whitespace-nowrap pl-3 text-xl font-semibold dark:text-white">
                    Website Watcher
                </span>
            </Navbar.Brand>
        </Navbar>
    );
};

export default WatcherNavbar;
