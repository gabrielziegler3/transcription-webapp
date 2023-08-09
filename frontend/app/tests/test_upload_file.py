import unittest
from unittest.mock import patch, Mock
from pages.Upload_File import upload_file  # Adjust the import according to your module's name

class TestUploadFile(unittest.TestCase):

    @patch("pages.Upload_File.st")  # Again, adjust the import according to your module's name
    @patch("pages.Upload_File.httpx.post")
    def test_successful_upload(self, mock_post, mock_st):
        # Mock successful response (status_code 200)
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = "File uploaded successfully"
        mock_post.return_value = mock_response
        
        # Mock file_uploader to return a file
        mock_file = Mock()
        mock_file.name = "test_file.txt"
        mock_st.file_uploader.return_value = mock_file
        
        upload_file()
        
        # Assertions
        mock_st.write.assert_called_with("File uploaded successfully")

    @patch("pages.Upload_File.st")  # Again, adjust the import according to your module's name
    @patch("pages.Upload_File.httpx.post")
    def test_failed_upload(self, mock_post, mock_st):
        # Mock unsuccessful response (status_code 400 for example)
        mock_response = Mock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response
        
        # Mock file_uploader to return a file
        mock_file = Mock()
        mock_file.name = "test_file.txt"
        mock_st.file_uploader.return_value = mock_file
        
        upload_file()
        
        # Assertions
        # In this case, we just want to ensure that st.write was not called
        mock_st.write.assert_not_called()

    @patch("pages.Upload_File.st")  # Again, adjust the import according to your module's name
    @patch("pages.Upload_File.httpx.post")
    def test_no_file_uploaded(self, mock_post, mock_st):
        # Mock file_uploader to return None (no file uploaded)
        mock_st.file_uploader.return_value = None
        
        upload_file()
        
        # Assertions
        mock_post.assert_not_called()  # Ensure httpx.post was not called
        mock_st.write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
