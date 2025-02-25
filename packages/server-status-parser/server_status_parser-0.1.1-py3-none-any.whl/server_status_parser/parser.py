import re
import pandas as pd
from bs4 import BeautifulSoup
from .utils import (
    remove_html_tags,
    find_info_in_text,
    find_info_smart_lines,
)


def extract_server_info(content):
    # server version should be before server mpm
    server_version = find_info_smart_lines(
        content, r"Server Version:(.*?)Server MPM:", None
    )
    if server_version is None:
        # if no server mpm then check if server version is before server built or if it exists at all
        server_version = find_info_smart_lines(
            content, r"Server Version:(.*?)Server Built:", r"Server Version:(.*)"
        )
    server_version = remove_html_tags(server_version)

    server_mpm = find_info_smart_lines(
        content, r"Server MPM:(.*?)Server Built:", r"Server MPM:(.*)"
    )
    server_mpm = remove_html_tags(server_mpm)

    server_built = find_info_smart_lines(
        content, r"Server Built:(.*?)<hr", r"Server Built:(.*)"
    )
    server_built = remove_html_tags(server_built)

    return server_version, server_mpm, server_built


def extract_heading(content):
    heading = find_info_smart_lines(
        content,
        r"<h1>Apache Server Status for(.*?)</h1>",
        r"Apache Server Status for(.*)",
    )
    heading = remove_html_tags(heading)
    if heading is None:
        return None, None, None

    # split heading into endpoint and via_part
    if "(via" in heading:
        endpoint, via_part = heading.split("(via")
        endpoint = endpoint.strip()
        via_part = via_part.strip()
        if via_part[-1] == ")":
            via_part = via_part[:-1].strip()
    else:
        endpoint = heading
        via_part = None

    return "Apache Server Status for " + heading, endpoint, via_part


def extract_scoreboard(content):
    # check if scorebaord exists
    if re.search(r"Scoreboard Key:", content):
        # remove newlines (to make scoreboard easier to read and parse)
        content_no_newlines = re.sub("\n", "", content)
        # first, check if scoreboard is in a <pre> tag
        scoreboard = find_info_in_text(
            content_no_newlines, r"<pre>(.*?)Scoreboard Key:", True
        )

        not_allowed = [
            "apache server status",
            "current time",
            "server version",
            "server built",
        ]
        # if any of the not allowed are in the scoreboard, then it is not the scoreboard
        if scoreboard is not None and any(
            [na in scoreboard.lower() for na in not_allowed]
        ):
            scoreboard = None

        # scoreboard is not in a <pre> tag (simple page layout) so we need to find it in a "bruteforce" manner
        if scoreboard is None:
            # check if there is "idle workers" then some characters, then a sequence of only scoreboard characters (_.SRWKDCLGI) followed by "Scoreboard Key:" and get last such sequence
            scoreboard = find_info_in_text(
                content_no_newlines,
                r"idle workers.*?([_\.SRWKDCLGI]+)(?=.*Scoreboard Key:)",
                True,
                match_idx=-1,
            )

        # if no match was still found, try relaxing the last constraint by removing the lookahead (but this might produce false positives)
        if scoreboard is None:
            scoreboard = find_info_in_text(
                content_no_newlines,
                r"([_\.SRWKDCLGI]+)(?=.*Scoreboard Key:)",
                True,
                match_idx=-1,
            )
            if scoreboard is not None:
                print(
                    f"Relaxed scoreboard match was found (might not be correct please double check."
                )

        return remove_html_tags(scoreboard)
    else:
        return None


