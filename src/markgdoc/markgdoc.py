import re
import threading
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Markdown Syntax Notes: https://www.markdownguide.org/basic-syntax/

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
        print(f"Applying Header Request: \n- Level {level}\n- Text: {text}\n- Index: {index} - {index+len(text)+1}\n")
    
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
        print(f"Applying Paragraph Request:\n- Text: {text}\n- Index: {index} - {index+len(text)+1}\n")
    
    return {"insertText": {"location": {"index": index}, "text": text + "\n"}}


def get_horizontal_line_request(index, debug=False):
    """
    This returns a Google Doc API Request for a Markdown Horizontal Line Syntax.
 
    - Input: Index to place in the GDoc
    - Output: GDoc Request for Horizontal Line Syntax
    """

    if(debug):
        print(f"Applying Horizontal Line Request:\n- Index: {index} - {index + 1}\n")

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


def get_hyperlink_request(text, url, index, debug=False):
    """
    This returns a Google Doc API Request for applying a hyperlink to text.
    
    - Input: Text to be linked, URL of the hyperlink, Index to place in the GDoc
    - Output: GDoc Request for the hyperlink
    """
    if debug:
        print(f"Applying Hyperlink Request:\n- Text: {text}\n- URL: {url}\n- Index: {index} - {index + len(text) + 1}\n")

    hyperlink_request = {
            "updateTextStyle": {
                "range": {"startIndex": index, "endIndex": index + len(text)},
                "textStyle": {"link": {"url": url}},
                "fields": "link",
            }
        }

    reset_request = {
        "updateTextStyle": {
            "range": {"startIndex": index + len(text), "endIndex": (index + len(text)) + 1},
            "textStyle": {},
            "fields": "*",
        }
    }

    return [hyperlink_request, reset_request]


def get_unordered_list_request(text, index, debug=False):
    """
    This returns a Google Doc API Request for a Markdown unordered list syntax
 
    - Input: Text, Index to place in the GDoc
    - Output: GDoc Request for Unordered List Syntax
    """

    if(debug): 
        print(f"Applying Unordered-list Request:\n- Text: {text}\n- Index: {index} - {index+len(text)+1}\n")

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
        print(f"Applying Ordered-list Request:\n- Text: {text}\n- Index: {index} - {index+len(text)+1}\n")

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

            received_styles, cleaned_cell = preprocess_nested_styles(cell, index, False)
            style_requests.extend(received_styles)

            if(debug): 
                print(f"Inserting content: {cleaned_cell} at Index: {index}")
            
            request = {
                "insertText": {"location": {"index": index}, "text": cleaned_cell}
            }

            table_requests.append(request)

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
# Google Doc Creation Helper Functions ====================================================================================
def authenticate_google_drive(credentials_file, scopes):
    """
    Authentication of Google Drive for Google Doc Creation\
    Simply make sure you pass the path to your credentials file and scopes of what you aim to use it for
    """

    creds = service_account.Credentials.from_service_account_file(
        credentials_file, scopes=scopes
    )
    return build("drive", "v3", credentials=creds)


def create_empty_google_doc(document_title, credentials_file, scopes):
    """
    This helper function can be used to create an empty google docs
    Simply make sure you pass the path to your credentials file and scopes of what you aim to use it for
    """
    drive_service = authenticate_google_drive(credentials_file, scopes)
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


