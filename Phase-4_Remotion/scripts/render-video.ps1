# Render Remotion Cinematic Master Video
param (
    [string]$Composition = "Documentary",
    [string]$OutputFile = "D:\ContentFactory\projects\video-001\remotion\renders\master-video-v1.mp4"
)

Write-Host "Rendering $Composition to $OutputFile..."
npx remotion render src/index.ts $Composition $OutputFile --overwrite

if ($LASTEXITCODE -eq 0) {
    Write-Host "Render successful: $OutputFile" -ForegroundColor Green
} else {
    Write-Host "Render failed with exit code $LASTEXITCODE" -ForegroundColor Red
}
