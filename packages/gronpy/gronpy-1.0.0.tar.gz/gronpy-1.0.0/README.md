# Gronpy

A Python port of [gron](https://github.com/tomnomnom/gron/) to make JSON greppable.

## Installation

The recommended way to install is to use `pipx`:

`pipx install gronpy`

## Usage

```
 % gronpy --help

 Usage: gronpy [OPTIONS] [INPUT_PATH]

╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   input_path      [INPUT_PATH]  Input file path or URL. If not specified uses stdin. [default: (stdin)]                                                           │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --gron                    --ungron                                       Transform JSON into GRON or back again [default: gron]                                   │
│ --color                   --no-color                                     Enable colouring in terminal. [default: color]                                           │
│ --user-agent          -u                TEXT                             Set custom User-Agent header for HTTP requests [default: None]                           │
│ --user-agent-random                                                      Use a random User-Agent header                                                           │
│ --timeout             -t                INTEGER                          Timeout in seconds for HTTP requests [default: 30]                                       │
│ --version             -v                                                                                                                                          │
│ --install-completion                    [bash|zsh|fish|powershell|pwsh]  Install completion for the specified shell. [default: None]                              │
│ --show-completion                       [bash|zsh|fish|powershell|pwsh]  Show completion for the specified shell, to copy it or customize the installation.       │
│                                                                          [default: None]                                                                          │
│ --help                                                                   Show this message and exit.                                                              │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Example

```
% gronpy "https://api.tvmaze.com/schedule?country=GB" | grep "show.name" | grep -i "news"
json[34].show.name = "Newsround";
json[40].show.name = "Channel 4 News Summary";
json[43].show.name = "BBC News at One";
json[44].show.name = "ITV Lunchtime News";
json[45].show.name = "5 News Lunchtime";
json[53].show.name = "5 News";
json[56].show.name = "BBC News at Six";
json[58].show.name = "ITV Evening News";
json[59].show.name = "Channel 4 News";
json[76].show.name = "ITV News at Ten";
json[77].show.name = "Newsnight";
```