def preprocess_nested_styles(chunk, index, paragraph_flag, debug=False):
    """
    This is a helper function that deals with nested markdown syntax. 
    Since you can have multiple markdown syntax in a chunk of text, 
    we first preprocess the ones that don't rely on text insertion such as 
    styling (bold, italics, strikethrough), hyperlinks, blockquotes. 

    This function inputs the chunk of text, the index, and whether the chunk 
    is a paragraph or not (as well as optional debugging).
    This function outputs the stored style_requests and the cleaned-up chunk.
    """
    style_requests = []

    # Now, detect all other styles and hyperlinks in the main chunk
    matches = []
    
    bolditalics_match = re.search(r"\*\*\_(.+?)\_\*\*", chunk) or re.search(r"\_\*\*(.+?)\*\*\_", chunk)
    bold_match = re.search(r"\*\*(.+?)\*\*", chunk)
    italic_match = re.search(r"\_(.+?)\_", chunk)
    strike_match = re.search(r"\~(.+?)\~", chunk)
    hyperlink_match = re.search(r"\[(.+?)\]\((http[s]?:\/\/.+?)\)", chunk)

    if bolditalics_match:
        matches.append(("bolditalics", bolditalics_match))

    elif bold_match:
        matches.append(("bold", bold_match))
    
    elif italic_match:
        matches.append(("italic", italic_match))
    
    if strike_match:
        matches.append(("strike", strike_match))
    
    if hyperlink_match:
        matches.append(("hyperlink", hyperlink_match))

    # Sort matches by their starting index
    matches.sort(key=lambda x: x[1].start())

    # Offset to track the difference between original and modified chunk
    offset = 0

    # Process matches in order
    for match_type, match in matches:
        original_start_idx = match.start() + offset
        original_end_idx = match.end() + offset

        # Update the start index based on the modified chunk
        if match_type == "bolditalics":
            text = match.group(1).strip()
            start_idx = original_start_idx if paragraph_flag else 0
            style_requests.append(get_style_request(text, "bold", index + start_idx, debug=debug))
            style_requests.append(get_style_request(text, "italic", index + start_idx, debug=debug))
            chunk = chunk[:original_start_idx] + text + chunk[original_end_idx:]
        
        elif match_type == "bold":
            text = match.group(1).strip()
            start_idx = original_start_idx if paragraph_flag else 0
            style_requests.append(get_style_request(text, "bold", index + start_idx, debug=debug))
            chunk = chunk[:original_start_idx] + text + chunk[original_end_idx:]
        
        elif match_type == "italic":
            text = match.group(1).strip()
            start_idx = original_start_idx if paragraph_flag else 0
            style_requests.append(get_style_request(text, "italic", index + start_idx, debug=debug))
            chunk = chunk[:original_start_idx] + text + chunk[original_end_idx:]
        
        elif match_type == "strike":
            text = match.group(1).strip()
            start_idx = original_start_idx if paragraph_flag else 0 
            style_requests.append(get_style_request(text, "strike", index + start_idx, debug=debug))
            chunk = chunk[:original_start_idx] + text + chunk[original_end_idx:]
        
        elif match_type == "hyperlink":
            text = match.group(1).strip()  
            url = match.group(2).strip()
            start_idx = original_start_idx if paragraph_flag else 0
            style_requests.append(get_hyperlink_request(text, url, index + start_idx, debug=debug))
            chunk = chunk[:original_start_idx] + text + chunk[original_end_idx:]

        # Adjust the offset based on the length difference between the original match and the new text
        offset -= (len(match.group(0)) - len(text))

    cleaned_chunk = chunk
    return style_requests, cleaned_chunk


def preprocess_markdown_table(markdown_table):
    """
    This is a helper function which converts a markdown table string input into a 2D vector list
    Simply input the markdown table as a string into the function, it will output the 2D vector. 
    """
    lines = markdown_table.strip().split("\n")
    table_data = []
    for i, line in enumerate(lines):
        if i == 1:
            continue  # Skip the second row with dashes
        row = [cell.strip() for cell in line.split("|")[1:-1]]
        table_data.append(row)
    return table_data


def preprocess_numbered_lists(content):
    """
    This is a helper function which pre processes numbered lists. In markdown syntax if there is a gap
    between numbered items, they will appear as a single cohesive numbered list. But in Google Docs, they will be recognized
    as several new numbered lists. Hence, we preprocess them to remove these gaps ("") to make sure they are requested as a
    cohesive single numbered list
    """
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


def is_paragraph(chunk):
    """
    Checks if the chunk of text is an ordinary paragraph, meaning it doesn't match any special markdown syntax.
    """
    # Matches for different markdown syntax
    if (
        not re.match(r"^(#{1,6})\s+(.+)", chunk) and  # Not a header
        not re.match(r"^-\s+(.+)", chunk) and         # Not a bullet point
        not re.match(r"^\d+\.\s+(.+)", chunk) and     # Not a numbered list
        not re.match(r"^\|.+\|", chunk) and           # Not a table row
        not re.match(r"^[-*_]{3,}$", chunk)           # Not a horizontal line
    ):
        return True
    return False

def send_batch_update(docs_service, doc_id, requests, rate_limit=120):
    """
    This is a helper function to send all the requests attained to the docs_service build. 
    This will request the API to update all the requests gathered into the Google Docs with the 
    appropriate Doc ID. 

    This function inputs the docs_service build, the doc_id, the requests list and an optional rate_limit
    The rate limit determines how much content you want to send in one batch. 
    """
    batch_size = rate_limit
    for i in range(0, len(requests), batch_size):
        batch_requests = requests[i : i + batch_size]
        docs_service.documents().batchUpdate(
            documentId=doc_id, body={"requests": batch_requests}
        ).execute()


