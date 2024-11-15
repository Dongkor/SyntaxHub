import { useState, useContext, createContext } from "react";
import createIDEModal from "./Modals/CreateIDEModal"

export const ModalContext = createContext();

export const ModalProvider = ({ children }) => {
    const [modalType, setModalType] = useState(null)

    const closeModal = () => {
        setModalType(null)
    }

    const modalFeatures = {
        openModal: setModalType,
        closeModal,
        activeModal: modalType
    }

    return (
        <ModalContext.Provider value={modalFeatures}>
            {children}
        </ModalContext.Provider>
    )
}