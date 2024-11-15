import React from 'react'
import { useNavigate } from 'react-router-dom';
import { Box, Text, Button } from "@chakra-ui/react"
import logo from "../../assets/logo.png"

const WelcomePage = ({ Path, setPath, Code, setCode, originalCode, setOriginalCode, IsModified, setIsModified, handleNewFile, handleOpenFile }) => {

    return (
        <Box
            minH="93.65vh"
            borderRadius={20}
            bg="#071821"
            px={16}
            py={16}
            position="relative"
            overflow="hidden"
        >
            <Text fontSize='6rem' fontWeight="semibold">
                <Text
                    as="span"
                    color="#C4EBFF"
                    textShadow="0px 0px 25px #C4EBFF" // Glowing effect for "Welcome to"
                >
                    Welcome to{' '}
                </Text>
                <Text
                    as="span"
                    color="#90D9FF"
                    textShadow="0px 0px 25px #90D9FF" // Glowing effect for "Syntax"
                >
                    Syntax
                </Text>
                <Text
                    as="span"
                    color="#8ED2CA"
                    textShadow="0px 0px 25px #8ED2CA" // Glowing effect for "Hub"
                >
                    Hub
                </Text>
                <Text
                    as="span"
                    color="#C4EBFF"
                    textShadow="0px 0px 25px #C4EBFF" // Glowing effect for "Welcome to"
                >
                    !
                </Text>
            </Text>
            <Text fontSize='2.5rem' color="#304D5C" fontWeight="semibold">Your efficient coding companion.</Text>
            <Text fontSize='2rem' color="#304D5C" paddingTop={100} marginBottom={2}>Quick start:</Text>
            {/* <Button
                onClick={handleGetStarted}
                mt={5} // Add margin to the button
                colorScheme="teal" // Use Chakra UI color scheme
                size="lg" // Adjust button size
            >
                Get Started!
            </Button> */}
            <Text fontSize='1.5rem' color="#509D94" marginLeft={5} onClick={handleNewFile} style={{ cursor: 'pointer' }}>   Open New File...</Text>
            <Text fontSize='1.5rem' color="#509D94" marginLeft={5} marginTop={2} onClick={handleOpenFile} style={{ cursor: 'pointer' }}>   Open Existing File...</Text>

            <Text fontSize='2rem' color="#304D5C" paddingTop={250}>Creators:</Text>
            <Text fontSize='1.3rem' color="#509D94" paddingTop={3} paddingLeft={3}>Fiel Jr. Condor</Text>
            <Text fontSize='1.3rem' color="#509D94" paddingTop={3} paddingLeft={3}>Liora Zhaune Cabanos</Text>
            <Text fontSize='1.3rem' color="#509D94" paddingTop={3} paddingLeft={3}>Jamaica Ruri Augusto</Text>
            <Box
                as="img"
                src={logo}
                alt="Logo"
                position="absolute"
                right="-25%" // Adjust to your preference for positioning
                bottom="-20%" // Adjust to your preference for positioning
                zIndex={0} // Send it to the back // Make it semi-transparent if desired
                opacity={0.9}
                style={{ height: '1500px', transform: 'rotate(290deg)' }} // Adjust the height as needed
            />
        </Box>
    )
}

export default WelcomePage