def process_markdown_content(docs_service, doc_id, content_markdown, debug=False):
    """
    This is a helper function which splits your entire markdown content into chunks to be processed individually,
    scanning them for any markdown syntax that may be found. Depending on the markdown syntax found, the appropriate 
    request will be made and appended to the requests list. Eventually to be updated onto the Google Docs. 
    """

    # First preprocess numbered lists, then split the content into chunks every new line detected. 
    content_markdown = preprocess_numbered_lists(content_markdown)
    chunks = re.split(r"(?<=\n)", content_markdown)

    # Initializing variables, index = 1
    chunks = iter(chunks)
    index = 1
    text_requests = []
    style_requests = []

    # For each chunk detected: 
    for chunk in chunks:
        # Initialize a chunk by stripping it and splitting into requests per chunk
        chunk = chunk.strip()
        requests = []
        table_flag = False
        paragraph_flag = is_paragraph(chunk)

        # Then we preprocess any styles recognized in the chunks and store them into the style_requests
        received_styling, cleaned_chunk = preprocess_nested_styles(chunk, index, paragraph_flag, debug=debug)
        style_requests.extend(received_styling)

        # Matches detected 
        header_match = re.match(r"^(#{1,6})\s+(.+)", cleaned_chunk)
        bullet_point_match = re.match(r"^-\s+(.+)", cleaned_chunk)
        numbered_list_match = re.match(r"^\d+\.\s+(.+)", cleaned_chunk)
        table_match = re.match(r"^\|.+\|", cleaned_chunk)
        horizontal_line_match = re.match(r"^[-*_]{3,}$", cleaned_chunk)
        
        # If the chunk has header markdown syntax add the request
        if header_match:
            header_level = len(re.match(r"^#+", cleaned_chunk).group(0))
            text = cleaned_chunk[header_level:].strip()
            requests.extend(get_header_request(text, header_level, index, debug=debug))
        
        # If the chunk has unordered list markdown syntax add the request
        elif bullet_point_match:
            text = cleaned_chunk[2:].strip()
            requests.extend(get_unordered_list_request(text, index, debug=debug))

        # If the chunk has ordered list markdown syntax add the request
        elif numbered_list_match:
            text = re.sub(r"^\d+\.\s", "", cleaned_chunk).strip()
            requests.extend(get_ordered_list_request(text, index, debug=debug))
        
        # If the chunk has horizontal line markdown syntax add the request
        elif horizontal_line_match:
            requests.extend(get_horizontal_line_request(index, debug=debug))

        # If the chunk has table markdown syntax add the request
        elif table_match:
            table_flag = True

            # If it's a table, first process everything already there in all_requests, then clear it
            send_batch_update(docs_service, doc_id, text_requests)
            text_requests.clear()

            # Split the table into a list of table lines
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
            
            # Create a 2D List of the table 
            table_data = preprocess_markdown_table("\n".join(table_lines))

            # Send a request to create an empty table in the google doc
            table_rows = len(table_data)
            table_columns = len(table_data[0])
            table_request = get_empty_table_request(table_rows, table_columns, index, debug=debug)

            # Send the request immediately 
            docs_service.documents().batchUpdate(
                documentId=doc_id, body={"requests": table_request}
            ).execute()

            # In the google doc, find the table and retrieve its starting index
            content = (
                docs_service.documents()
                .get(documentId=doc_id, fields="body")
                .execute()
                .get("body")
                .get("content")
            )
            tables = [c for c in content if c.get("table")]
            table_start_index = tables[-1]["startIndex"]
            
            # Insert the contents of the table into the empty table 
            table_content_requests, table_style_requests, table_end_index = get_table_content_request(
                table_data, table_start_index, debug=debug
            )

            #  Append the style requests of the table contents and update index accordingly
            requests.extend(table_content_requests) 
            style_requests.extend(table_style_requests)
            index = table_end_index
            requests.append(get_paragraph_request("\n", index, debug=debug))
            index += 2 # Update index to account for paragraph since it's not being accounted for due to table_flag

        # If the chunk has none of those, then it is likely a paragraph
        else:
            requests.append(get_paragraph_request(cleaned_chunk, index, debug=debug))
        
        #  Append the general requets into the all requests and then appropriately increment the index based on the request text
        for request in requests:
            text_requests.append(request)
            # Table automatically updates index due to monitoring hence, no need to update index if it's a table
            if "insertText" in request and not table_flag:
                index += len(request["insertText"]["text"])

    # Send batch updates to insert the text into the google doc
    send_batch_update(docs_service, doc_id, text_requests)
    
    # After inserting the text, send a separate batch update for style requests
    send_batch_update(docs_service, doc_id, style_requests)


def convert_to_google_docs(content_markdown, document_title, docs_service, credentials_file, scopes, debug=False):
    doc_id, doc_url = create_empty_google_doc(document_title, credentials_file, scopes)

    if debug: 
        print(f"Google Doc Link: {doc_url}\n")
    
    def stream_content():
        process_markdown_content(docs_service, doc_id, content_markdown, debug=debug)

    content_thread = threading.Thread(target=stream_content)
    content_thread.start()
    
    if debug:
        content_thread.join()
    
    return doc_url
    