import re
import threading
from google.oauth2 import service_account
from googleapiclient.discovery import build
import time

# Markdown Syntax Notes: https://www.markdownguide.org/basic-syntax/

# Path to the service account key file
SERVICE_ACCOUNT_FILE = "credentials.json"
SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
]


# Requests Need Fixing: 
# 2) Table Content - See what i_cell, i_row do and if not needed remove
# 3) Block Quotes (>) Syntax basically is indentations so need to add this
# 4) Links - Need to work on creating a hyperlink syntax on Google Docs

# Google Docs API Request Functions ===================================================================================
# Disclaimer! Every Request has an optional 'debug' parameter. By default this is False, however if switched on as True
# You will be able to see the request made, the content, extra parameters and the index the content is being inserted at 

def get_header_request(text, level, index, debug=False):
    """
    This returns a Google Doc API Request for a Markdown Header Syntax. 
    Header Levels: (# Header 1, ## Header 2, ### Header 3, ### Header 4, ##### Header 5, ###### Header 6)

    - Input: Text, Header Level, Index to place in the GDoc
    - Output: GDoc Request for Header Syntax
    """

    if(debug): 
        print(f"Applying Header Request: \n- Level {level}\n- Text: {text}\n- Index: {index}\n")
    
    return (
        {"insertText": {"location": {"index": index}, "text": text + "\n"}},
        {
            "updateParagraphStyle": {
                "range": {"startIndex": index, "endIndex": index + len(text) + 1},
                "paragraphStyle": {"namedStyleType": f"HEADING_{level}"},
                "fields": "namedStyleType",
            }
        },
    )


def get_paragraph_request(text, index, debug=False):
    """
    This returns a Google Doc API Request for a Markdown Paragraph Syntax. 

    - Input: Text, Index to place in the GDoc
    - Output: GDoc Request for Paragraph Syntax
    """

    if(debug):
        print(f"Applying Paragraph Request:\n- Text: {text}\n- Index: {index}\n")
    
    return {"insertText": {"location": {"index": index}, "text": text + "\n"}}


def get_horizontal_line_request(index, debug=False):
    """
    This returns a Google Doc API Request for a Markdown Horizontal Line Syntax.
 
    - Input: Index to place in the GDoc
    - Output: GDoc Request for Horizontal Line Syntax
    """

    if(debug):
        print(f"Applying Horizontal Line Request:\n- Index: {index}\n")

    return {"insertText": {"location": {"index": index}, "text": "\n"}}, {
        "updateParagraphStyle": {
            "range": {"startIndex": index, "endIndex": index + 1},
            "paragraphStyle": {
                "borderBottom": {
                    "color": {"color": {"rgbColor": {"red": 0, "green": 0, "blue": 0}}},
                    "width": {"magnitude": 1, "unit": "PT"},
                    "padding": {"magnitude": 1, "unit": "PT"},
                    "dashStyle": "SOLID",
                }
            },
            "fields": "borderBottom",
        }
    }


def get_blockquote_request(text, frequency, index, debug=False):
    """
    This returns a Google Doc API Request for applying an indentation on text at a particular index in the GDoc
 
    - Input: Text, Frequency of indentation (how many times), Index to place in the GDoc
    - Output: GDoc Request for Indenting the text
    """


def get_style_request(text, style, index, debug=False):
    """
    This returns a Google Doc API Request for applying some styling for the entire text index
    Styling Examples: Bolding (**), Italics (_), Bolding + Italics (**_ or_**), Strikethrough (~)
 
    - Input: Text, Styling, Index to place in the GDoc
    - Output: GDoc Request for Styling Syntax
    """

    if(debug):
        print(f"Applying Style Request:\n- Style: {style}\n- Text: {text}\n- Index: {index} - {index + len(text)}\n")

    style_mapping = {
        "bold": {"bold": True},
        "italic": {"italic": True},
        "strike": {"strike": True}
    }
    style_request = {
        "updateTextStyle": {
            "range": {"startIndex": index, "endIndex": index + len(text)},
            "textStyle": style_mapping[style],
            "fields": style,
        }
    }
    
    reset_request = {
        "updateTextStyle": {
            "range": {"startIndex": index + len(text), "endIndex": (index + len(text)) + 1},
            "textStyle": {},
            "fields": "*",
        }
    }
    return [style_request, reset_request]


def get_unordered_list_request(text, index, debug=False):
    """
    This returns a Google Doc API Request for a Markdown unordered list syntax
 
    - Input: Text, Index to place in the GDoc
    - Output: GDoc Request for Unordered List Syntax
    """

    if(debug): 
        print(f"Applying Unordered-list Request:\n- Text: {text}\n- Index: {index}\n")

    return {"insertText": {"location": {"index": index}, "text": text + "\n"}}, {
        "createParagraphBullets": {
            "range": {"startIndex": index, "endIndex": index + len(text) + 1},
            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
        }
    }


