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
# 1) Styling - No need to call reset function after, find a way to fuse the two 
# 2) Table Content - See what i_cell, i_row do and if not needed remove
# 3) Block Quotes (>) Syntax basically is indentations so need to add this
# 4) Links - Need to work on creating a hyperlink syntax on Google Docs

# Google Docs API Request Functions ===================================================================================
def get_header_request(text, level, index):
    """
    This returns a Google Doc API Request for a Markdown Header Syntax. 
    Header Levels: (# Header 1, ## Header 2, ### Header 3, ### Header 4, ##### Header 5, ###### Header 6)

    - Input: Text, Header Level, Index to place in the GDoc
    - Output: GDoc Request for Header Syntax
    """

    # print(f"Applying Header formats: Level {level}, Text: {text} at Index: {index}")
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


def get_paragraph_request(text, index):
    """
    This returns a Google Doc API Request for a Markdown Paragraph Syntax. 

    - Input: Text, Index to place in the GDoc
    - Output: GDoc Request for Paragraph Syntax
    """
    # print(f"Applying Paragraph formats: Text: {text} at Index: {index}")
    return {"insertText": {"location": {"index": index}, "text": text + "\n"}}


def get_horizontal_line_request(index):
    """
    This returns a Google Doc API Request for a Markdown Horizontal Line Syntax.
 
    - Input: Index to place in the GDoc
    - Output: GDoc Request for Horizontal Line Syntax
    """
    # print(f"Applying Horizontal Line format at Index: {index}")
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


def get_blockquote_request(text, frequency, index):
    """
    This returns a Google Doc API Request for applying an indentation on text at a particular index in the GDoc
 
    - Input: Text, Frequency of indentation (how many times), Index to place in the GDoc
    - Output: GDoc Request for Indenting the text
    """


def get_style_request(text, style, index):
    """
    This returns a Google Doc API Request for applying some styling for the entire text index
    Styling Examples: Bolding (**), Italics (_), Bolding + Italics (**_ or_**), Strikethrough (~)
 
    - Input: Text, Styling, Index to place in the GDoc
    - Output: GDoc Request for Styling Syntax
    """
    # print(f"Applying Style formats: {style}, Text: {text} at Index: {index}")
    style_mapping = {
        "bold": {"bold": True},
        "italic": {"italic": True},
        "strike": {"strike": True}
    }
    return {
        "updateTextStyle": {
            "range": {"startIndex": index, "endIndex": index + len(text)},
            "textStyle": style_mapping[style],
            "fields": style,
        }
    }

# Need to test putting this request after the get style request so no need for two functions just one universal one
def get_reset_text_style_request(index):
    """
    This request should be called after a styling call is done to switch off the styling option
 
    - Input: Latest Index after a styled text
    - Output: GDoc Request for switching off Styling
    """
    return {
        "updateTextStyle": {
            "range": {"startIndex": index, "endIndex": index + 1},
            "textStyle": {},
            "fields": "*",
        }
    }


def get_unordered_list_request(text, index):
    """
    This returns a Google Doc API Request for a Markdown unordered list syntax
 
    - Input: Text, Index to place in the GDoc
    - Output: GDoc Request for Unordered List Syntax
    """
    # print(f"Applying Unordered-list formats: Text: {text} at Index: {index}")
    return {"insertText": {"location": {"index": index}, "text": text + "\n"}}, {
        "createParagraphBullets": {
            "range": {"startIndex": index, "endIndex": index + len(text) + 1},
            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
        }
    }


def get_ordered_list_request(text, index):
    """
    This returns a Google Doc API Request for a Markdown ordered list syntax
 
    - Input: Text, Index to place in the GDoc
    - Output: GDoc Request for Ordered List Syntax
    """
    # print(f"Applying Ordered-list formats: Text: {text} at Index: {index}")
    return (
        {"insertText": {"location": {"index": index}, "text": text + "\n"}},
        {
            "createParagraphBullets": {
                "range": {"startIndex": index, "endIndex": index + len(text) + 1},
                "bulletPreset": "NUMBERED_DECIMAL_NESTED",
            }
        },
    )


def get_empty_table_request(rows, cols, index):
    """
    This returns a Google Doc API Request to create an empty table from Markdown syntax to Google Docs
 
    - Input: Number of Rows, Columns and Index to place the empty table in the GDoc
    - Output: GDoc Request for Empty Table Creation in GDoc
    """
    # print(f"Creating a table of {rows} Rows and {cols} Columns at Index: {index}")
    table_request = {
        "insertTable": {"rows": rows, "columns": cols, "location": {"index": index}}
    }
    return table_request


