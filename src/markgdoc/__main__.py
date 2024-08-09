# import markgdoc.markgdoc as markgdoc

def main():
    # Rename this variable (md_example) to the appropriate markdown file you would like to refer to from the "../src/markgdoc/example_markdown_files/" folder
    md_example = "md_ex1.md"
    md_inputfile = f"../src/markgdoc/example_markdown_files/{md_example}.md"

    # Read the content of the markdown file
    with open(md_inputfile, 'r') as file:
        md_content = file.read()
        print(md_content)

    # markgdoc.generate_google_docs()


if __name__ == "__main__":
    main()