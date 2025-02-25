import re


def remove_html_tags(text):
    if text is None:
        return None
    return re.sub(r"<[^\s>]*[\w]+>", "", text).strip()


def find_info_in_text(text, pattern, match_across_newlines=True, match_idx=0):
    matches = re.findall(
        pattern, text, re.IGNORECASE | re.DOTALL if match_across_newlines else 0
    )
    if not matches:
        return None
    if match_idx is None:
        return matches
    if len(matches) > 1:
        print(f"Multiple matches found for {pattern}. Using index {match_idx}.")
    return matches[match_idx]


def find_info_smart_lines(text, pattern_newline, pattern_no_newline, match_idx=0):
    info = find_info_in_text(
        text, pattern_newline, match_across_newlines=True, match_idx=match_idx
    )
    if info is None and pattern_no_newline is not None:
        info = find_info_in_text(
            text, pattern_no_newline, match_across_newlines=False, match_idx=match_idx
        )
    return info
