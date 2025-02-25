# Parser for the `/server-status` page of an Apache server

`server-status-parser` is a simple Python package that parses the output of the `/server-status` page of an Apache server. 

The package is **not intended to parse the `?auto` version** of the page as it is already in a machine-readable format. `server-status-parser` is made to parse the normal version of the `/server-status` page and extract as much of the content as possible. This includes the workers table which under `?auto` is not available.

## Installation

```shell
pip install server-status-parser
```


## Usage

```python
from server_status_parser import extract_info_from_html

with open('server_status.html', 'r') as f:
    content = f.read()

parsed_content = extract_info_from_html(content)
print(parsed_content)
```

### Example Page
If we have a page like the one shown below, we can parse it using the `server-status-parser` package. The output is shown underneath.

<img src="https://raw.githubusercontent.com/kolevvelyan/server-status-parser/main/images/page_example.png" alt="apache server status page example" width="600">

### Output from the Parser
> ```
> {
>     'heading': 'Apache Server Status for google.com (via 127.0.0.1)',
>     'endpoint': 'google.com',
>     'via_part': '127.0.0.1',
>     'server_version': 'Apache/2.4.62 (Win64)',
>     'server_mpm': 'WinNT\nApache Lounge VS17',
>     'server_built': None,
>     'aggregated_stats': {
>         'current time': 'Monday, 24-Feb-2025 16:29:45 W. Europe Standard Time',
>         'restart time': 'Monday, 24-Feb-2025 16:05:19 W. Europe Standard Time',
>         'parent server config. generation': '1',
>         'parent server mpm generation': '0',
>         'server uptime': '24 minutes 25 seconds',
>         'server load': '-1.00 -1.00 -1.00',
>         'total accesses': '5',
>         'total traffic': '6 KB',
>         'total duration': '8',
>         'requests/sec': '00341',
>         'b/second': '4',
>         'b/request': '1228',
>         'ms/request': '1.6',
>         'requests currently being processed': '1',
>         'workers gracefully restarting': '0',
>         'idle workers': '63'
>     },
>     'scoreboard': '___________________________________________W____________________',
>     'workers_table': pd.DataFrame( Srv  PID   ...       VHost               Request 
>                                0  0-0  11288  ...  localhost:9090  GET /server-status HTTP/1.1),
>     'problems': []
> }
> ```

## Content that is Currently NOT PARSED

Some contents of the page are not currently parsed as we do not consider them important and hence worth investing time.
### TLS Cache Section

This section appears near the end of the page and shows the status of the TLS cache.

<img src="https://raw.githubusercontent.com/kolevvelyan/server-status-parser/main/images/tls_cache.png" alt="tls cache section example" width="400">

### `mod_fcgid`

This section appears below the workers table when `mod_fcgid` is enabled.

<img src="https://raw.githubusercontent.com/kolevvelyan/server-status-parser/main/images/mod_fcgid.png" alt="mod_fcgid section example" width="300">


### `GnuTLS`

This section appears below the workers table when `mod_gnutls` is enabled.

<img src="https://raw.githubusercontent.com/kolevvelyan/server-status-parser/main/images/gnu_tls.png" alt="gnu tls section example" width="400">

### Slot Table

This table appears above the scoreboard.

<img src="https://raw.githubusercontent.com/kolevvelyan/server-status-parser/main/images/slot_table.png" alt="slot table example" width="500">

### Plaintext Workers Table

Very rarely we have found that the workers table is in plaintext format in stead of being properly formatted as an HTML table. This is not parsed.

<img src="https://raw.githubusercontent.com/kolevvelyan/server-status-parser/main/images/plaintext_workers_table.png" alt="plaintext workers table example" width="600">