def extract_aggregated_stats(stats_list):
    stats_problems = []
    final_stats = {}
    for agg_stat in stats_list:
        if agg_stat == "":
            continue  # skip empty lines
        agg_stat = agg_stat.strip()
        lower_agg_stat = agg_stat.lower()
        if "idle workers" in lower_agg_stat:
            # split idle workers line by ","
            values = agg_stat.split(",")

            # split idle workers line with regex by finding [num] [words]
            for value in values:
                value = value.strip()
                matches = re.findall(r"(\d+) (.+)", value)
                if len(matches) == 0:
                    stats_problems.append(
                        f"Couldn't parse part of idle workers line: {value}"
                    )
                else:
                    if len(matches) > 1:
                        stats_problems.append(
                            f"Multiple matches found for agg stats {value}. Using the first one."
                        )
                    num, word = matches[0]
                    final_stats[word] = num
        elif "total accesses" in lower_agg_stat or "total traffic" in lower_agg_stat:
            # parse total accesses/traffic line by splitting by "-"
            agg_stat = agg_stat.split(" - ")
            for substat in agg_stat:
                substat = substat.split(":", 1)
                if len(substat) == 2:
                    key, value = substat
                    final_stats[key] = value
                else:
                    stats_problems.append(
                        f"Couldn't parse part of total accesses/traffic line: {substat}"
                    )
        elif "cpu usage" in lower_agg_stat:
            # CPU Usage/Load line
            match = re.search(
                r"CPU Usage:\s*(\S+.*?)\s-\s+(\S+.*?)CPU Load", agg_stat, re.IGNORECASE
            )
            if match:
                final_stats["CPU Usage"] = match.group(1)
                final_stats["CPU Load"] = match.group(2)
                # check if line consists only of cpu usage and cpu load
                if not (
                    lower_agg_stat.startswith("cpu usage")
                    and lower_agg_stat.endswith("cpu load")
                ):
                    stats_problems.append("irregular CPU Usage/Load line")
            else:
                match = re.search(r"CPU Usage:\s*(\S+.*)", agg_stat, re.IGNORECASE)
                if match:
                    final_stats["CPU Usage"] = match.group(1)
                else:
                    stats_problems.append(
                        f"Couldn't parse CPU Usage/Load line: {agg_stat}"
                    )
        elif "requests/sec" in lower_agg_stat or "/request" in lower_agg_stat:
            # requests stats line
            # .0377 requests/sec - 140 B/second - 3726 B/request
            # split line by "-" and parse each part
            rstats_line = agg_stat.split(" - ")
            if len(rstats_line) == 0:
                stats_problems.append(f"Couldn't parse requests stats line: {agg_stat}")
            for rstat in rstats_line:
                # regex format (number) (unit) where number can be 4, -4, 4.5, 4.5e-5, etc.
                match = re.search(
                    r"([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\s+([a-zA-Z/]+)", rstat
                )
                if match:
                    final_stats[match.group(2)] = match.group(1)
                else:
                    stats_problems.append(
                        f"Couldn't parse requests stats part: {rstat}"
                    )
        else:
            # general rule for parsing lines
            result = agg_stat.split(":", 1)
            if len(result) == 2:
                key, value = result
                final_stats[key.lower().strip()] = value
            else:
                stats_problems.append(f"Couldn't parse agg stats line: {agg_stat}")

    # strip all keys, and values and make keys lowercase
    temp_dict = final_stats.copy()
    final_stats = {}
    for key, value in temp_dict.items():
        final_stats[key.strip().lower()] = value.strip()
    del temp_dict

    return final_stats, stats_problems


