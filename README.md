# TTS Pastebin Proxy

Redirects Steam game Pastebin requests to `pastebinp.com` to bypass regional blocks or connectivity issues.

## How to Use

1.  **Clone** this repository to a safe folder.
2.  **Run the setup script**:
    *   **Linux**: Run `linux/setup.sh`
    *   **Windows**: Run `windows/setup.bat`
3.  **Configure Steam**:
    *   The setup script will provide a command (e.g., `"/path/to/launcher.sh" %command%`).
    *   Copy this command.
    *   Right-click your game in Steam -> **Properties** -> **General** -> **Launch Options**.
    *   Paste the command there.

## How it Works
The proxy interceptor runs a local multi-threaded server that captures HTTP/HTTPS requests, specifically rewriting any `pastebin.com` traffic to use the `pastebinp.com` mirror while forwarding all other traffic (like Steam downloads) as-is.
