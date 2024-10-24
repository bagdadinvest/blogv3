(function() {
    // Function to handle parsing the HTML content inside the editor
    function parseHTMLContent(editorState) {
        const contentState = editorState.getCurrentContent();
        const rawContent = window.draftail.convertToRaw(contentState);

        let blocks = rawContent.blocks;
        let parsedBlocks = [];

        blocks.forEach((block) => {
            let blockText = block.text;

            // Use a DOMParser to parse and remove HTML tags
            const doc = new DOMParser().parseFromString(blockText, 'text/html');
            const parsedText = doc.body.textContent || ""; // Text without HTML tags

            // Determine the block type based on the original HTML tag
            let blockType = block.type;
            if (blockText.includes('<h2>')) {
                blockType = 'header-two';
            } else if (blockText.includes('<h3>')) {
                blockType = 'header-three';
            } else if (blockText.includes('<h4>')) {
                blockType = 'header-four';
            } else if (blockText.includes('<p>')) {
                blockType = 'paragraph';
            }

            // Push the updated block
            parsedBlocks.push({
                ...block,
                text: parsedText,
                type: blockType,
            });
        });

        // Create the new content state and return it as EditorState
        const newRawContent = {
            ...rawContent,
            blocks: parsedBlocks,
        };

        const newContentState = window.draftail.convertFromRaw(newRawContent);
        return window.draftail.EditorState.push(editorState, newContentState);
    }

    // Register the Draftail plugin for the "parse-html" control
    window.draftail.registerPlugin({
        type: 'entity',
        name: 'parse-html',
        onClick: (editorState, setEditorState) => {
            const newEditorState = parseHTMLContent(editorState);
            setEditorState(newEditorState);
        },
        icon: 'icon-code',
    });
})();
