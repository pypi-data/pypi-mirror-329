import json
import subprocess
import unittest
from unittest.mock import MagicMock, Mock, patch

from wmk.packager import Packager


class TestPackager(unittest.TestCase):
    def setUp(self):
        self.test_dir = "/test/dir"
        self.packager = Packager(
            target=self.test_dir,
            platform=["linux_x86_64"],
            build_version="1.0.0",
            python_version="3.9",
            skip=["skip_pkg"],
        )

    def test_init(self):
        # Test initialization with default values
        packager = Packager()
        self.assertEqual(packager.platform, ["manylinux2014_x86_64", "manylinux_2_17_x86_64"])
        self.assertTrue(packager.only_tracked)
        self.assertIsNone(packager.additional_files)
        self.assertIsNone(packager.build_version)
        self.assertIsNone(packager.python_version)

        # Test initialization with custom values
        packager = Packager(
            target="/custom/dir",
            platform=["win_amd64"],
            only_tracked=False,
            additional_files=["extra.txt"],
            build_version="2.0.0",
            python_version="3.10",
        )
        self.assertEqual(packager.target_dir, "/custom/dir")
        self.assertEqual(packager.platform, ["win_amd64"])
        self.assertFalse(packager.only_tracked)
        self.assertEqual(packager.additional_files, ["extra.txt"])
        self.assertEqual(packager.build_version, "2.0.0")
        self.assertEqual(packager.python_version, "3.10")
        self.assertEqual(packager.dependencies_dir, "/custom/dir/dependencies")

        # Test initialization with skip parameter
        packager = Packager(skip=["pkg1", "pkg2"])
        self.assertEqual(packager.skip, ["pkg1", "pkg2"])

    @patch("wmk.packager.subprocess.run")
    @patch("wmk.packager.subprocess.Popen")
    @patch("wmk.packager.Path")
    @patch("wmk.packager.os.path.exists")
    def test_download_packages(self, mock_exists, mock_path, mock_popen, mock_run):
        # Test when requirements file doesn't exist
        mock_exists.return_value = False
        self.assertFalse(self.packager.download_packages())

        # Test successful download
        mock_exists.return_value = True
        mock_run.return_value = Mock(returncode=0)
        mock_process = Mock()
        mock_process.returncode = 0
        mock_process.stderr.readline.return_value = ""
        mock_process.poll.return_value = 0
        mock_popen.return_value = mock_process

        report_data = {
            "install": [
                {
                    "metadata": {"name": "pkg1", "version": "1.0"},
                    "download_info": {"url": "pkg1.whl"},
                },
                {
                    "metadata": {"name": "pkg2", "version": "2.0"},
                    "download_info": {"url": "pkg2.tar.gz"},
                },
            ]
        }
        mock_open = unittest.mock.mock_open(read_data=json.dumps(report_data))
        with patch("builtins.open", mock_open):
            self.assertTrue(self.packager.download_packages())

        # Test download failure
        mock_run.return_value = Mock(returncode=1, stderr="Download error")
        self.assertFalse(self.packager.download_packages())

    @patch("wmk.packager.subprocess.run")
    @patch("wmk.packager.subprocess.Popen")
    @patch("wmk.packager.Path")
    @patch("wmk.packager.os.path.exists")
    def test_skip_packages(self, mock_exists, mock_path, mock_popen, mock_run):
        mock_exists.return_value = True
        mock_run.return_value = Mock(returncode=0)
        mock_process = Mock()
        mock_process.returncode = 0
        mock_process.stderr.readline.return_value = ""
        mock_process.poll.return_value = 0
        mock_popen.return_value = mock_process

        report_data = {
            "install": [
                {
                    "metadata": {"name": "skip_pkg", "version": "1.0"},
                    "download_info": {"url": "skip_pkg.whl"},
                },
                {
                    "metadata": {"name": "pkg2", "version": "2.0"},
                    "download_info": {"url": "pkg2.whl"},
                },
            ]
        }
        mock_open = unittest.mock.mock_open(read_data=json.dumps(report_data))
        with patch("builtins.open", mock_open):
            self.assertTrue(self.packager.download_packages())
            # Verify that only pkg2 was processed
            write_calls = [call[0][0] for call in mock_open().write.call_args_list]
            self.assertTrue(any("pkg2==2.0" in call for call in write_calls))
            self.assertFalse(any("skip_pkg==1.0" in call for call in write_calls))

    def test_generate_manifest(self):
        manifest = self.packager.generate_manifest()

        self.assertEqual(manifest["runtime"], "python")
        self.assertEqual(manifest["runtimeRequirements"]["platform"], ["linux_x86_64"])
        self.assertEqual(manifest["runtimeRequirements"]["pythonVersion"], "3.9")
        self.assertEqual(manifest["buildVersion"], "1.0.0")
        self.assertEqual(manifest["entities"], [])
        self.assertIn("timeStamp", manifest)
        self.assertIn("scripts", manifest)
        self.assertIn("install", manifest["scripts"])

    @patch("wmk.packager.ZipFile")
    @patch("wmk.packager.subprocess.check_output")
    @patch("wmk.packager.os.path.exists")
    def test_create_archive(self, mock_exists, mock_check_output, mock_zipfile):
        mock_exists.return_value = True
        mock_zip = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip

        # Test with git-tracked files
        mock_check_output.return_value = "file1.py\nfile2.py"
        self.assertTrue(self.packager.create_archive("test.zip"))
        self.assertEqual(mock_zip.write.call_count, 2)

        # Test with git command failure
        mock_check_output.side_effect = subprocess.CalledProcessError(128, "git")
        self.assertFalse(self.packager.create_archive("test.zip"))

        # Test with additional files
        mock_check_output.side_effect = None
        mock_check_output.return_value = ""
        packager = Packager(
            target=self.test_dir, only_tracked=False, additional_files=["extra.txt"]
        )

        with (
            patch("wmk.packager.os.path.isfile") as mock_isfile,
            patch("wmk.packager.os.path.isdir") as mock_isdir,
        ):
            mock_isfile.return_value = True
            mock_isdir.return_value = False
            self.assertTrue(packager.create_archive("test.zip"))

        # Test archive creation failure
        mock_zipfile.side_effect = Exception("ZIP error")
        self.assertFalse(self.packager.create_archive("test.zip"))


if __name__ == "__main__":
    unittest.main()
