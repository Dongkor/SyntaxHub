import { useState } from "react";
import { Box } from "@chakra-ui/react"
import reactLogo from "./assets/react.svg";
import { invoke } from "@tauri-apps/api/core";
import WelcomePage from "./Welcome/WelcomePage";
import IDEPage from "./IDE/IDEPage";


function App() {
  const [Page, setPage] = useState("welcome");

  const togglePage = () => {
    setPage((prev) => (prev === "welcome" ? "ide" : "welcome")); // Toggle between welcome and ide
  };
  return (
    <Box
      minH="100vh"
      bg="#020C12"
      px={4}
      py={4}
    >
      {Page === "welcome" && <WelcomePage togglePage={togglePage} />}
      {Page === "ide" && <IDEPage togglePage={togglePage} />}
    </Box>
  );
}

export default App;