def get_ordered_list_request(text, index, debug=False):
    """
    This returns a Google Doc API Request for a Markdown ordered list syntax
 
    - Input: Text, Index to place in the GDoc
    - Output: GDoc Request for Ordered List Syntax
    """

    if(debug):
        print(f"Applying Ordered-list Request:\n- Text: {text}\n- Index: {index}\n")

    return (
        {"insertText": {"location": {"index": index}, "text": text + "\n"}},
        {
            "createParagraphBullets": {
                "range": {"startIndex": index, "endIndex": index + len(text) + 1},
                "bulletPreset": "NUMBERED_DECIMAL_NESTED",
            }
        },
    )


def get_empty_table_request(rows, cols, index, debug=False):
    """
    This returns a Google Doc API Request to create an empty table from Markdown syntax to Google Docs
 
    - Input: Number of Rows, Columns and Index to place the empty table in the GDoc
    - Output: GDoc Request for Empty Table Creation in GDoc
    """

    if(debug): 
        print(f"Applying Table Creation Request:\n- Created {rows} Rows and {cols} Columns\n- Index: {index}\n")

    table_request = {
        "insertTable": {"rows": rows, "columns": cols, "location": {"index": index}}
    }
    return table_request


# Need to see what this i_cell and i_row does... beacuse it is unused
def get_table_content_request(table_data, index, debug=False):
    """
    This returns a Google Doc API Request to populate the contents of the table inside an existing empty table in the GDoc
    This includes styling implemented within the table so no need to explicitly call it when this is called
 
    - Input: Table Data: 2D List of the [Rows][Cols], index of the start of the table
    - Output: Content Insertion Requests for each cell, Styling Requests for each cell, Table ending index
    """

    if(debug): 
        print("Applying Table Content Insertion Request: =========================================\n")

    table_requests = []
    style_requests = []

    # Accounting for table initiation
    index = index + 1
    for i_row, row in enumerate(table_data):
        # For each row we increment
        index += 1
        for i_cell, cell in enumerate(row):
            # For each cell we incremenet
            index += 1

            if(debug): 
                print("Start Index: ", index)

            received_styles, cleaned_cell = clean_and_capture_styles(cell, index)
            style_requests.extend(received_styles)

            if(debug): 
                print(f"Inserting content: {cleaned_cell} at Index: {index}")
            
            table_requests = {
                "insertText": {"location": {"index": index}, "text": cleaned_cell}
            }

            if(debug): 
                print("Length of Characters in cell: ", len(cleaned_cell) + 1)

            # Accounting for newline character
            index += len(cleaned_cell) + 1

            if(debug): 
                print(f"End Index: {index}\n")

    table_end_index = index + 1

    if(debug): 
        print("===================================================================================\n")

    return table_requests, style_requests, table_end_index
# ========================================================================================================================
# Google Doc Creation Testing ============================================================================================

def authenticate_google_drive():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build("drive", "v3", credentials=creds)


def create_empty_google_doc(document_title):
    drive_service = authenticate_google_drive()
    doc_metadata = {
        "name": document_title,
        "mimeType": "application/vnd.google-apps.document",
    }

    doc = drive_service.files().create(body=doc_metadata).execute()
    doc_id = doc["id"]

    # Set permissions to allow user to view and edit immediately
    permission_body = {"type": "anyone", "role": "writer"}
    drive_service.permissions().create(fileId=doc_id, body=permission_body).execute()

    doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"
    return doc_id, doc_url

# Clean markdown styling and capture style requests
def clean_and_capture_styles(chunk, index, debug=False):
    requests = []
    bolditalics_match = re.search(r"\*\*\*(.+?)\*\*\*", chunk)
    bold_match = re.search(r"\*\*(.+?)\*\*", chunk)
    italic_match = re.search(r"\_(.+?)\_", chunk)
    strike_match = re.search(r"\~(.+?)\~", chunk)

    if bolditalics_match:
        text = bolditalics_match.group(1).strip()
        requests.append(get_style_request(text, "bold", index, debug=debug))
        requests.append(get_style_request(text, "italic", index, debug=debug))
        chunk = re.sub(r"\*\*\*(.+?)\*\*\*", text, chunk)

    elif bold_match:
        text = bold_match.group(1).strip()
        requests.append(get_style_request(text, "bold", index, debug=debug))
        chunk = re.sub(r"\*\*(.+?)\*\*", text, chunk)

    elif italic_match:
        text = italic_match.group(1).strip()
        requests.append(get_style_request(text, "italic", index, debug=debug))
        chunk = re.sub(r"\_(.+?)\_", text, chunk)

    if strike_match:
        text = strike_match.group(1).strip()
        requests.append(get_style_request(text, "underline", index, debug=debug))
        chunk = re.sub(r"\~(.+?)\~", text, chunk)

    cleaned_chunk = chunk
    return requests, cleaned_chunk

def parse_markdown_table(markdown_table):
    lines = markdown_table.strip().split("\n")
    table_data = []
    for i, line in enumerate(lines):
        if i == 1:
            continue  # Skip the second row with dashes
        row = [cell.strip() for cell in line.split("|")[1:-1]]
        table_data.append(row)
    return table_data


