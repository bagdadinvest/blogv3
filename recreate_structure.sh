#!/bin/bash

# Script to recreate directory and file structure from a given tree command output file.

TREE_FILE="tree_structure.txt"

# Function to create directories and files
create_structure() {
    while IFS= read -r line; do
        # Determine the depth based on leading whitespace
        depth=$(echo "$line" | sed -e 's/\S.*$//' | wc -c)
        stripped_line=$(echo "$line" | xargs)

        # Skip empty lines or lines starting with dots (e.g., "./")
        if [[ -z "$stripped_line" ]] || [[ "$stripped_line" == .* ]]; then
            continue
        fi

        if [[ "$stripped_line" == */ ]]; then
            # It's a directory
            dir_name=$(echo "$stripped_line" | sed 's:/$::')
            mkdir -p "$PWD/$dir_name" 2>/dev/null || {
                echo "Error creating directory: $dir_name"
                read -p "Retry manually? (y/n): " retry
                if [[ "$retry" == "y" ]]; then
                    mkdir -p "$PWD/$dir_name"
                fi
            }
            cd "$dir_name" || exit
        else
            # It's a file
            touch "$PWD/$stripped_line" 2>/dev/null || {
                echo "Error creating file: $stripped_line"
                read -p "Retry manually? (y/n): " retry
                if [[ "$retry" == "y" ]]; then
                    touch "$PWD/$stripped_line"
                fi
            }
        fi
    done <"$TREE_FILE"
}

# Main execution
echo "Starting structure recreation from $TREE_FILE..."

if [[ ! -f "$TREE_FILE" ]]; then
    echo "Error: $TREE_FILE not found!"
    echo "Please run 'tree -o tree_structure.txt' to generate the tree file."
    exit 1
fi

# Ensure we start in the root directory
root_dir=$(head -1 "$TREE_FILE" | xargs)
if [[ -z "$root_dir" ]]; then
    echo "Error: Root directory not found in $TREE_FILE."
    exit 1
fi

echo "Root directory: $root_dir"
mkdir -p "$root_dir" || {
    echo "Error creating root directory: $root_dir"
    exit 1
}
cd "$root_dir" || exit

# Call the function to process the tree file
create_structure

echo "Structure recreation completed successfully."