# Need to see what this i_cell and i_row does... beacuse it is unused
def get_table_content_request(table_data, index):
    """
    This returns a Google Doc API Request to populate the contents of the table inside an existing empty table in the GDoc
    This includes styling implemented within the table so no need to explicitly call it when this is called
 
    - Input: Table Data: 2D List of the [Rows][Cols], index of the start of the table
    - Output: Content Insertion Requests for each cell, Styling Requests for each cell, Table ending index
    """
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

            # print("Start Index: ", index)

            received_styles, cleaned_cell = clean_and_capture_styles(cell, index)
            style_requests.extend(received_styles)

            # print(f"Inserting in cell index {index}, content: {cleaned_cell}")
            table_requests = {
                "insertText": {"location": {"index": index}, "text": cleaned_cell}
            }

            # print("Content: ", cleaned_cell)
            # print("Length of Cell: ", len(cleaned_cell) + 1)

            # Accounting for newline character
            index += len(cleaned_cell) + 1
            # print(f"End Index: {index}\n")

    table_end_index = index + 1

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
def clean_and_capture_styles(chunk, index):
    requests = []
    bolditalics_match = re.search(r"\*\*\*(.+?)\*\*\*", chunk)
    bold_match = re.search(r"\*\*(.+?)\*\*", chunk)
    italic_match = re.search(r"\_(.+?)\_", chunk)
    strike_match = re.search(r"\~(.+?)\~", chunk)

    if bolditalics_match:
        text = bolditalics_match.group(1).strip()
        requests.append(get_style_request(text, "bold", index))
        requests.append(get_style_request(text, "italic", index))
        chunk = re.sub(r"\*\*\*(.+?)\*\*\*", text, chunk)

    elif bold_match:
        text = bold_match.group(1).strip()
        requests.append(get_style_request(text, "bold", index))
        chunk = re.sub(r"\*\*(.+?)\*\*", text, chunk)

    elif italic_match:
        text = italic_match.group(1).strip()
        requests.append(get_style_request(text, "italic", index))
        chunk = re.sub(r"\_(.+?)\_", text, chunk)

    if strike_match:
        text = strike_match.group(1).strip()
        requests.append(get_style_request(text, "underline", index))
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
def update_google_doc_content(doc_id, docs_service, content_markdown):
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
        received_styling, cleaned_chunk = clean_and_capture_styles(chunk, index)
        style_requests.extend(received_styling)

        header_match = re.match(r"^(#{1,6})\s+(.+)", cleaned_chunk)
        bullet_point_match = re.match(r"^-\s+(.+)", cleaned_chunk)
        numbered_list_match = re.match(r"^\d+\.\s+(.+)", cleaned_chunk)
        table_match = re.match(r"^\|.+\|", cleaned_chunk)

        if header_match:
            header_level = len(re.match(r"^#+", cleaned_chunk).group(0))
            text = cleaned_chunk[header_level:].strip()
            requests.extend(get_header_request(header_level, text, index))
        elif bullet_point_match:
            text = cleaned_chunk[2:].strip()
            requests.extend(get_unordered_list_request(text, index))
        elif numbered_list_match:
            text = re.sub(r"^\d+\.\s", "", cleaned_chunk).strip()
            requests.extend(get_ordered_list_request(text, index))
        elif cleaned_chunk == "---":
            requests.extend(get_horizontal_line_request(index))
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
            table_request = get_empty_table_request(table_data, index)

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
            received_styles, table_end_index = get_table_content_request(
                table_data, table_start_index, docs_service, doc_id
            )
            style_requests.extend(received_styles)
            index = table_end_index
            requests.append(get_paragraph_request("\n", index))
        else:
            requests.append(get_paragraph_request(cleaned_chunk, index))

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

        all_requests.append(get_reset_text_style_request(index))

    rate_limited_batch_update(docs_service, doc_id, all_requests)


def convert_to_google_docs(content_in_bytes, document_title, docs_service):
    start = time.time()
    doc_id, doc_url = create_empty_google_doc(document_title)
    end = time.time()

    def stream_content():
        content_markdown = content_in_bytes.getvalue().decode("utf-8")
        update_google_doc_content(doc_id, docs_service, content_markdown)

    threading.Thread(target=stream_content).start()

    print(f"Elapsed Time = {end-start} seconds")
    return doc_url