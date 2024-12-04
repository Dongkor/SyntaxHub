import React from 'react';
import { IconButton, Text } from "@chakra-ui/react";
import { FaRegWindowMinimize, FaRegWindowMaximize } from "react-icons/fa";
import { BsXLg } from "react-icons/bs";
import './TitleBar.css';
import logo from "../assets/logo.png";
import { getCurrentWindow } from '@tauri-apps/api/window';
import { Link } from 'react-router-dom';
import { confirm } from '@tauri-apps/plugin-dialog';
import closeSVG from '../pages/IDE/assets/x.svg'

export const TitleBar = ({ isModified }) => {
    const appWindow = getCurrentWindow();

    const handleMinimize = async () => {
        await appWindow.minimize();
    };

    const handleMaximizeRestore = async () => {
        const isMaximized = await appWindow.isMaximized();
        if (isMaximized) {
            await appWindow.unmaximize();
        } else {
            await appWindow.maximize();
        }
    };

    const handleClose = async () => {
        if (isModified) {
            // If there are unsaved changes, show a confirmation dialog
            const userConfirmed = await confirm(
                "You have unsaved changes. Are you sure you want to close?",
                {
                    title: "Unsaved Changes Detected", // Customize the title
                    type: "warning",                 // Set the dialog type (e.g., "info", "warning", "error")
                    okLabel: "Okay"         // Customize the "OK" button label
                }
            );

            if (!userConfirmed) {
                // If the user cancels, do nothing
                return;
            }
        }

        // Close the window if no unsaved changes or user confirms
        await appWindow.close();
    };

    return (
        <div data-tauri-drag-region className='title-bar'>
            {/* Logo and Title - Navigates to Home */}
            <Link to="/">
                <div className='title'>
                    <img src={logo} alt="Logo" style={{ height: '3rem' }} />
                    <Text fontSize='16px' color="#ffffff">SyntaxHub</Text>
                </div>
            </Link>
            {/* Window Control Buttons */}
            <div className='buttons'>
                <IconButton
                    paddingX={5}
                    borderRadius={0}
                    aria-label="Minimize"
                    variant="ghost"
                    onClick={handleMinimize}>
                    <FaRegWindowMinimize />
                </IconButton>

                <IconButton
                    paddingX={5}
                    borderRadius={0}
                    aria-label="Maximize/Restore"
                    variant="ghost"
                    onClick={handleMaximizeRestore}>
                    <FaRegWindowMaximize />
                </IconButton>

                <IconButton
                    paddingX={5}
                    borderRadius={0}
                    aria-label="Close"
                    variant="ghost"
                    onClick={handleClose}
                    sx={{
                        _hover: {
                            bg: "red.500", // Set the background to red when hovered
                        },
                    }}>

                    <img src={closeSVG} alt="" height="1rem" width="20rem" />
                </IconButton>
            </div>
        </div>
    );
};
