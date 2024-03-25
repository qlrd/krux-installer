# The MIT License (MIT)

# Copyright (c) 2021-2024 Krux contributors

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
base_flasher.py
"""
from unittest import TestCase
from unittest.mock import patch
from src.utils.signer.base_signer import BaseSigner


class TestBaseSigner(TestCase):

    @patch("os.path.exists", return_value=True)
    def test_filename(self, mock_exists):
        s = BaseSigner(filename="mock.txt")
        mock_exists.assert_called_once_with("mock.txt")
        self.assertEqual(s.filename, "mock.txt")

    @patch("os.path.exists", return_value=False)
    def test_fail_filename(self, mock_exists):
        with self.assertRaises(ValueError) as exc_info:
            BaseSigner(filename="mock.txt")
            mock_exists.assert_called_once_with("mock.txt")

        self.assertEqual(str(exc_info.exception), "mock.txt do not exists")

    @patch("os.path.exists", return_value=True)
    def test_filehash(self, mock_exists):
        s = BaseSigner(filename="mock.txt")
        s.filehash = "5f98101992d1b411c05050dec665c16b1ddfd88aec9dd3ed55eefa046a3f4ab9"
        mock_exists.assert_called_once_with("mock.txt")
        self.assertEqual(
            s.filehash,
            "5f98101992d1b411c05050dec665c16b1ddfd88aec9dd3ed55eefa046a3f4ab9",
        )

    @patch("os.path.exists", return_value=True)
    def test_fail_filehash(self, mock_exists):
        with self.assertRaises(ValueError) as exc_info:
            s = BaseSigner(filename="mock.txt")
            s.filehash = (
                "5h98101992i1b411j05050klm665n16o1pqfd88rst9uv3wd55eefa046a3f4ab9"
            )
            mock_exists.assert_called_once_with("mock.txt")

        self.assertEqual(
            str(exc_info.exception),
            "Invalid hash: 5h98101992i1b411j05050klm665n16o1pqfd88rst9uv3wd55eefa046a3f4ab9",
        )

    @patch("os.path.exists", return_value=True)
    def test_signature(self, mock_exists):
        s = BaseSigner(filename="mock.txt")
        s.signature = "".join(
            [
                "MEQCIC2VjiRUu/UyjDlfQJCrA8Yy",
                "PE8gxqZXslsqck3N6t/2AiBj0hvV",
                "6lpczTW4CoaBGlmQB/0yKice5BUF",
                "6xwHQRWvow==",
            ]
        )
        mock_exists.assert_called_once_with("mock.txt")
        self.assertEqual(
            s.signature,
            b"".join(
                [
                    b"0D\x02 -\x95\x8e$T\xbb\xf52\x8c9_@",
                    b"\x90\xab\x03\xc62<O \xc6\xa6W\xb2[*rM",
                    b"\xcd\xea\xdf\xf6\x02 c\xd2\x1b\xd5",
                    b"\xeaZ\\\xcd5\xb8\n\x86\x81\x1aY\x90",
                    b"\x07\xfd2*'\x1e\xe4\x15\x05\xeb\x1c",
                    b"\x07A\x15\xaf\xa3",
                ]
            ),
        )

    @patch("os.path.exists", return_value=True)
    def test_fail_signature(self, mock_exists):
        with self.assertRaises(ValueError) as exc_info:
            s = BaseSigner(filename="mock.txt")
            s.signature = "*&ï&*$#@!@#)*&&*%%"
            mock_exists.assert_called_once_with("mock.txt")

        self.assertEqual(
            str(exc_info.exception), "Invalid signature: *&ï&*$#@!@#)*&&*%%"
        )

    @patch("os.path.exists", return_value=True)
    def test_pubkey(self, mock_exists):
        s = BaseSigner(filename="mock.txt")
        s.pubkey = "027fbea3abf78019ff6da48d6c235931b26732faaf74eeeda8f0a7e5eb32477c20"
        mock_exists.assert_called_once_with("mock.txt")
        self.assertEqual(
            s.pubkey,
            "MDYwEAYHKoZIzj0CAQYFK4EEAAoDIgACf76jq/eAGf9tpI1sI1kxsmcy+q907u2o8Kfl6zJHfCA=",
        )

    @patch("os.path.exists", return_value=True)
    def test_fail_pubkey(self, mock_exists):
        with self.assertRaises(ValueError) as exc_info:
            s = BaseSigner(filename="mock.txt")
            s.pubkey = "abcdef0123456789"
            mock_exists.assert_called_once_with("mock.txt")

        self.assertEqual(str(exc_info.exception), "Invalid pubkey: abcdef0123456789")
