import { React, useState, useRef, useEffect } from 'react'
import { Box, Text, HStack, VStack, useToast } from "@chakra-ui/react"
import CodeEditor from './components/CodeEditor'
import Toolbar from './components/Toolbar'
import Sidebar from './components/sidebar-components/Sidebar'

const IDEPage = ({ togglePage }) => {
    const editorRef = useRef(null); // Reference to access editor instance later
    const toast = useToast();
    const [File, setFile] = useState(null)
    const [Change, setChange] = useState(false)
    const [originalFileContent, setOriginalFileContent] = useState(''); // Store the original content of the file
    const [isModified, setIsModified] = useState(false);

    const handleNewFile = async () => {

        editorRef.current.setValue('');
        setFile(null)
        setIsModified(false)
        toast({
            title: "New File Created",
            description: "You can now start coding in a new file.",
            status: "info",
            duration: 2000,
            isClosable: true,
            position: "top",
        });
    }
    // Function to save the current content to a .txt file
    const handleSaveFile = async () => {
        try {
            // If a file handle is already stored (i.e., a file was opened or saved previously)
            setIsModified(!isModified)
            if (File) {
                const writableStream = await File.createWritable();
                await writableStream.write(editorRef.current.getValue());
                await writableStream.close();
                toast({
                    title: "Success!",
                    description: "Your file has been saved successfully.",
                    status: "success",
                    duration: 2000, // Duration in milliseconds
                    isClosable: true,
                    position: "top", // Position of the toast
                });
            } else {
                // If no file handle, treat this as a 'Save As' operation
                await handleSaveAsFile();
            }
        } catch (error) {
            console.error('Error saving file:', error);
            toast({
                title: "Error",
                description: "Failed to save the file.",
                status: "error",
                duration: 2000,
                isClosable: true,
                position: "top",
            });
        }
    };

    const handleOpenFile = async () => {
        try {
            if ('showOpenFilePicker' in window) {
                // Use File System Access API
                const [fileHandle] = await window.showOpenFilePicker({
                    types: [
                        {
                            description: 'Text Files',
                            accept: { 'text/plain': ['.txt'] },
                        },
                    ],
                    multiple: false, // Ensure the user selects only one file
                });

                const file = await fileHandle.getFile();
                const content = await file.text();

                // Set the content of the file in Monaco Editor
                editorRef.current.setValue(content);
                setFile(fileHandle)
                setOriginalFileContent(content);

                // Reset modified state since it's a newly loaded file
                setIsModified(false);
            } else {
                // Fallback for browsers that don't support File System Access API
                const input = document.createElement('input');
                input.type = 'file';
                input.accept = '.txt';

                input.onchange = async (event) => {
                    const file = event.target.files[0];
                    if (file) {
                        const reader = new FileReader();
                        reader.onload = (e) => {
                            const content = e.target.result;
                            editorRef.current.setValue(content); // Set the content to the editor
                        };
                        reader.readAsText(file);
                    }
                };

                input.click(); // Trigger the file input
            }
        } catch (error) {
            console.error('Error opening file:', error);
            // alert('Failed to open the file.');
            toast({
                title: "Warning",
                description: "Was not able to open the file.",
                status: "warning",
                duration: 2000,
                isClosable: true,
                position: "top",
            });
        }
    };

    const handleEditorChange = () => {
        const currentContent = editorRef.current.getValue();
        // Compare current content with the original content to determine if the file is modified
        setIsModified(currentContent !== originalFileContent);
    };

    // Function to "Save As" a new file with user-provided name
    const handleSaveAsFile = async () => {
        try {
            if ('showSaveFilePicker' in window) {
                const fileHandle = await window.showSaveFilePicker({
                    suggestedName: 'new_code.txt',
                    types: [
                        {
                            description: 'Text Files',
                            accept: { 'text/plain': ['.txt'] },
                        },
                    ],
                });

                const writableStream = await fileHandle.createWritable();
                await writableStream.write(editorRef.current.getValue());
                await writableStream.close();
                toast({
                    title: "Success!",
                    description: "Your file has been saved successfully.",
                    status: "success",
                    duration: 2000,
                    isClosable: true,
                    position: "top",
                });
            } else {
                const content = editorRef.current.getValue();
                const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });

                const fileName = prompt('Enter new file name:', 'code');
                const link = document.createElement('a');
                link.href = URL.createObjectURL(blob);
                link.download = `${fileName || 'code'}.txt`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
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
            console.error('Error saving file:', error);
            toast({
                title: "Error",
                description: "Failed to save the file.",
                status: "warning",
                duration: 2000,
                isClosable: true,
                position: "top",
            });
        }
    };

    useEffect(() => {
        if (editorRef.current) {
            // Add change listener to the editor when it's mounted
            const model = editorRef.current.getModel();
            model.onDidChangeContent(handleEditorChange);
        }
    }, []);
    // console.log("isModified:", isModified, originalFileContent)
    return (
        <Box minH="97vh">

            <HStack alignItems="stretch">
                {/* Sidebar positioned on the left */}
                {/* You can adjust the width */}

                <Sidebar togglePage={togglePage} onNewFile={handleNewFile} onSave={handleSaveFile} onSaveAs={handleSaveAsFile} onOpenFile={handleOpenFile} isModified={isModified} />
                {/* </Box> */}

                {/* Main content */}
                <VStack w="100%" spacing={4} alignItems="stretch"> {/* Adjust to take the remaining width */}
                    <HStack>
                        <Text w="50%" color="#86A0A0" py={2} px={3}>Input</Text>
                        <Text w="50%" color="#86A0A0" py={2} px={3}>Output</Text>
                    </HStack>

                    <HStack w="100%" alignItems="flex-end" justifyContent="space-between" py={0}>
                        <Box
                            w="50%"
                            height="91.7vh"
                            bottom="3vh"
                            borderRadius={12}
                            bg="#071821"
                        >
                            {/* <Text color="#589B81" py={1} px={3}>File Location</Text> */}
                            <CodeEditor editorRef={editorRef} setChange={setChange} />
                        </Box>

                        <Box
                            w="50%"
                            height="91.7vh"
                            borderRadius={12}
                            bg="#071821"
                        >
                            {/* <Text color="#589B81" py={1} px={3}>File Location</Text> */}
                        </Box>
                    </HStack>


                </VStack>
            </HStack>
        </Box>
    )
}

export default IDEPage