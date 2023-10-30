import { useEffect, useState } from "react";
import { Button, Label, Modal, TextInput } from "flowbite-react";
import { HiPlus } from "react-icons/hi";
import { createWatcher } from "@/services/watcherApi";

const WatcherCreationModal = ({ onCreate }) => {
    const [watcherName, setWatcherName] = useState("");
    const [watcherUrl, setWatcherUrl] = useState("");
    const [isCreatingWatcher, setIsCreatingWatcher] = useState(true);

    const [openModal, setOpenModal] = useState();
    const props = { openModal, setOpenModal };

    useEffect(() => {
        // Only enable the button after hydration, otherwise browser tests can click them too fast
        setIsCreatingWatcher(false);
    }, []);

    const submitNewWatcher = async () => {
        setIsCreatingWatcher(true);
        await createWatcher(watcherName, watcherUrl);
        // const errorMessage = await authenticate(username, password);
        // if (errorMessage == "") {
        //     router.push("/watchers");
        // } else {
        //     toast.error(errorMessage);
        // }
        // await new Promise((resolve) => setTimeout(resolve, 1000));

        setIsCreatingWatcher(false);
        props.setOpenModal(undefined);
        onCreate();
    };

    const changeWatcherName = (e) => {
        setWatcherName(e.target.value);
    };

    const changeWatcherUrl = (e) => {
        setWatcherUrl(e.target.value);
    };

    return (
        <>
            <Button
                className="absolute bottom-10 left-10 w-20 h-20"
                onClick={() => props.setOpenModal("dismissible")}
                data-testid="new-watcher"
            >
                <HiPlus></HiPlus>
            </Button>

            <Modal
                dismissible
                show={props.openModal === "dismissible"}
                onClose={() => props.setOpenModal(undefined)}
            >
                <Modal.Header>New Watcher</Modal.Header>
                <Modal.Body>
                    <div className="space-y-6">
                        <div>
                            <div className="mb-2 block">
                                <Label htmlFor="watcherName1" value="Name" />
                            </div>
                            <TextInput
                                defaultValue={watcherName}
                                disabled={isCreatingWatcher}
                                id="watcherName1"
                                onChange={changeWatcherName}
                                placeholder="My New Watcher"
                                required
                                // type="email"
                            />
                        </div>

                        <div>
                            <div className="mb-2 block">
                                <Label htmlFor="watcherUrl1" value="URL" />
                            </div>
                            <TextInput
                                defaultValue={watcherUrl}
                                disabled={isCreatingWatcher}
                                id="watcherUrl1"
                                onChange={changeWatcherUrl}
                                placeholder="https://google.com"
                                required
                                // type="password"
                            />
                        </div>
                    </div>
                </Modal.Body>
                <Modal.Footer>
                    <Button
                        disabled={isCreatingWatcher}
                        isProcessing={isCreatingWatcher}
                        onClick={submitNewWatcher}
                    >
                        Create
                    </Button>
                    <Button
                        color="gray"
                        disabled={isCreatingWatcher}
                        onClick={() => props.setOpenModal(undefined)}
                    >
                        Cancel
                    </Button>
                </Modal.Footer>
            </Modal>
        </>
    );
};
export default WatcherCreationModal;
