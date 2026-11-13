param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Url,

    [ValidateSet("auto", "instagram", "youtube", "other")]
    [string]$Platform = "auto"
)

$ErrorActionPreference = "Stop"

if ($Platform -eq "auto") {
    if ($Url -match "instagram\.com") {
        $Platform = "instagram"
    } elseif ($Url -match "(youtube\.com|youtu\.be)") {
        $Platform = "youtube"
    } else {
        $Platform = "other"
    }
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$baseDir = Split-Path -Parent $scriptDir
$winOutDir = Join-Path $baseDir "downloads\$Platform"
New-Item -ItemType Directory -Force -Path $winOutDir | Out-Null
$driveLetter = ($baseDir.Substring(0, 1)).ToLower()
$wslPath = $baseDir.Substring(2).Replace('\', '/')
$wslOutDir = "/mnt/$driveLetter$wslPath/downloads/$Platform"

$env:TARGET_URL = $Url
$env:WSL_OUT_DIR = $wslOutDir
$env:WSLENV = "TARGET_URL/u:WSL_OUT_DIR/u"

$script = @'
export PATH="$HOME/.local/bin:$PATH"
yt-dlp --no-warnings -o "$WSL_OUT_DIR/%(id)s.%(ext)s" "$TARGET_URL"
'@

$script | wsl -d Ubuntu -- bash -c "tr -d '\r' | bash -s"
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
Write-Host "Saved to $winOutDir"
