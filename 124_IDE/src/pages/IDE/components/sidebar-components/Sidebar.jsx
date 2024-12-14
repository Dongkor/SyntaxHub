import { React, useState, useEffect } from 'react'
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



const Sidebar = ({ navSize, changeNavSize, onNewFile, onSave, onSaveAs, onOpenFile, isModified, code }) => {

    return (
        <Flex
            pos="sticky"
            minWidth={"70px"}
            height="93.5vh"
            bg="#297B71"
            color="white"
            boxShadow="0 4px 12px 0 rgba(0, 0, 0, 0.05)"
            borderRadius={12}
            w={navSize === "small" ? "3.5vw" : "15vw"}
            flexDir="column"
            transition='width 0.2s ease'
            alignItems={navSize === "small" ? "center" : "flex-start"}
            p={navSize === "small" ? "5px" : "10px"}
        >
            <Flex flexDir="column" w="100%" mt={1} className='buttons' height={"95%"}>

                <NavItem navSize={navSize} icon={NewSVG} title="New File" handleClick={onNewFile} isModified={false} />
                <NavItem navSize={navSize} icon={OpenSVG} title="Open File" handleClick={onOpenFile} isModified={false} />
                <NavItem navSize={navSize} icon={SaveSVG} title="Save" handleClick={onSave} isModified={!isModified} />
                <NavItem navSize={navSize} icon={SaveAsSVG} title="Save As" handleClick={onSaveAs} isModified={!code} />
            </Flex>
            <Divider />
            <Flex w="100%" justifyContent={navSize === "small" ? "center" : "flex-end"} className='toggle-button' height={"5%"} alignItems={"center"}> {/* Changed justifyContent to "flex-end" */}
                <IconButton
                    size="lg"
                    background="none"
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
    );
}

export default Sidebar