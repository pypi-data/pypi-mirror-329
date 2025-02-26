from pathlib import Path

def write_to_latex(func):
    """
    Decorator that writes the output of a function to a LaTeX document

    Note: The line after the keyword is removed from the LaTeX document
    
    args:
        file_path: Path to the LaTeX document
        keyword: Keyword in the LaTeX document where the output is written

    """
    def wrapper(file_path: Path, keyword: str, *args, **kwargs):
        output = func(*args, **kwargs)  # Get the function output
        file_path = Path(file_path)

        # Read the LaTeX file and modify its content
        modified_lines = []
        skip_next_line = False
        with file_path.open('r') as file:
            for line in file:
                # Removed the line below the keyword
                if skip_next_line:
                    skip_next_line = False
                    continue
                # Append every line to the new file
                modified_lines.append(line)
                # If the keyword, append a new line
                if keyword in line:  # Match the keyword
                    skip_next_line = True
                    modified_lines.append(output + '\n')  # Insert the function output after it


        # Write the updated content back to the file
        file_path.write_text(''.join(modified_lines))
        print(f"Output from '{func.__name__}' written to '{file_path}'")

    return wrapper


if __name__ == '__main__':

    @write_to_latex
    def get_output():
        return 'Hello, World!'

    help(write_to_latex)




