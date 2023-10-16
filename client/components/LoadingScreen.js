import { Spinner } from "flowbite-react";

const LoadingScreen = () => {
    return (
        <div className="h-screen w-screen flex justify-center items-center">
            <Spinner size="xl" />
        </div>
    );
};

export default LoadingScreen;
