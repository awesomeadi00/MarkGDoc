# import markgdoc.markgdoc as markgdoc

def main():
    md_example = "md_ex1.md"
    md_inputfile = f"../src/markgdoc/example_markdown_files/{md_example}.md"
    
    # Read the content of the markdown file
    with open(md_inputfile, 'r') as file:
        md_content = file.read()
        print(md_content)

    # markgdoc.generate_google_docs()


if __name__ == "__main__":
    main()