def split_chunks(content):
    lines = content.splitlines()
    clean_lines = []
    skip_next_empty = False

    for i, line in enumerate(lines):
        if line.strip() == "" and skip_next_empty:
            continue

        if re.match(r"^\d+\.\s+(.+)", line.strip()):
            skip_next_empty = True
        else:
            skip_next_empty = False

        clean_lines.append(line)

        # Peek at the next line
        if i < len(lines) - 1:
            next_line = lines[i + 1].strip()
            if (
                line.strip() != ""
                and next_line == ""
                and re.match(r"^\d+\.\s+(.+)", lines[i + 2].strip())
            ):
                continue
            if re.match(r"^\d+\.\s+(.+)", line.strip()) and next_line == "":
                clean_lines.append("")

    return "\n".join(clean_lines)


def rate_limited_batch_update(docs_service, doc_id, requests, rate_limit=120):
    batch_size = rate_limit
    for i in range(0, len(requests), batch_size):
        batch_requests = requests[i : i + batch_size]
        docs_service.documents().batchUpdate(
            documentId=doc_id, body={"requests": batch_requests}
        ).execute()


# Update Google Doc Content with Rate Limiting
def update_google_doc_content(doc_id, docs_service, content_markdown, debug=False):
    content_markdown = split_chunks(content_markdown)
    chunks = re.split(r"(?<=\n)", content_markdown)
    chunks = iter(chunks)
    index = 1
    all_requests = []

    for chunk in chunks:
        chunk = chunk.strip()
        requests = []
        style_requests = []

        # Clean the chunk and capture style requests
        received_styling, cleaned_chunk = clean_and_capture_styles(chunk, index, debug=debug)
        style_requests.extend(received_styling)

        header_match = re.match(r"^(#{1,6})\s+(.+)", cleaned_chunk)
        bullet_point_match = re.match(r"^-\s+(.+)", cleaned_chunk)
        numbered_list_match = re.match(r"^\d+\.\s+(.+)", cleaned_chunk)
        table_match = re.match(r"^\|.+\|", cleaned_chunk)

        if header_match:
            header_level = len(re.match(r"^#+", cleaned_chunk).group(0))
            text = cleaned_chunk[header_level:].strip()
            requests.extend(get_header_request(text, header_level, index, debug=debug))
        
        elif bullet_point_match:
            text = cleaned_chunk[2:].strip()
            requests.extend(get_unordered_list_request(text, index, debug=debug))
        
        elif numbered_list_match:
            text = re.sub(r"^\d+\.\s", "", cleaned_chunk).strip()
            requests.extend(get_ordered_list_request(text, index, debug=debug))
        
        elif cleaned_chunk == "---":
            requests.extend(get_horizontal_line_request(index, debug=debug))
        
        elif table_match:
            # If it's a table, first process everything already there in all_requests, then clear it
            rate_limited_batch_update(docs_service, doc_id, all_requests)
            all_requests.clear()

            table_lines = [chunk]
            while True:
                try:
                    next_chunk = next(chunks).strip()
                    if re.match(r"^\|.+\|", next_chunk):
                        table_lines.append(next_chunk)
                    else:
                        break
                except StopIteration:
                    break

            table_data = parse_markdown_table("\n".join(table_lines))
            table_rows = len(table_data)
            table_columns = len(table_data[0])
            table_request = get_empty_table_request(table_rows, table_columns, index, debug=debug)

            docs_service.documents().batchUpdate(
                documentId=doc_id, body={"requests": table_request}
            ).execute()

            content = (
                docs_service.documents()
                .get(documentId=doc_id, fields="body")
                .execute()
                .get("body")
                .get("content")
            )
            tables = [c for c in content if c.get("table")]
            table_start_index = tables[-1]["startIndex"]
            table_content_requests, received_styles, table_end_index = get_table_content_request(
                table_data, table_start_index, debug=debug
            )
            requests.extend(table_content_requests)
            style_requests.extend(received_styles)
            index = table_end_index
            requests.append(get_paragraph_request("\n", index, debug=debug))
        else:
            requests.append(get_paragraph_request(cleaned_chunk, index, debug=debug))

        for req_tuple in requests:
            if isinstance(req_tuple, tuple):
                for req in req_tuple:
                    all_requests.append(req)
                    if "insertText" in req:
                        index += len(req["insertText"]["text"])
            else:
                all_requests.append(req_tuple)
                if "insertText" in req_tuple:
                    index += len(req_tuple["insertText"]["text"])

        for req in style_requests:
            all_requests.append(req)

    rate_limited_batch_update(docs_service, doc_id, all_requests)


def convert_to_google_docs(content_markdown, document_title, docs_service, debug=False):
    start = time.time()
    doc_id, doc_url = create_empty_google_doc(document_title)
    end = time.time()

    def stream_content():
        update_google_doc_content(doc_id, docs_service, content_markdown, debug=debug)

    threading.Thread(target=stream_content).start()

    print(f"Elapsed Time = {end-start} seconds")
    return doc_url
    