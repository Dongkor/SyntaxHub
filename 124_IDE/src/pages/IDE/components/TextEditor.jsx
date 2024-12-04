import React, { useEffect, useRef, useState } from 'react';
import './TextEditor.css';
import Editor, { useMonaco } from '@monaco-editor/react';
import Toolbar from '../components/Toolbar'
import { readText, writeText } from '@tauri-apps/plugin-clipboard-manager';

const editorOptions = {
    fontSize: 20,
    wordWrap: 'on'
};

const TextEditor = ({ code, setCode, onRun, onCompile, isModified }) => {
    const monaco = useMonaco();
    const editorRef = useRef(null);
    const [clipBoard, setClipBoard] = useState(false);
    const [isTextSelected, setIsTextSelected] = useState(false);
    const [canUndo, setCanUndo] = useState(true); // State for Undo button
    const [canRedo, setCanRedo] = useState(true); // State for Redo button

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

    const handleEditorChange = (value) => {
        setCode(value)
    }


    const handleUndo = () => {
        if (editorRef.current && canUndo) {
            editorRef.current.trigger('keyboard', 'undo', null);
        }
    };

    const handleRedo = () => {
        if (editorRef.current && canRedo) {
            editorRef.current.trigger('keyboard', 'redo', null);
        }
    };

    const handleCopy = async () => {
        if (editorRef.current && isTextSelected) {
            const selectedText = editorRef.current.getModel().getValueInRange(editorRef.current.getSelection());
            await writeText(selectedText); // Use Tauri's writeText instead of navigator.clipboard.writeText
            setClipBoard(true);
            console.log("Copied to clipboard:", selectedText);
        }
    };

    const handleCut = async () => {
        if (editorRef.current && isTextSelected) {
            const selectedText = editorRef.current.getModel().getValueInRange(editorRef.current.getSelection());
            await writeText(selectedText); // Use Tauri's writeText for cutting (to clipboard)
            editorRef.current.executeEdits(null, [
                { range: editorRef.current.getSelection(), text: '' } // Clear selected text
            ]);
            setClipBoard(true);
            console.log("Cut to clipboard:", selectedText);
        }
    };

    const handlePaste = async () => {
        if (editorRef.current) {
            const clipboardText = await readText(); // Use Tauri's readText for pasting
            editorRef.current.executeEdits(null, [
                { range: editorRef.current.getSelection(), text: clipboardText }
            ]);
            console.log("Pasted from clipboard:", clipboardText);
        }
    };

    const handleFind = () => {
        if (editorRef.current) {
            editorRef.current.trigger('keyboard', 'actions.find', null);
        }
    };


    useEffect(() => {
        setTimeout(() => {
            const editor = editorRef.current;

            if (editor) {
                const handleSelectionChange = () => {
                    const selection = editor.getSelection(); // Get current selection
                    if (!selection.isEmpty()) {
                        const selectedText = editor.getModel().getValueInRange(selection);
                        console.log(`Highlighted text: ${selectedText}`);
                        setIsTextSelected(true)// Log the selected text
                    } else {

                        setIsTextSelected(false)
                        console.log("No text is selected");
                    }
                };

                // Listen to selection changes
                const selectionChangeListener = editor.onDidChangeCursorSelection(handleSelectionChange);

                // Cleanup listener when the component unmounts
                return () => {
                    selectionChangeListener.dispose();
                };
            }
        }, 500);
    }, []);

    useEffect(() => {
        setTimeout(() => {
            const editor = editorRef.current;

            if (editor) {
                const handleContentChange = () => {
                    const model = editor.getModel();
                    if (model) {
                        setCanUndo(model.canUndo());
                        setCanRedo(model.canRedo());
                    }
                };
                const changeListener = editor.onDidChangeModelContent(handleContentChange);

                handleContentChange();
                return () => changeListener.dispose();
            }
        }, 500);
    }, []);

    useEffect(() => {
        // Check clipboard content on component mount
        const checkClipboardContent = async () => {
            try {
                const clipboardText = await readText();
                setClipBoard(clipboardText.trim().length > 0); // Update state based on clipboard content
            } catch (err) {
                console.error("Failed to read clipboard:", err);
                setClipBoard(false);
            }
        };

        checkClipboardContent(); // Initial check for clipboard content

        // Optional: Check clipboard periodically for updates
        const intervalId = setInterval(checkClipboardContent, 500); // Check every 1 second

        return () => clearInterval(intervalId); // Cleanup the interval on component unmount
    }, []);



    return (
        <div className='text-editor'>
            <div className='text-editor-content'>
                <Editor
                    theme="myCustomTheme"  // Apply the custom theme
                    options={editorOptions}
                    value={code}
                    onChange={handleEditorChange}
                    onMount={(editor) => {
                        editorRef.current = editor;
                    }}
                />
            </div>
            <Toolbar
                onUndo={handleUndo}
                onRedo={handleRedo}
                onCopy={handleCopy}
                onCut={handleCut}
                onPaste={handlePaste}
                onFind={handleFind}
                // onClear={handleClear}
                editorRef={editorRef}
                code={code}
                clipBoard={clipBoard}
                isTextSelected={isTextSelected}
                isUndoActive={canUndo}
                isRedoActive={canRedo}
                onRun={onRun}
                onCompile={onCompile}
                isModified={isModified}
            />
        </div>
    );
};

export default TextEditor;
