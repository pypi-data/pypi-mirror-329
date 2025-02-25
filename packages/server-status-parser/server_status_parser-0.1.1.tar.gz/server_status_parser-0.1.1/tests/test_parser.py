import unittest
from server_status_parser import extract_info_from_html


class TestParser(unittest.TestCase):
    def test_html_page(self):
        content = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<html><head>\n<title>Apache Server Status for localhost</title>\n</head><body>\n<h1>Apache Server Status for onion.onion (via 127.0.0.1)</h1>\n<dl><dt>Server Version: Apache/2.2.9 (Ubuntu) PHP/5.2.6-2ubuntu4.6 with Suhosin-Patch mod_perl/2.0.4 Perl/v5.10.0</dt> \n<dt>Server Built: Mar 9 2022 22:03:13\n</dt></dl><hr /><dl>\n<dt>Current Time: Monday, 22-Mar-2022 16:45:44 EET</dt>\n<dt>Restart Time: Monday, 22-Mar-2022 16:40:18 EET</dt>\n<dt>Parent Server Config. Generation: 1</dt>\n<dt>Parent Server MPM Generation: 0</dt>\n<dt>Server uptime:  10 hours 32 minutes 23 seconds</dt>\n<dt>Server load: -1.00 -1.00 -1.00</dt>\n<dt>Total accesses: 254 - Total Traffic: 32.0 MB - Total Duration: 3437</dt>\n<dt>.00669 requests/sec - 885 B/second - 129.2 kB/request - 13.5315 ms/request</dt>\n<dt>1 requests currently being processed, 149 idle workers</dt>\n</dl><pre>________________________________________________________________\n________________________________________________________________\n_________________W____</pre>\n<p>Scoreboard Key:<br/>\n"<b><code>_</code></b>" Waiting for Connection,\n"<b><code>S</code></b>" Starting up, \n"<b><code>R</code></b>" Reading Request,<br />\n"<b><code>W</code></b>" Sending Reply, \n"<b><code>K</code></b>" Keepalive (read), \n"<b><code>D</code></b>" DNS Lookup,<br />\n"<b><code>C</code></b>" Closing connection, \n"<b><code>L</code></b>" Logging, \n"<b><code>G</code></b>" Gracefully finishing,<br /> \n"<b><code>I</code></b>" Idle cleanup of worker, \n"<b><code>.</code></b>" Open slot with no current process<br />\n</p>\n\n<table border="0"><tr><th>Srv</th><th>PID</th><th>Acc</th><th>M</th><th>SS</th><th>Req</th><th>Dur</th><th>Conn</th><th>Child</th><th>Slot</th><th>Client</th><th>Protocol</th><th>VHost</th><th>Request</th></tr>\n\n<tr><td><b>0-0</b></td><td>10776</td><td>0/18/18</td><td>_\n</td><td>707</td><td>1</td><td>114</td><td>0.0</td><td>1.84</td><td>1.84\n</td><td>127.0.0.1</td><td>http/1.1</td><td nowrap>localhost:80</td><td nowrap>GET /index.html HTTP/1.1</td></tr>\n\n<tr><td><b>0-0</b></td><td>10776</td><td>0/10/10</td><td>_\n</td><td>705</td><td>3</td><td>70</td><td>0.0</td><td>2.42</td><td>2.42\n</td><td>127.0.0.1</td><td>http/1.1</td><td nowrap>localhost:80</td><td nowrap>GET /css/upper.css HTTP/1.1</td></tr>\n\n<tr><td><b>0-0</b></td><td>10776</td><td>0/1/1</td><td>_\n</td><td>6004</td><td>4</td><td>8</td><td>0.0</td><td>0.00</td><td>0.00\n</td><td>127.0.0.1</td><td>http/1.1</td><td nowrap>localhost:80</td><td nowrap>GET /images/icon.png HTTP/1.1</td></tr>\n \n<tr><td><b>0-0</b></td><td>10776</td><td>0/4/4</td><td>_\n</td><td>6005</td><td>2</td><td>27</td><td>0.0</td><td>0.01</td><td>0.01\n</td><td>127.0.0.1</td><td>http/1.1</td><td nowrap></td><td nowrap></td></tr>\n\n<tr><td><b>0-0</b></td><td>10776</td><td>0/30/30</td><td><b>W</b>\n</td><td>0</td><td>0</td><td>397</td><td>0.0</td><td>8.54</td><td>8.54\n</td><td>127.0.0.1</td><td>http/1.1</td><td nowrap>localhost:80</td><td nowrap>GET /server-status HTTP/1.1</td></tr>\n \n<tr><td><b>0-0</b></td><td>10776</td><td>0/58/58</td><td>_\n</td><td>85</td><td>4</td><td>917</td><td>0.0</td><td>8.21</td><td>8.21\n</td><td>127.0.0.1</td><td>http/1.1</td><td nowrap></td><td nowrap></td></tr>\n\n<tr><td><b>0-0</b></td><td>10776</td><td>0/57/57</td><td>_\n</td><td>1264</td><td>6</td><td>605</td><td>0.0</td><td>4.83</td><td>4.83\n</td><td>127.0.0.1</td><td>http/1.1</td><td nowrap></td><td nowrap></td></tr>\n\n</table>\n <hr /> <table>\n <tr><th>Srv</th><td>Child Server number - generation</td></tr>\n <tr><th>PID</th><td>OS process ID</td></tr>\n <tr><th>Acc</th><td>Number of accesses this connection / this child / this slot</td></tr>\n <tr><th>M</th><td>Mode of operation</td></tr>\n<tr><th>SS</th><td>Seconds since beginning of most recent request</td></tr>\n <tr><th>Req</th><td>Milliseconds required to process most recent request</td></tr>\n <tr><th>Dur</th><td>Sum of milliseconds required to process all requests</td></tr>\n <tr><th>Conn</th><td>Kilobytes transferred this connection</td></tr>\n <tr><th>Child</th><td>Megabytes transferred this child</td></tr>\n <tr><th>Slot</th><td>Total megabytes transferred this slot</td></tr>\n </table>\n<hr>\n<table cellspacing=0 cellpadding=0>\n<tr><td bgcolor="#000000">\n<b><font color="#ffffff" face="Arial,Helvetica">SSL/TLS Session Cache Status:</font></b>\n</td></tr>\n<tr><td bgcolor="#ffffff">\ncache type: <b>SHMCB</b>, shared memory: <b>512000</b> bytes, current entries: <b>0</b><br>subcaches: <b>32</b>, indexes per subcache: <b>88</b><br>index usage: <b>0%</b>, cache usage: <b>0%</b><br>total entries stored since starting: <b>0</b><br>total entries replaced since starting: <b>0</b><br>total entries expired since starting: <b>0</b><br>total (pre-expiry) entries scrolled out of the cache: <b>0</b><br>total retrieves since starting: <b>0</b> hit, <b>0</b> miss<br>total removes since starting: <b>0</b> hit, <b>0</b> miss<br></td></tr>\n</table>\n<hr />\n\n<address>Apache/2.2.9 (Ubuntu PHP/5.2.6-2ubuntu4.6 with Suhosin-Patch mod_perl/2.0.4 Perl/v5.10.0 Server at gpvdip7rd7bdy5gf7scl3rzgzgzckqw4sqxbmy6g3zijfwu4lz3ypbyd.onion Port 80</address>\n</body></html>\n'
        parsed = extract_info_from_html(content)

        self.assertEqual(
            parsed["heading"], "Apache Server Status for onion.onion (via 127.0.0.1)"
        )
        self.assertEqual(parsed["endpoint"], "onion.onion")
        self.assertEqual(parsed["via_part"], "127.0.0.1")

        self.assertEqual(
            parsed["server_version"],
            "Apache/2.2.9 (Ubuntu) PHP/5.2.6-2ubuntu4.6 with Suhosin-Patch mod_perl/2.0.4 Perl/v5.10.0",
        )
        self.assertIsNone(parsed["server_mpm"])
        self.assertEqual(parsed["server_built"], "Mar 9 2022 22:03:13")

        self.assertEqual(len(parsed["aggregated_stats"].keys()), 15)
        self.assertEqual(
            parsed["aggregated_stats"]["current time"].lower(),
            "monday, 22-mar-2022 16:45:44 eet".lower(),
        )
        self.assertEqual(
            parsed["aggregated_stats"]["restart time"].lower(),
            "monday, 22-mar-2022 16:40:18 eet".lower(),
        )
        self.assertEqual(
            parsed["aggregated_stats"]["parent server config. generation"], "1"
        )
        self.assertEqual(
            parsed["aggregated_stats"]["parent server mpm generation"], "0"
        )
        self.assertEqual(
            parsed["aggregated_stats"]["server uptime"],
            "10 hours 32 minutes 23 seconds",
        )
        self.assertEqual(parsed["aggregated_stats"]["server load"], "-1.00 -1.00 -1.00")
        self.assertEqual(parsed["aggregated_stats"]["total accesses"], "254")
        self.assertEqual(parsed["aggregated_stats"]["total traffic"].lower(), "32.0 mb")
        self.assertEqual(parsed["aggregated_stats"]["total duration"], "3437")
        self.assertEqual(parsed["aggregated_stats"]["requests/sec"], "00669")
        self.assertEqual(parsed["aggregated_stats"]["b/second"], "885")
        self.assertEqual(parsed["aggregated_stats"]["kb/request"], "129.2")
        self.assertEqual(parsed["aggregated_stats"]["ms/request"], "13.5315")
        self.assertEqual(
            parsed["aggregated_stats"]["requests currently being processed"], "1"
        )
        self.assertEqual(parsed["aggregated_stats"]["idle workers"], "149")

        self.assertEqual(
            parsed["scoreboard"],
            "_________________________________________________________________________________________________________________________________________________W____",
        )

        self.assertIsNotNone(parsed["workers_table"])
        self.assertEqual(parsed["workers_table"].shape, (7, 14))

    def test_simple_page(self):
        content = 'Apache Server Status for localhost\n   Server Version: Apache/2.2.15 (Unix) DAV/2 PHP/5.3.3\n   Server Built: Aug 13 2019 17:29:28\n\n   --------------------------------------------------------------------------\n   Current Time: Tuesday, 14-Jan-2019 04:34:13 EST\n   Restart Time: Tuesday, 14-Jan-2019 00:33:05 EST\n   Parent Server Generation: 0\n   Server uptime: 4 hours 1 minute 7 seconds\n   Total accesses: 2748 - Total Traffic: 9.6 MB\n   CPU Usage: u.9 s1.06 cu0 cs0 - .0135% CPU load\n   .19 requests/sec - 695 B/second - 3658 B/request\n   1 requests currently being processed, 4 idle workers\n .__.__W...\n\n   Scoreboard Key:\n   "_" Waiting for Connection, "S" Starting up, "R" Reading Request,\n   "W" Sending Reply, "K" Keepalive (read), "D" DNS Lookup,\n   "C" Closing connection, "L" Logging, "G" Gracefully finishing,\n   "I" Idle cleanup of worker, "." Open slot with no current process\n\nSrv PID     Acc    M CPU   SS  Req Conn Child Slot     Client        VHost             Request\n0-0 -    0/0/428   . 0.30 5572 0   0.0  0.00  1.34 127.0.0.1      5.175.142.66 OPTIONS * HTTP/1.0\n                                                                               GET\n1-0 5606 0/639/639 _ 0.46 4    0   0.0  2.18  2.18 115.113.134.14 5.175.142.66 /server-status?refresh=5\n                                                                               HTTP/1.1\n                                                                               GET\n2-0 5607 0/603/603 _ 0.43 0    0   0.0  2.09  2.09 115.113.134.14 5.175.142.66 /server-status?refresh=5\n                                                                               HTTP/1.1\n3-0 -    0/0/337   . 0.23 5573 0   0.0  0.00  1.09 127.0.0.1      5.175.142.66 OPTIONS * HTTP/1.0\n                                                                               GET\n4-0 5701 0/317/317 _ 0.23 9    0   0.0  1.21  1.21 115.113.134.14 5.175.142.66 /server-status?refresh=5\n                                                                               HTTP/1.1\n                                                                               GET\n5-0 5708 0/212/213 _ 0.15 6    0   0.0  0.85  0.85 115.113.134.14 5.175.142.66 /server-status?refresh=5\n                                                                               HTTP/1.1\n6-0 5709 0/210/210 W 0.16 0    0   0.0  0.84  0.84 127.0.0.1      5.175.142.66 GET /server-status\n                                                                               HTTP/1.1\n7-0 -    0/0/1     . 0.00 5574 0   0.0  0.00  0.00 127.0.0.1      5.175.142.66 OPTIONS * HTTP/1.0\n\n   --------------------------------------------------------------------------\n\n    Srv  Child Server number - generation\n    PID  OS process ID\n    Acc  Number of accesses this connection / this child / this slot\n     M   Mode of operation\n    CPU  CPU usage, number of seconds\n    SS   Seconds since beginning of most recent request\n    Req  Milliseconds required to process most recent request\n   Conn  Kilobytes transferred this connection\n   Child Megabytes transferred this child\n   Slot  Total megabytes transferred this slot\n   --------------------------------------------------------------------------\n\n    Apache/2.2.15 (CentOS) Server at localhost Port 80\n'
        parsed = extract_info_from_html(content)

        self.assertEqual(parsed["heading"], "Apache Server Status for localhost")
        self.assertEqual(parsed["endpoint"], "localhost")
        self.assertIsNone(parsed["via_part"])

        self.assertEqual(
            parsed["server_version"], "Apache/2.2.15 (Unix) DAV/2 PHP/5.3.3"
        )
        self.assertIsNone(parsed["server_mpm"])
        self.assertEqual(parsed["server_built"], "Aug 13 2019 17:29:28")

        self.assertEqual(len(parsed["aggregated_stats"].keys()), 13)
        self.assertEqual(
            parsed["aggregated_stats"]["current time"].lower(),
            "tuesday, 14-jan-2019 04:34:13 est".lower(),
        )
        self.assertEqual(
            parsed["aggregated_stats"]["restart time"].lower(),
            "tuesday, 14-jan-2019 00:33:05 est".lower(),
        )
        self.assertEqual(parsed["aggregated_stats"]["parent server generation"], "0")
        self.assertEqual(
            parsed["aggregated_stats"]["server uptime"], "4 hours 1 minute 7 seconds"
        )
        self.assertEqual(parsed["aggregated_stats"]["total accesses"], "2748")
        self.assertEqual(parsed["aggregated_stats"]["total traffic"].lower(), "9.6 mb")
        self.assertEqual(parsed["aggregated_stats"]["cpu usage"], "u.9 s1.06 cu0 cs0")
        self.assertEqual(parsed["aggregated_stats"]["cpu load"], ".0135%")
        self.assertEqual(parsed["aggregated_stats"]["requests/sec"], "19")
        self.assertEqual(parsed["aggregated_stats"]["b/second"], "695")
        self.assertEqual(parsed["aggregated_stats"]["b/request"], "3658")
        self.assertEqual(
            parsed["aggregated_stats"]["requests currently being processed"], "1"
        )
        self.assertEqual(parsed["aggregated_stats"]["idle workers"], "4")

        self.assertEqual(parsed["scoreboard"], ".__.__W...")

        self.assertIsNone(parsed["workers_table"])


if __name__ == "__main__":
    unittest.main()
