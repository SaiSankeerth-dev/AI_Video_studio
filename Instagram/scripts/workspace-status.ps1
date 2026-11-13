$ErrorActionPreference = "Stop"

$script = @'
export PATH="$HOME/.local/bin:$PATH"
echo "=== Versions ==="
echo "node: $(node --version)"
echo "npm: $(npm --version)"
echo "python3: $(python3 --version)"
echo "uv: $(uv --version)"
echo "yt-dlp: $(yt-dlp --version)"
echo "opencli: $(opencli --version)"
echo ""
echo "=== OpenCLI Doctor ==="
opencli doctor
echo ""
echo "=== Agent Reach Browser Status ==="
agent-reach browser status
echo ""
echo "=== Agent Reach Doctor ==="
agent-reach doctor --text
'@

$script | wsl -d Ubuntu -- bash -c "tr -d '\r' | bash -s"
