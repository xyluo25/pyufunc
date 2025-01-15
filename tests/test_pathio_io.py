import pytest
from pathlib import Path
import shutil

from pyufunc.util_pathio._io import get_file_size, get_dir_size
from pyufunc import path2linux


class TestGetFileSize:
    # Helper method to create a temporary file with a specific size
    @staticmethod
    def create_temp_file(size_in_bytes: int, tmp_path: Path, filename: str) -> Path:
        file_path = tmp_path / filename
        with open(file_path, "wb") as f:
            f.write(b"\0" * size_in_bytes)
        return file_path

    @pytest.mark.parametrize("input_size, unit, expected_output", [
        (1024, "kb", "Filesize: test_file 1.0 kb"),
        (1048576, "mb", "Filesize: test_file 1.0 mb"),
    ])
    def test_valid_file_size(self, tmp_path, input_size, unit, expected_output):
        filename = "test_file"
        file_path = self.create_temp_file(input_size, tmp_path, filename)
        result = get_file_size(file_path, unit)

        # delete file_path
        file_path.unlink()

        # delete tmp_path
        tmp_path.rmdir()

        assert expected_output == result

    def test_invalid_filename_type(self):
        with pytest.raises(AssertionError) as excinfo:
            get_file_size(123, "kb")
        assert "filename must be a string or Path" in str(excinfo.value)

    def test_invalid_unit(self):
        with pytest.raises(AssertionError) as excinfo:
            get_file_size("somefile.txt", "xyz")
        assert "unit must be one of 'kb', 'mb', 'gb', 'tb'" in str(excinfo.value)

    def test_file_not_found(self, tmp_path):
        file_path = tmp_path / "nonexistent_file.txt"
        with pytest.raises(AssertionError) as excinfo:
            get_file_size(file_path, "kb")
        assert "File nonexistent_file.txt does not found" in str(excinfo.value)


class TestGetDirSize:
    def test_valid_directory_size(self, tmp_path: str):
        # Create a temporary directory with some files
        dir_path = tmp_path / "test_directory"
        dir_path.mkdir()
        file1 = dir_path / "file1.txt"
        file1.write_text("This is file 1")

        # Calculate the expected size in kb
        expected_size_kb = file1.stat().st_size / 1024

        # Call the function
        result = get_dir_size(path2linux(dir_path), "kb")

        # Delete the temporary directory
        shutil.rmtree(dir_path, ignore_errors=True)

        # Check the result
        assert result == f"Directory size: test_directory {expected_size_kb} kb"

    def test_invalid_directory_type(self):
        with pytest.raises(AssertionError) as excinfo:
            get_dir_size(123, "kb")
        assert "directory must be a string" in str(excinfo.value)

    def test_invalid_unit(self):
        with pytest.raises(AssertionError) as excinfo:
            get_dir_size("some_directory", "xyz")
        assert "unit must be one of 'kb', 'mb', 'gb', 'tb'" in str(excinfo.value)

    def test_directory_not_found(self):
        with pytest.raises(AssertionError) as excinfo:
            get_dir_size("nonexistent_directory", "kb")
        assert "Directory nonexistent_directory does not found" in str(excinfo.value)