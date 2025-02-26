import unittest
from file_compressor import compress_file, compress_directory

class TestCompressor(unittest.TestCase):
    def test_compress_file(self):
        compress_file('test_file.txt', 'test_output.zip')
        # Test if the file is compressed successfully (e.g., by checking if it exists)
        # Add more tests for your logic

    def test_compress_directory(self):
        compress_directory('test_folder', 'test_folder.zip')
        # Test if the directory is compressed successfully (e.g., check if the zip file exists)
        # Add more tests for your logic

if __name__ == '__main__':
    unittest.main()
