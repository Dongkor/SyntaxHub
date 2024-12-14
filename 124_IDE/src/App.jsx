import { useState, useEffect } from "react";
import { Box, useToast } from "@chakra-ui/react";
import reactLogo from "./assets/react.svg";
import { invoke } from "@tauri-apps/api/core";  // Tauri API integration (if needed)
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import WelcomePage from "./pages/Welcome/WelcomePage";
import TestIDE from "./pages/IDE/testIDE";  // Ensure this component exists
import { TitleBar } from "./components/TitleBar.jsx";  // Ensure TitleBar is working
import { readTextFile, writeTextFile } from '@tauri-apps/plugin-fs'
import { open, save } from '@tauri-apps/plugin-dialog'
import { basename } from '@tauri-apps/api/path';

function App() {
  const navigate = useNavigate();
  const [Code, setCode] = useState(``)
  const [originalCode, setOriginalCode] = useState(``)
  const [Path, setPath] = useState(null)
  const [IsModified, setIsModified] = useState(false)
  const toast = useToast();

  //start new file
  const handleNewFile = async () => {
    setCode(``)
    setPath(null)
    setOriginalCode(``)
    setIsModified(false)
    toast({
      title: "New File Created",
      description: "You can now start coding in a new file.",
      status: "info",
      duration: 2000,
      isClosable: true,
      position: "top",
    });
    navigate('/ide');
  }

  //opening a file
  const handleOpenFile = async () => {
    try {
      const selectedPath = await open({
        multiple: false,
        directory: false
      });
      if (selectedPath) {
        const context = await readTextFile(selectedPath);
        setPath(selectedPath)
        const fileName = await basename(selectedPath);
        console.log("File Title:", fileName);
        console.log("context:", context)
        setCode(context);
        setOriginalCode(context)
        navigate('/ide');
      } else {
        console.log("No File Selected.");
        toast({
          title: "Warning",
          description: "No File Selected.",
          status: "warning",
          duration: 2000,
          isClosable: true,
          position: "top",
        });
      }

    } catch (error) {
      console.log(error)
      toast({
        title: "Error",
        description: "Failed to open the file.",
        status: "error",
        duration: 2000,
        isClosable: true,
        position: "top",
      });
    }
  }
  useEffect(() => {

    const normalizedCode = Code.trim();
    const normalizedOriginalCode = originalCode.trim();
    const modified = normalizedCode !== normalizedOriginalCode;
    setIsModified(modified);

  }, [Code]);
  return (
    <>
      <TitleBar isModified={IsModified} />
      {/* <CodeProvider> */}
      <Box
        minH="85vh"
        bg="#020C12"
        px={4}
        paddingTop="56px"
        paddingBottom="12px"
      >
        <Routes>
          {/* Welcome page route */}
          <Route path="/" element={<WelcomePage Path={Path} setPath={setPath} Code={Code} setCode={setCode} originalCode={originalCode} setOriginalCode={setOriginalCode} IsModified={IsModified} setIsModified={setIsModified} handleNewFile={handleNewFile} handleOpenFile={handleOpenFile} />} />

          {/* IDE page route */}
          <Route path="/ide" element={<TestIDE Path={Path} setPath={setPath} Code={Code} setCode={setCode} originalCode={originalCode} setOriginalCode={setOriginalCode} IsModified={IsModified} setIsModified={setIsModified} handleNewFile={handleNewFile} handleOpenFile={handleOpenFile} />} />
        </Routes>
      </Box>
    </>
  );
}

export default App;
