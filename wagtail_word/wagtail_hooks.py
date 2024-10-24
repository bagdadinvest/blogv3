# from wagtail import hooks
# from wagtail.admin.rich_text.editors.draftail import features as draftail_features
#
# # 1. Register the custom button in Draftail for HTML parsing
# @hooks.register('register_rich_text_features')
# def register_html_parser_feature(features):
#     feature_name = "parse-html"
#     features.default_features.append(feature_name)
#
#     # Register the feature with a Draftail control button
#     features.register_editor_plugin(
#         'draftail',
#         feature_name,
#         draftail_features.EntityFeature(
#             {
#                 "type": feature_name,
#                 "icon": "icon-code",  # Wagtail's default code icon
#             },
#         ),
#     )
#
#
# # 2. Inject custom JavaScript for the button behavior
# @hooks.register('insert_editor_js')
# def extend_draftail_with_custom_button():
#     return '''
#     <script>
#         (function() {
#             // Function to handle HTML parsing in the editor
#             function parseHTMLContent(editorState) {
#                 const rawContent = window.draftail.convertToRaw(editorState);
#                 let blocks = rawContent.blocks;
#                 let parsedBlocks = [];
#
#                 // Iterate through blocks to find HTML tags
#                 blocks.forEach((block) => {
#                     let blockText = block.text;
#
#                     // Use a DOMParser to extract inner text from the HTML
#                     const doc = new DOMParser().parseFromString(blockText, 'text/html');
#                     const parsedText = doc.body.innerText || "";
#
#                     // Convert HTML tags into Draftail block types
#                     let blockType = block.type;
#                     if (blockText.includes('<h2>')) {
#                         blockType = 'header-two';
#                     } else if (blockText.includes('<h3>')) {
#                         blockType = 'header-three';
#                     } else if (blockText.includes('<h4>')) {
#                         blockType = 'header-four';
#                     } else if (blockText.includes('<p>')) {
#                         blockType = 'paragraph';
#                     }
#
#                     // Create a new block with the updated text and type
#                     parsedBlocks.push({
#                         ...block,
#                         text: parsedText,
#                         type: blockType,
#                     });
#                 });
#
#                 // Create a new content state with the parsed blocks
#                 const newRawContent = {
#                     ...rawContent,
#                     blocks: parsedBlocks,
#                 };
#
#                 // Update the editor state with the parsed content
#                 return window.draftail.EditorState.createWithContent(window.draftail.convertFromRaw(newRawContent));
#             }
#
#             // Register the plugin and associate it with the custom button
#             window.draftail.registerPlugin({
#                 type: 'entity',
#                 name: 'parse-html',
#                 onClick: (editorState, setEditorState) => {
#                     const newEditorState = parseHTMLContent(editorState);
#                     setEditorState(newEditorState);
#                 },
#                 icon: 'icon-code',  // You can use any other icon from Wagtail
#             });
#         })();
#     </script>
#     '''
#
#
# # 3. Optional: Inject CSS for customizing the button appearance
# @hooks.register('insert_editor_css')
# def extend_draftail_with_custom_styles():
#     return '''
#     <style>
#         /* Optional: Custom styling for the Parse HTML button */
#         .Draftail-ToolbarButton__parse-html {
#             color: #007bff;
#             background-color: transparent;
#             border: none;
#             font-weight: bold;
#             padding: 5px;
#             cursor: pointer;
#         }
#
#         .Draftail-ToolbarButton__parse-html:hover {
#             color: #0056b3;
#             background-color: #e9ecef;
#             border-radius: 4px;
#         }
#     </style>
#     '''
