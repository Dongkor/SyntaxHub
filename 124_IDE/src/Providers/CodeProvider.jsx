import { useContext, createContext } from "react";

export const CodeContext = createContext();

export const CodeProvider = ({ children }) => {
    return (
        <CodeContext.Provider>
            {children}
        </CodeContext.Provider>
    );
}