import { React, useState, useEffect } from 'react'
import { Box, Text, IconButton, HStack, ButtonGroup, Menu, MenuButton, MenuList, MenuItem } from '@chakra-ui/react';
import CutSVG from "../assets/cut.svg";
import CopySVG from "../assets/copy.svg"
import PasteSVG from "../assets/paste.svg"
import ClearSVG from "../assets/clear.svg"
import UndoSVG from "../assets/undo.svg"
import RedoSVG from "../assets/redo.svg"
import FindSVG from "../assets/find.svg"
import PlaySVG from "../assets/play.svg"
import DropdownSVG from "../assets/dropdown.svg"



const Toolbar = ({ onUndo, onRedo, onCopy, onCut, onPaste, onFind, code, clipBoard, isTextSelected, isUndoActive, isRedoActive, onRun, onCompile, isModified }) => {
    return (
        <Box
            position="fixed" // Fixes the box to the viewport
            bottom="1vh" // Adjust vertical position to the bottom
            left="50%" // Start from the left center
            transform="translateX(-50%)" // Center the box horizontally
            height="70px"
            width="445px" // Width of the floating box
            minWidth="445px"
            px={2}
            borderRadius="15px" // Rounded corners
            boxShadow="md" // Shadow for depth
            bg="#297B71" // Background color
            color="white" // Text color
            zIndex="1000" // Ensures it appears above other elements
            display="flex" // Use flexbox for centering
            flexDirection="column" // Stack children vertically
            alignItems="center" // Center children horizontally
            justifyContent="center" // Center children vertically
            borderWidth="1px"
            borderColor="#BABABA"
        >
            <HStack>
                <IconButton size="lg" borderWidth="1px" borderColor="#BABABA" title="Cut" onClick={onCut} isDisabled={!isTextSelected}>
                    <img src={CutSVG} height="1rem" width="35rem" />
                </IconButton>
                <IconButton size="lg" borderWidth="1px" borderColor="#BABABA" title="Copy" onClick={onCopy} isDisabled={!isTextSelected}>
                    <img src={CopySVG} height="1rem" width="35rem" />
                </IconButton>
                <IconButton size="lg" borderWidth="1px" borderColor="#BABABA" title="Paste" onClick={onPaste} isDisabled={!clipBoard}>
                    <img src={PasteSVG} height="1rem" width="27rem" />
                </IconButton>
                <ButtonGroup isAttached>
                    <IconButton size="lg" borderWidth="1px" borderColor="#BABABA" title="Undo" onClick={onUndo} isDisabled={!isUndoActive}>
                        <img src={UndoSVG} height="1rem" width="35rem" />
                    </IconButton>
                    <IconButton size="lg" borderWidth="1px" borderColor="#BABABA" title="Redo" onClick={onRedo} isDisabled={!isRedoActive}>
                        <img src={RedoSVG} height="1rem" width="26rem" />
                    </IconButton>
                </ButtonGroup>
                <IconButton size="lg" borderWidth="1px" borderColor="#BABABA" title="Find" onClick={onFind} isDisabled={code ? false : true}>
                    <img src={FindSVG} height="1rem" width="30rem" />

                </IconButton>
                <ButtonGroup isAttached>
                    <IconButton size="lg" borderWidth="1px" borderColor="#BABABA" title="Run" onClick={onRun} isDisabled={isModified || !code}>
                        <img src={PlaySVG} height="1rem" width="35rem" />
                    </IconButton>
                    <Menu>
                        <MenuButton
                            as={IconButton}
                            size="lg"
                            borderWidth="1px"
                            flexShrink={1}
                            borderColor="#BABABA"
                            title="More"
                            paddingLeft={'5px'}
                            minWidth="2rem"
                            isDisabled={isModified || !code}
                        >
                            <img src={DropdownSVG} height="1rem" width="20rem" />
                        </MenuButton>
                        <MenuList>
                            <MenuItem onClick={onCompile}>Compile only</MenuItem>
                        </MenuList>
                    </Menu>
                </ButtonGroup>
            </HStack>
            {/*  */}

        </Box>
    );

}

export default Toolbar
