import { React, useState, useEffect, Component } from 'react'
import './testIDE.css'
import Sidebar from './components/sidebar-components/Sidebar'
import { invoke } from '@tauri-apps/api/core';
import { Box, Text, useToast } from '@chakra-ui/react'
import TextEditor from './components/TextEditor'
import { readTextFile, writeTextFile } from '@tauri-apps/plugin-fs'
import { open, save } from '@tauri-apps/plugin-dialog'
import { basename } from '@tauri-apps/api/path';

const TestIDE = ({ Path, setPath, Code, setCode, originalCode, setOriginalCode, IsModified, setIsModified, handleNewFile, handleOpenFile }) => {
    const [sideBar, setSideBar] = useState("small")
    const toast = useToast()

    const run_compiler = async (event) => {
        event.preventDefault();
        try {
            console.log(Path)
            const response = await invoke('run_python_compiler', { filePath: Path });
            console.log(response);  // Logs: "Python script ran successfully!"
        } catch (error) {
            console.error('Error running Python script:', error);
        }
    };
    const compile_only = async (event) => {
        event.preventDefault();
        try {
            console.log(Path)
            const response = await invoke('compile_only', { filePath: Path });
            console.log(response);  // Logs: "Python script ran successfully!"
        } catch (error) {
            console.error('Error running Python script:', error);
        }
    };

    const handleSaveFile = async () => {
        if (!Path) {
            // If no path exists, ask for Save As
            handleSaveAsFile();
        } else {
            try {
                await writeTextFile(Path, Code); // Save code to the current file path
                setOriginalCode(Code); // Update original code after saving
                setIsModified(false)// console.log(`File saved at ${Path}`);
                // setCode(Code)
                toast({
                    title: "Success!",
                    description: `Your file has been saved successfully at ${Path}.`,
                    status: "success",
                    duration: 2000, // Duration in milliseconds
                    isClosable: true,
                    position: "top", // Position of the toast
                });
            } catch (error) {
                console.error("Error saving file:", error);
                toast({
                    title: "Error",
                    description: "Failed to save the file.",
                    status: "error",
                    duration: 2000,
                    isClosable: true,
                    position: "top",
                });
            }
        }
    }

    const handleSaveAsFile = async () => {
        try {
            // Open the file dialog to choose a location and filename
            const selectedSavePath = await save({
                defaultPath: Path || "untitled.txt", // Default to current file path if available
                filters: [{ name: "Text Files", extensions: ["txt"] }] // Filter file types
            });

            if (selectedSavePath) {
                // Write the code to the new file path
                await writeTextFile(selectedSavePath, Code);
                setPath(selectedSavePath); // Update the file path state

                setOriginalCode(Code)
                setIsModified(false)
                console.log(`File saved at ${selectedSavePath}`);
                toast({
                    title: "Success!",
                    description: "Your file has been saved successfully.",
                    status: "success",
                    duration: 2000,
                    isClosable: true,
                    position: "top",
                });
            }
        } catch (error) {
            console.error("Error saving file:", error);
            toast({
                title: "Error",
                description: "Failed to save the file.",
                status: "warning",
                duration: 2000,
                isClosable: true,
                position: "top",
            });
        }
    }



    return (
        <>
            <div className='body'>

                <div
                    className='code-editor'
                    style={{ width: sideBar === "small" ? "51.5%" : "60%" }}
                >
                    <div className='code-editor-sidebar'><Sidebar code={Code} navSize={sideBar} changeNavSize={setSideBar} onNewFile={handleNewFile} onOpenFile={handleOpenFile} onSave={handleSaveFile} onSaveAs={handleSaveAsFile} isModified={IsModified} /></div>
                    <div className='code-editor-content'>
                        <Text color="#86A0A0" px={3} height="5%" className='code-editor-header'>Code Editor</Text>
                        <Box bg="#071821" className='editor-box' w="100%" height="95%" borderRadius={12} >
                            <TextEditor code={Code} setCode={setCode} onRun={run_compiler} isModified={IsModified} onCompile={compile_only} />
                        </Box>
                    </div>
                </div>
                <div
                    className='terminal-container'
                    style={{ width: sideBar === "small" ? "48.5%" : "40%" }}
                >
                    <Text color="#86A0A0" px={3} height="5%" className='terminal-header'>Terminal</Text>
                    <Box bg="#071821" className='terminal-box' w="100%" height="95%" borderRadius={12} >
                        {/* <Terminal Path={Path} /> */}
                    </Box>
                </div>

            </div >

        </>
    )
}

export default TestIDE