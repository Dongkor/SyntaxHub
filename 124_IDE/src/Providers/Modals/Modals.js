import { useContext } from "react"
import { ModalContext } from "../ModalProvider"
import CreateIDEModal from "./CreateIDEModal"

export const Modal = () => {
    const modalFeatures = useContext(ModalContext)

    return <>
        {modalFeatures.activeModal === "CREATE_FILE" && CreateIDEModal}
    </>
}