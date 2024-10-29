import React, { useRef, useState, useEffect } from 'react';
import Editor, { useMonaco } from '@monaco-editor/react';
import { Box } from '@chakra-ui/react';
import Toolbar from './Toolbar'; // Import your Toolbar component

const CodeEditor = ({ editorRef, setChange }) => {
    const [code, setCode] = useState(``);
    const [clipBoard, setClipBoard] = useState(false)
    const monaco = useMonaco();

    // Apply the custom theme when Monaco is available
    useEffect(() => {
        if (monaco) {
            monaco.editor.defineTheme('myCustomTheme', {
                base: 'vs-dark',
                rules: [],
                colors: {
                    'editor.background': '#071821',
                    'editor.foreground': '#7B87ED',
                },
            });
            monaco.editor.setTheme('myCustomTheme');
        }
    }, [monaco]);

    // Handle editor content change
    const handleEditorChange = (value) => {
        // setChange(true);
        setCode(value);

    };

    // Capture the editor instance once it mounts
    const handleEditorDidMount = (editor, monaco) => {
        editorRef.current = editor; // Set the editor instance in the ref
    };

    // Function to trigger undo
    const handleUndo = () => {
        if (editorRef.current) {
            editorRef.current.trigger('keyboard', 'undo', null);
        }
    };

    // Function to trigger redo
    const handleRedo = () => {
        if (editorRef.current) {
            editorRef.current.trigger('keyboard', 'redo', null);
        }
    };

    // Clipboard: Copy text manually
    const handleCopy = async () => {
        if (editorRef.current) {
            const selectedText = editorRef.current.getModel().getValueInRange(editorRef.current.getSelection());
            if (selectedText) {
                await navigator.clipboard.writeText(selectedText);
                setClipBoard(true)
                console.log("Copied to clipboard:", selectedText);
            }
        }
    };

    // Clipboard: Cut text manually (copy and delete the selected text)
    const handleCut = async () => {
        if (editorRef.current) {
            const selectedText = editorRef.current.getModel().getValueInRange(editorRef.current.getSelection());
            if (selectedText) {
                await navigator.clipboard.writeText(selectedText);
                editorRef.current.executeEdits(null, [
                    { range: editorRef.current.getSelection(), text: '' } // Clear the selected text
                ]);
                setClipBoard(true)
                console.log("Cut to clipboard:", selectedText);
            }
        }
    };

    // Clipboard: Paste text manually
    const handlePaste = async () => {
        if (editorRef.current) {
            const clipboardText = await navigator.clipboard.readText();
            editorRef.current.executeEdits(null, [
                { range: editorRef.current.getSelection(), text: clipboardText }
            ]);
            console.log("Pasted from clipboard:", clipboardText);
        }
    };

    // Function to trigger find
    const handleFind = () => {
        if (editorRef.current) {
            editorRef.current.trigger('keyboard', 'actions.find', null);
        }
    };

    // Function to clear the editor content
    const handleClear = () => {
        if (editorRef.current) {
            editorRef.current.setValue(''); // Clear the editor content
        }
    };

    return (
        <Box>
            <Box height="1rem" px={4} py={4} marginTop={8}>
                <Editor
                    height="80vh"
                    // paddingTop={10}
                    language="python"
                    theme="myCustomTheme"
                    value={code}
                    onChange={handleEditorChange}
                    onMount={handleEditorDidMount} // Attach the editor instance on mount
                />
            </Box>

            {/* Toolbar with Undo and Redo Buttons */}
            <Toolbar
                onUndo={handleUndo}
                onRedo={handleRedo}
                onCopy={handleCopy}
                onCut={handleCut}
                onPaste={handlePaste}
                onFind={handleFind}
                onClear={handleClear}
                editorRef={editorRef}
                code={code}
                clipBoard={clipBoard}
            />
        </Box>
    );
};

export default CodeEditor;