def parse_ss_page_from_tags(content):
    soup_content = BeautifulSoup(content, "html.parser")
    problems = []

    # extract heading
    h1_tags = soup_content.find_all("h1")
    if len(h1_tags) == 0:
        problems.append("No h1 tags found.")
    elif len(h1_tags) >= 2:
        problems.append(
            f"Multiple h1 tags found. ({[h1.get_text(strip=True) for h1 in h1_tags]})"
        )
    heading, endpoint, via_part = extract_heading(content)

    server_version, server_mpm, server_built, aggregated_stats = None, None, None, None
    # find all dl tags
    dl_tags = soup_content.find_all("dl")
    for dl in dl_tags:
        str_dl_lower = str(dl).lower()
        soup_dl = BeautifulSoup(str_dl_lower, "html.parser")
        dt_tags = soup_dl.find_all("dt")
        if "server version" in str_dl_lower or "server built" in str_dl_lower:
            # parse server info section
            server_version, server_mpm, server_built = extract_server_info(str(dl))
        elif "current time" in str_dl_lower:
            # parse aggregated stats (if dt tag has more than one opening <dt> then it is missing a closing dt so we get it until the next opening <dt>)
            aggregated_stats = [
                (
                    remove_html_tags(str(dt).split("<dt>", 2)[1])
                    if str(dt).count("<dt>") > 1
                    else dt.get_text(strip=True)
                )
                for dt in dt_tags
            ]
            aggregated_stats, stats_problems = extract_aggregated_stats(
                aggregated_stats
            )
            problems.extend(stats_problems)
        else:
            problems.append(f"Unknown dl section found")

    # get scoreboard
    scoreboard = extract_scoreboard(content)

    # find all tables
    tables = soup_content.find_all("table")
    tables = [str(table) for table in tables]

    workers_table = None
    for i, table in enumerate(tables):
        has_client = re.search(
            r"<th[^>]*>.*?Client.*?</th>", table, re.IGNORECASE | re.DOTALL
        )
        has_vhost = re.search(
            r"<th[^>]*>.*?VHost.*?</th>", table, re.IGNORECASE | re.DOTALL
        )
        is_workers_table = has_client and has_vhost
        if is_workers_table:
            if workers_table is not None:
                problems.append(
                    f"Multiple workers tables found. Using the first one found."
                )
                break
            else:
                workers_table = table

    if workers_table is not None:
        soup_workers_table = BeautifulSoup(workers_table, "html.parser")
        # parse table html contents
        headers = [
            header.get_text(strip=True) for header in soup_workers_table.find_all("th")
        ]
        rows = []
        for i, row in enumerate(soup_workers_table.find_all("tr")):
            values = [cell.get_text(strip=True) for cell in row.find_all(["td", "th"])]
            if len(values) != len(headers):
                problems.append(
                    f"Row {i} of workers table has different number of columns than headers ({len(values)} != {len(headers)})."
                )
                continue
            if values:
                rows.append(values)
        assert all(
            [row == header for row, header in zip(rows[0], headers)]
        ), "Row 0 doesn't match headers"
        rows = rows[1:]  # remove header row
        workers_table = pd.DataFrame(rows, columns=headers)
    else:
        pass  # no workers table found (workers_table is None)

    return {
        "heading": heading,
        "endpoint": endpoint,
        "via_part": via_part,
        "server_version": server_version,
        "server_mpm": server_mpm,
        "server_built": server_built,
        "aggregated_stats": aggregated_stats,
        "scoreboard": scoreboard,
        "workers_table": workers_table,
        "problems": problems,
    }


def extract_info_from_html(content):
    if len(BeautifulSoup(content, "html.parser").find_all("h1")) == 0:
        # simple page (no html tags so harder to parse)

        problems = []

        heading, endpoint, via_part = extract_heading(content)

        server_version, server_mpm, server_built = extract_server_info(content)

        # get aggregated stats section (all text from "Current Time" to "idle workers" including)
        aggregated_stats = find_info_in_text(
            content, r"Current Time:.*?idle workers", True
        )
        aggregated_stats = remove_html_tags(aggregated_stats)
        if aggregated_stats is not None:
            aggregated_stats = aggregated_stats.split("\n")  # split stats per line
            aggregated_stats, stats_problems = extract_aggregated_stats(
                aggregated_stats
            )
            problems.extend(stats_problems)

        scoreboard = extract_scoreboard(content)

        return {
            "heading": heading,
            "endpoint": endpoint,
            "via_part": via_part,
            "server_version": server_version,
            "server_mpm": server_mpm,
            "server_built": server_built,
            "aggregated_stats": aggregated_stats,
            "scoreboard": scoreboard,
            "workers_table": None,
            "problems": problems,
        }
    else:
        # easier to parse page through html tags
        return parse_ss_page_from_tags(content)
