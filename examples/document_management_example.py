#!/usr/bin/env python3
"""
Document Management Example for MarkGDoc

This example demonstrates the new document management features:
- Creating documents in specific folders
- Using existing documents instead of creating new ones
- Clearing existing document content
- Advanced configuration options
"""

from src.markgdoc.markgdoc import convert_to_google_docs, authenticate_google_docs

# Example markdown content
MARKDOWN_CONTENT = """
# Document Management Demo

This document demonstrates the new **document management** features of MarkGDoc.

## Features Demonstrated

### 📁 Folder Management
- Automatically create folders if they don't exist
- Organize documents in specific folders
- Support for nested folder structures

### 📄 Document Handling
- Use existing documents instead of always creating new ones
- Clear existing content while preserving document properties
- Flexible permission management

### ✨ Enhanced Formatting
- **Bold text** and *italic text* support
- Multiple markdown patterns: __bold__, _italic_, ***bold-italic***
- Extended bullet point support:
  - Standard bullets with -
  • Unicode bullets with •
  – En dash bullets with –
  — Em dash bullets with —

### 🎯 Usage Examples

1. **Create in specific folder:**
   ```python
   result = convert_to_google_docs(
       content, "My Document", docs_service, creds, scopes,
       folder_name="Project Documents"
   )
   ```

2. **Use existing document:**
   ```python
   result = convert_to_google_docs(
       content, "Existing Doc", docs_service, creds, scopes,
       use_existing=True, clear_existing=True
   )
   ```

3. **Private document (no public permissions):**
   ```python
   result = convert_to_google_docs(
       content, "Private Doc", docs_service, creds, scopes,
       set_public_permissions=False
   )
   ```

## Benefits

✅ **Organized**: Keep documents organized in folders
✅ **Efficient**: Reuse existing documents instead of creating duplicates
✅ **Flexible**: Control permissions and document behavior
✅ **Robust**: Enhanced error handling and edge cases

---
*Generated using MarkGDoc with enhanced document management features*
"""

def example_basic_usage():
    """Example of basic usage with new features"""
    
    # Configuration
    CREDENTIALS_FILE = "path/to/your/credentials.json"
    SCOPES = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/documents"
    ]
    
    # Authenticate Google Docs service
    docs_service = authenticate_google_docs(CREDENTIALS_FILE, SCOPES)
    
    # Example 1: Create document in a specific folder
    print("Example 1: Creating document in 'MarkGDoc Examples' folder...")
    result1 = convert_to_google_docs(
        MARKDOWN_CONTENT,
        "Document Management Demo",
        docs_service,
        CREDENTIALS_FILE,
        SCOPES,
        folder_name="MarkGDoc Examples",
        debug=True
    )
    
    print(f"✅ Document created: {result1['doc_url']}")
    print(f"   - Document ID: {result1['doc_id']}")
    print(f"   - Was existing: {result1['was_existing']}")
    print(f"   - Folder: {result1['folder_info']}")
    
    # Example 2: Use existing document (if found)
    print("\nExample 2: Using existing document (if found)...")
    result2 = convert_to_google_docs(
        "# Updated Content\n\nThis content replaces the previous content.",
        "Document Management Demo",  # Same name as above
        docs_service,
        CREDENTIALS_FILE,
        SCOPES,
        folder_name="MarkGDoc Examples",
        use_existing=True,
        clear_existing=True,
        debug=True
    )
    
    print(f"✅ Document updated: {result2['doc_url']}")
    print(f"   - Was existing: {result2['was_existing']}")
    
    # Example 3: Create private document (no public permissions)
    print("\nExample 3: Creating private document...")
    result3 = convert_to_google_docs(
        "# Private Document\n\nThis document has restricted permissions.",
        "Private Demo Document",
        docs_service,
        CREDENTIALS_FILE,
        SCOPES,
        folder_name="Private Documents",
        set_public_permissions=False,
        debug=True
    )
    
    print(f"✅ Private document created: {result3['doc_url']}")
    print(f"   - Public permissions: False")

def example_advanced_configuration():
    """Example showing all configuration options"""
    
    CREDENTIALS_FILE = "path/to/your/credentials.json"
    SCOPES = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/documents"
    ]
    
    docs_service = authenticate_google_docs(CREDENTIALS_FILE, SCOPES)
    
    # All configuration options
    result = convert_to_google_docs(
        content_markdown=MARKDOWN_CONTENT,
        document_title="Full Configuration Example",
        docs_service=docs_service,
        credentials_file=CREDENTIALS_FILE,
        scopes=SCOPES,
        folder_name="Advanced Examples",          # Create/use this folder
        use_existing=True,                        # Use existing if found
        clear_existing=True,                      # Clear existing content
        set_public_permissions=True,              # Set public write permissions
        debug=True                               # Enable debug output
    )
    
    print("Advanced Configuration Result:")
    print(f"  URL: {result['doc_url']}")
    print(f"  ID: {result['doc_id']}")
    print(f"  Was Existing: {result['was_existing']}")
    print(f"  Folder: {result['folder_info']}")

if __name__ == "__main__":
    print("MarkGDoc Document Management Examples")
    print("=" * 50)
    print()
    print("⚠️  Note: Update CREDENTIALS_FILE path before running!")
    print()
    
    # Uncomment the example you want to run:
    
    # example_basic_usage()
    # example_advanced_configuration()
    
    print("Examples completed! 🎉")
    print()
    print("New Features Summary:")
    print("✅ Folder-based organization")
    print("✅ Existing document reuse")
    print("✅ Content clearing")
    print("✅ Permission control")
    print("✅ Enhanced markdown support")
    print("✅ Comprehensive testing")
