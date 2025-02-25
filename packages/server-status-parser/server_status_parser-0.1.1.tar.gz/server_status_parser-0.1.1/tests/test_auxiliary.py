import unittest
from server_status_parser.parser import (
    extract_heading,
    extract_server_info,
    extract_scoreboard,
)


class TestParser(unittest.TestCase):
    def test_extract_heading_html(self):
        content = "<h1>Apache Server Status for example.com (via 127.0.0.1)</h1>"
        heading, endpoint, via_part = extract_heading(content)
        self.assertEqual(
            heading, "Apache Server Status for example.com (via 127.0.0.1)"
        )
        self.assertEqual(endpoint, "example.com")
        self.assertEqual(via_part, "127.0.0.1")

    def test_extract_heading_html_no_via(self):
        content = "<h1>Apache Server Status for example.com</h1>"
        heading, endpoint, via_part = extract_heading(content)
        self.assertEqual(heading, "Apache Server Status for example.com")
        self.assertEqual(endpoint, "example.com")
        self.assertIsNone(via_part)

    def test_extract_heading_text(self):
        content = "Apache Server Status for localhost\n   Server Version: Apache/2.2.15 (Unix)"
        heading, endpoint, via_part = extract_heading(content)
        self.assertEqual(heading, "Apache Server Status for localhost")
        self.assertEqual(endpoint, "localhost")
        self.assertIsNone(via_part)

    def test_extract_heading_title_has_heading(self):
        content = "<head>\n<title>Apache Status</title>\n</head><body>\n<h1>Apache Server Status for i_am_an_onion.onion (via 1.2.3.4)</h1>\n\n<dl><dt>Server Version: Apache/2.4.5"
        heading, endpoint, via_part = extract_heading(content)
        self.assertEqual(
            heading, "Apache Server Status for i_am_an_onion.onion (via 1.2.3.4)"
        )
        self.assertEqual(endpoint, "i_am_an_onion.onion")
        self.assertEqual(via_part, "1.2.3.4")

    def test_extract_heading_none(self):
        content = ""
        heading, endpoint, via_part = extract_heading(content)
        self.assertIsNone(heading)
        self.assertIsNone(endpoint)
        self.assertIsNone(via_part)

    def test_server_properties_all(self):
        content = "</h1>\n\n<dl><dt>Server Version: Apache/2.4.52 (Ubuntu)</dt>\n<dt>Server MPM: prefork</dt>\n<dt>Server Built: 2023-05-03T20:02:51\n</dt></dl><hr /><dl>\n<dt>Current Time:"
        server_version, server_mpm, server_built = extract_server_info(content)
        self.assertEqual(server_version, "Apache/2.4.52 (Ubuntu)")
        self.assertEqual(server_mpm, "prefork")
        self.assertEqual(server_built, "2023-05-03T20:02:51")

    def test_server_properties_only_version(self):
        content = "</h1>\n\n<dl><dt>Server Version: Apache/2.4.52 (Ubuntu)</dt>\n</dl><hr /><dl>\n<dt>Current Time:"
        server_version, server_mpm, server_built = extract_server_info(content)
        self.assertEqual(server_version, "Apache/2.4.52 (Ubuntu)")
        self.assertIsNone(server_mpm)
        self.assertIsNone(server_built)

    def test_server_properties_none(self):
        content = ""
        server_version, server_mpm, server_built = extract_server_info(content)
        self.assertIsNone(server_version)
        self.assertIsNone(server_mpm)
        self.assertIsNone(server_built)

    def test_extract_scoreboard_html(self):
        content = "n</dl><pre>______._W_._\n...</pre>\n<p>Scoreboard Key:<br />\n"
        scoreboard = extract_scoreboard(content)
        self.assertEqual(scoreboard, "______._W_._...")


if __name__ == "__main__":
    unittest.main()
