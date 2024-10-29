import { React, useState } from 'react'
import { Box, Text, IconButton, HStack, ButtonGroup, Flex, Divider } from '@chakra-ui/react';
import DropdownSVG from "../../assets/dropdown.svg"
import { TbChevronRightPipe } from "react-icons/tb";
import NavItem from './NavItem';
import logo from '../../assets/logo.png';
import NewSVG from "../../assets/new file.svg";
import OpenSVG from "../../assets/open file.svg"
import SaveSVG from "../../assets/save.svg"
import SaveAsSVG from "../../assets/save as.svg"
import ShareSVG from "../../assets/share.svg"



const Sidebar = ({ togglePage, onNewFile, onSave, onSaveAs, onOpenFile, isModified }) => {
    const [navSize, changeNavSize] = useState("large")
    // console.log(hasChanges)
    return (
        <Flex
            pos="sticky"
            left="0"
            height="97vh"
            marginY={0}
            paddingTop={navSize === "small" ? 2 : 0}
            bg="#297B71"
            color="white"
            boxShadow="0 4px 12px 0 rgba(0, 0, 0, 0.05)"
            borderRadius={12}
            w={navSize === "small" ? "3.5vw" : "15vw"}
            flexDir="column"
            transition='width 0.2s ease'
        >
            <Flex
                p="5%"
                flexDir="column"
                w="100%"
                alignItems={navSize === "small" ? "center" : "flex-start"}
                as="nav"
            >
                {/* Button to toggle nav size */}
                <Flex
                    w="100%"
                    justifyContent={navSize === "small" ? "center" : "space-between"}
                    alignItems="center"
                    marginBottom={1}
                    paddingBottom={1}
                >
                    {navSize === "large" && ( // Render logo only when navSize is large
                        <Flex alignItems="center" _hover={{ cursor: 'pointer' }} onClick={togglePage}>
                            <img src={logo} alt="Logo" style={{ height: '3rem', transition: 'transform 0.5s ease' }} />
                            <Text paddingLeft={1} color="#ffffff" fontSize="xl">SyntaxHub</Text>
                        </Flex>
                    )}
                    {navSize === "small" && (
                        <Flex alignItems="center" _hover={{ cursor: 'pointer' }} onClick={togglePage}>
                            <img src={logo} alt="Logo" style={{ height: '2.5rem', transition: 'transform 0.5s ease' }} />
                        </Flex>
                    )}
                </Flex>
                <Divider />
                {/* NavItems stacked vertically below the button */}
                <Flex flexDir="column" w="100%" mt={1} mb={navSize === "small" ? 695 : 685}>

                    <NavItem navSize={navSize} icon={NewSVG} title="New File" handleClick={onNewFile} isModified={false} />
                    <NavItem navSize={navSize} icon={OpenSVG} title="Open File" handleClick={onOpenFile} isModified={false} />
                    <NavItem navSize={navSize} icon={SaveSVG} title="Save" handleClick={onSave} isModified={!isModified} />
                    <NavItem navSize={navSize} icon={SaveAsSVG} title="Save As" handleClick={onSaveAs} isModified={!isModified} />
                    {/* <NavItem navSize={navSize} icon={ShareSVG} title="Share" /> */}
                </Flex>
                <Divider />
                <Flex w="100%" justifyContent="flex-end" > {/* Changed justifyContent to "flex-end" */}
                    <IconButton
                        size="lg"
                        background="none"
                        marginRight={1}
                        _hover={{ background: 'none' }}
                        title={navSize === "small" ? "Expand" : "Collapse"}
                        onClick={() => {
                            changeNavSize(navSize === "small" ? "large" : "small");
                        }}
                        aria-label={navSize === "small" ? "Expand sidebar" : "Collapse sidebar"}
                    >
                        <TbChevronRightPipe style={{ fontSize: "1.4rem", transform: navSize === "small" ? '' : 'scaleX(-1)', transition: 'transform 0.5s ease' }} />
                    </IconButton>
                </Flex>
            </Flex>
        </Flex>
    );
}

export default Sidebar