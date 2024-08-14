import pytest
from src.markgdoc.markgdoc import (
    get_header_request, 
    get_paragraph_request, 
    get_horizontal_line_request,  
    get_style_request, 
    get_hyperlink_request, 
    get_unordered_list_request, 
    get_ordered_list_request, 
    get_empty_table_request, 
    get_table_content_request
)


# Example test data for testing purposes
@pytest.mark.parametrize("text, level, index, expected", [
    ("Header 1", 1, 0, (
        {"insertText": {"location": {"index": 0}, "text": "Header 1\n"}},
        {
            "updateParagraphStyle": {
                "range": {"startIndex": 0, "endIndex": 9},
                "paragraphStyle": {"namedStyleType": "HEADING_1"},
                "fields": "namedStyleType",
            }
        }
    )),
])
def test_get_header_request(text, level, index, expected):
    result = get_header_request(text, level, index)
    assert result == expected


@pytest.mark.parametrize("text, index, expected", [
    ("This is a paragraph.", 5, {"insertText": {"location": {"index": 5}, "text": "This is a paragraph.\n"}}),
])
def test_get_paragraph_request(text, index, expected):
    result = get_paragraph_request(text, index)
    assert result == expected


@pytest.mark.parametrize("index, expected", [
    (10, (
        {"insertText": {"location": {"index": 10}, "text": "\n"}},
        {
            "updateParagraphStyle": {
                "range": {"startIndex": 10, "endIndex": 11},
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
    )),
])
def test_get_horizontal_line_request(index, expected):
    result = get_horizontal_line_request(index)
    assert result == expected


@pytest.mark.parametrize("text, style, index, expected", [
    ("Bold Text", "bold", 8, [
        {
            "updateTextStyle": {
                "range": {"startIndex": 8, "endIndex": 17},
                "textStyle": {"bold": True},
                "fields": "bold",
            }
        },
        {
            "updateTextStyle": {
                "range": {"startIndex": 17, "endIndex": 18},
                "textStyle": {},
                "fields": "*",
            }
        }
    ]),
])
def test_get_style_request(text, style, index, expected):
    result = get_style_request(text, style, index)
    assert result == expected


@pytest.mark.parametrize("text, url, index, expected", [
    ("Link Text", "http://example.com", 20, [
        {
            "updateTextStyle": {
                "range": {"startIndex": 20, "endIndex": 29},
                "textStyle": {"link": {"url": "http://example.com"}},
                "fields": "link",
            }
        },
        {
            "updateTextStyle": {
                "range": {"startIndex": 29, "endIndex": 30},
                "textStyle": {},
                "fields": "*",
            }
        }
    ]),
])
def test_get_hyperlink_request(text, url, index, expected):
    result = get_hyperlink_request(text, url, index)
    assert result == expected


@pytest.mark.parametrize("text, index, expected", [
    ("Unordered list item", 12, (
        {"insertText": {"location": {"index": 12}, "text": "Unordered list item\n"}},
        {
            "createParagraphBullets": {
                "range": {"startIndex": 12, "endIndex": 32},
                "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
            }
        }
    )),
])
def test_get_unordered_list_request(text, index, expected):
    result = get_unordered_list_request(text, index)
    assert result == expected


@pytest.mark.parametrize("text, index, expected", [
    ("Ordered list item", 7, (
        {"insertText": {"location": {"index": 7}, "text": "Ordered list item\n"}},
        {
            "createParagraphBullets": {
                "range": {"startIndex": 7, "endIndex": 25},
                "bulletPreset": "NUMBERED_DECIMAL_NESTED",
            }
        }
    )),
])
def test_get_ordered_list_request(text, index, expected):
    result = get_ordered_list_request(text, index)
    assert result == expected


@pytest.mark.parametrize("rows, cols, index, expected", [
    (3, 3, 5, {
        "insertTable": {"rows": 3, "columns": 3, "location": {"index": 5}}
    }),
])
def test_get_empty_table_request(rows, cols, index, expected):
    result = get_empty_table_request(rows, cols, index)
    assert result == expected


@pytest.mark.parametrize("table_data, index, expected_requests_length, expected_style_requests_length, expected_table_end_index", [
    ([["A1", "B1", "C1"], ["A2", "B2", "C2"], ["A3", "B3", "C3"]], 10, 9, 0, 51),
])
def test_get_table_content_request(table_data, index, expected_requests_length, expected_style_requests_length, expected_table_end_index):
    requests, style_requests, table_end_index = get_table_content_request(table_data, index)
    assert len(requests) == expected_requests_length
    assert len(style_requests) == expected_style_requests_length
    assert table_end_index == expected_table_end_index
