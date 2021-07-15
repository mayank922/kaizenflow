import logging

import helpers.open as hopen
import helpers.unit_test as hut

_LOG = logging.getLogger(__name__)


# TODO(gp): Some of these tests should be executed outside of the container to
#  test other systems.


class Test_open_unknown(hut.TestCase):
    """
    Test unknown extension and unknown systems.
    """

    def test_unknown_extension1(self) -> None:
        """
        Test unknown extension raises an error.
        """
        with self.assertRaises(AssertionError) as cm:
            hopen.open_file("a.unknown_ext")
        # Check error text.
        self.assertIn("unknown_ext", str(cm.exception))

    def test_unknown_os1(self) -> None:
        """
        Test unknown OS raises an error.
        """
        with self.assertRaises(AssertionError) as cm:
            hopen._cmd_open_html("b.html", "UnknownOS")
        # Check error text.
        self.assertIn("UnknownOS", str(cm.exception))


class Test_open_html(hut.TestCase):
    """
    Test different command correctness for opening html file.
    """

    def test_linux1(self) -> None:
        """
        Test Linux.
        """
        cmd = hopen._cmd_open_html("a.html", "Linux")
        self.check_string(str(cmd))

    def test_windows1(self) -> None:
        """
        Test Windows.
        """
        cmd = hopen._cmd_open_html("b.html", "Windows")
        self.check_string(str(cmd))

    def test_mac1(self) -> None:
        """
        Test Darwin.
        """
        cmd = hopen._cmd_open_html("c.html", "Darwin")
        self.check_string(str(cmd))


class Test_open_pdf(hut.TestCase):
    """
    Test different command correctness for opening pdf file.
    """

    def test_mac1(self) -> None:
        """
        Test Darwin.
        """
        cmd = hopen._cmd_open_html("a.pdf", "Darwin")
        self.check_string(str(cmd))
