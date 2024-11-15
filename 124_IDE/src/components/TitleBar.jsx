import React from 'react';
import { IconButton, Text } from "@chakra-ui/react";
import { FaRegWindowMinimize, FaRegWindowMaximize } from "react-icons/fa";
import { BsXLg } from "react-icons/bs";
import './TitleBar.css';
import logo from "../assets/logo.png";
import { getCurrentWindow } from '@tauri-apps/api/window';
import { Link } from 'react-router-dom';

export const TitleBar = () => {
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
                    aria-label="Minimize"
                    variant="ghost"
                    onClick={handleMinimize}>
                    <FaRegWindowMinimize />
                </IconButton>

                <IconButton
                    aria-label="Maximize/Restore"
                    variant="ghost"
                    onClick={handleMaximizeRestore}>
                    <FaRegWindowMaximize />
                </IconButton>

                <IconButton
                    aria-label="Close"
                    variant="ghost"
                    onClick={handleClose}>
                    <BsXLg />
                </IconButton>
            </div>
        </div>
    );
};
