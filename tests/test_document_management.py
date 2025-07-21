import pytest
from unittest.mock import Mock, patch, MagicMock
from src.markgdoc.markgdoc import (
    authenticate_google_docs,
    find_or_create_folder,
    get_existing_document_id,
    clear_document_content,
    create_empty_google_doc,
    get_or_create_document,
    convert_to_google_docs
)


class TestDocumentManagement:
    
    @patch('src.markgdoc.markgdoc.build')
    @patch('src.markgdoc.markgdoc.service_account.Credentials.from_service_account_file')
    def test_authenticate_google_docs(self, mock_creds, mock_build):
        """Test Google Docs API authentication"""
        mock_creds.return_value = Mock()
        mock_build.return_value = Mock()
        
        result = authenticate_google_docs("test_creds.json", ["scope1"])
        
        mock_creds.assert_called_once_with("test_creds.json", scopes=["scope1"])
        mock_build.assert_called_once_with("docs", "v1", credentials=mock_creds.return_value)
        assert result == mock_build.return_value

    def test_find_or_create_folder_existing(self):
        """Test finding existing folder"""
        mock_drive_service = Mock()
        mock_list_result = Mock()
        mock_list_result.execute.return_value = {
            'files': [{'id': 'folder_123', 'name': 'Test Folder'}]
        }
        mock_drive_service.files().list.return_value = mock_list_result
        
        result = find_or_create_folder(mock_drive_service, "Test Folder")
        
        assert result == 'folder_123'
        # Verify the query was called correctly
        mock_drive_service.files().list.assert_called_with(
            q="name='Test Folder' and mimeType='application/vnd.google-apps.folder' and trashed=false",
            fields="files(id, name)"
        )

    def test_find_or_create_folder_create_new(self):
        """Test creating new folder when not found"""
        mock_drive_service = Mock()
        # First call returns no folders (not found)
        mock_list_result = Mock()
        mock_list_result.execute.return_value = {'files': []}
        mock_drive_service.files().list.return_value = mock_list_result
        
        # Second call creates folder
        mock_create_result = Mock()
        mock_create_result.execute.return_value = {'id': 'new_folder_456'}
        mock_drive_service.files().create.return_value = mock_create_result
        
        result = find_or_create_folder(mock_drive_service, "New Folder")
        
        assert result == 'new_folder_456'
        # Verify create was called with correct metadata
        expected_metadata = {
            'name': 'New Folder',
            'mimeType': 'application/vnd.google-apps.folder'
        }
        mock_drive_service.files().create.assert_called_with(body=expected_metadata)

    def test_find_or_create_folder_with_parent(self):
        """Test creating folder with parent folder"""
        mock_drive_service = Mock()
        # Setup list mock
        mock_list_result = Mock()
        mock_list_result.execute.return_value = {'files': []}
        mock_drive_service.files().list.return_value = mock_list_result
        
        # Setup create mock
        mock_create_result = Mock()
        mock_create_result.execute.return_value = {'id': 'child_folder_789'}
        mock_drive_service.files().create.return_value = mock_create_result
        
        result = find_or_create_folder(mock_drive_service, "Child Folder", "parent_123")
        
        assert result == 'child_folder_789'
        # Verify parent was included in create metadata
        expected_metadata = {
            'name': 'Child Folder',
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': ['parent_123']
        }
        mock_drive_service.files().create.assert_called_with(body=expected_metadata)

    def test_get_existing_document_id_found(self):
        """Test finding existing document"""
        mock_drive_service = Mock()
        mock_drive_service.files().list().execute.return_value = {
            'files': [{'id': 'doc_123', 'name': 'Test Doc'}]
        }
        
        result = get_existing_document_id(mock_drive_service, "Test Doc")
        
        assert result == 'doc_123'

    def test_get_existing_document_id_not_found(self):
        """Test when document is not found"""
        mock_drive_service = Mock()
        mock_drive_service.files().list().execute.return_value = {'files': []}
        
        result = get_existing_document_id(mock_drive_service, "Nonexistent Doc")
        
        assert result is None

    def test_clear_document_content(self):
        """Test clearing content from existing document"""
        mock_docs_service = Mock()
        mock_docs_service.documents().get().execute.return_value = {
            'body': {
                'content': [
                    {'endIndex': 50},
                    {'endIndex': 100}
                ]
            }
        }
        
        clear_document_content(mock_docs_service, "doc_123")
        
        # Verify delete request was made
        expected_delete_request = {
            'deleteContentRange': {
                'range': {
                    'startIndex': 1,
                    'endIndex': 99  # end_index - 1
                }
            }
        }
        mock_docs_service.documents().batchUpdate.assert_called_once_with(
            documentId="doc_123",
            body={'requests': [expected_delete_request]}
        )

    def test_clear_document_content_empty_doc(self):
        """Test clearing content from empty document"""
        mock_docs_service = Mock()
        mock_docs_service.documents().get().execute.return_value = {
            'body': {'content': []}
        }
        
        clear_document_content(mock_docs_service, "doc_123")
        
        # Should not call batchUpdate for empty document
        mock_docs_service.documents().batchUpdate.assert_not_called()

    @patch('src.markgdoc.markgdoc.authenticate_google_drive')
    def test_create_empty_google_doc_basic(self, mock_auth):
        """Test basic document creation"""
        mock_drive_service = Mock()
        mock_auth.return_value = mock_drive_service
        mock_drive_service.files().create().execute.return_value = {'id': 'doc_new_123'}
        
        doc_id, doc_url = create_empty_google_doc("Test Doc", "creds.json", ["scope"])
        
        assert doc_id == 'doc_new_123'
        assert doc_url == 'https://docs.google.com/document/d/doc_new_123/edit'
        
        # Verify permissions were set
        mock_drive_service.permissions().create.assert_called_once_with(
            fileId='doc_new_123',
            body={'type': 'anyone', 'role': 'writer'}
        )

    @patch('src.markgdoc.markgdoc.authenticate_google_drive')
    def test_create_empty_google_doc_in_folder(self, mock_auth):
        """Test document creation in specific folder"""
        mock_drive_service = Mock()
        mock_auth.return_value = mock_drive_service
        mock_drive_service.files().create().execute.return_value = {'id': 'doc_folder_456'}
        
        doc_id, doc_url = create_empty_google_doc("Test Doc", "creds.json", ["scope"], 
                                                 folder_id="folder_123")
        
        assert doc_id == 'doc_folder_456'
        
        # Verify folder was specified in create call
        create_call_args = mock_drive_service.files().create.call_args[1]['body']
        assert 'parents' in create_call_args
        assert create_call_args['parents'] == ['folder_123']

    @patch('src.markgdoc.markgdoc.authenticate_google_drive')
    def test_create_empty_google_doc_no_permissions(self, mock_auth):
        """Test document creation without public permissions"""
        mock_drive_service = Mock()
        mock_auth.return_value = mock_drive_service
        mock_drive_service.files().create().execute.return_value = {'id': 'doc_private_789'}
        
        doc_id, doc_url = create_empty_google_doc("Private Doc", "creds.json", ["scope"], 
                                                 set_public_permissions=False)
        
        assert doc_id == 'doc_private_789'
        
        # Verify permissions were NOT set
        mock_drive_service.permissions().create.assert_not_called()

    @patch('src.markgdoc.markgdoc.authenticate_google_docs')
    @patch('src.markgdoc.markgdoc.find_or_create_folder')
    @patch('src.markgdoc.markgdoc.get_existing_document_id')
    @patch('src.markgdoc.markgdoc.create_empty_google_doc')
    @patch('src.markgdoc.markgdoc.authenticate_google_drive')
    def test_get_or_create_document_create_new(self, mock_auth_drive, mock_create_doc, 
                                              mock_get_existing, mock_create_folder, 
                                              mock_auth_docs):
        """Test creating new document when existing not found"""
        mock_get_existing.return_value = None
        mock_create_doc.return_value = ('new_doc_123', 'https://docs.google.com/document/d/new_doc_123/edit')
        mock_create_folder.return_value = 'folder_456'
        
        doc_id, doc_url, was_existing = get_or_create_document(
            "New Doc", "creds.json", ["scope"], folder_name="Test Folder"
        )
        
        assert doc_id == 'new_doc_123'
        assert doc_url == 'https://docs.google.com/document/d/new_doc_123/edit'
        assert was_existing == False
        
        mock_create_folder.assert_called_once_with(mock_auth_drive.return_value, "Test Folder")
        mock_create_doc.assert_called_once_with("New Doc", "creds.json", ["scope"], 'folder_456', True)

    @patch('src.markgdoc.markgdoc.clear_document_content')
    @patch('src.markgdoc.markgdoc.authenticate_google_docs')
    @patch('src.markgdoc.markgdoc.get_existing_document_id')
    @patch('src.markgdoc.markgdoc.authenticate_google_drive')
    def test_get_or_create_document_use_existing(self, mock_auth_drive, mock_get_existing, 
                                                mock_auth_docs, mock_clear_content):
        """Test using existing document"""
        mock_get_existing.return_value = 'existing_doc_789'
        
        doc_id, doc_url, was_existing = get_or_create_document(
            "Existing Doc", "creds.json", ["scope"], use_existing=True
        )
        
        assert doc_id == 'existing_doc_789'
        assert doc_url == 'https://docs.google.com/document/d/existing_doc_789/edit'
        assert was_existing == True
        
        mock_clear_content.assert_called_once_with(mock_auth_docs.return_value, 'existing_doc_789')

    @patch('src.markgdoc.markgdoc.process_markdown_content')
    @patch('src.markgdoc.markgdoc.get_or_create_document')
    def test_convert_to_google_docs_enhanced(self, mock_get_or_create, mock_process):
        """Test enhanced convert_to_google_docs function"""
        mock_get_or_create.return_value = ('doc_123', 'https://example.com/doc', False)
        mock_docs_service = Mock()
        
        result = convert_to_google_docs(
            "# Test Markdown", "Test Doc", mock_docs_service, 
            "creds.json", ["scope"], folder_name="Projects", 
            use_existing=True, debug=True
        )
        
        assert result['doc_url'] == 'https://example.com/doc'
        assert result['doc_id'] == 'doc_123'
        assert result['was_existing'] == False
        assert result['folder_info'] == 'Projects'
        
        mock_get_or_create.assert_called_once_with(
            "Test Doc", "creds.json", ["scope"], "Projects", True, True, True
        )
