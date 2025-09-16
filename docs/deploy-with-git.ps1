param(
  [Parameter(Mandatory)][string]$GitHubUser,
  [Parameter(Mandatory)][string]$RepoName
)

# Ensure Git identity
if (-not (git config --global user.name)) {
  git config --global user.name "Your Name"
  git config --global user.email "you@yourdomain.com"
}

$projectRoot = Get-Location
$repoPath    = Join-Path $projectRoot $RepoName
$distDir     = Join-Path $projectRoot 'dist'
$docsDir     = Join-Path $repoPath 'docs'
$remote      = "https://github.com/$GitHubUser/$RepoName.git"
$pagesUrl    = "https://$GitHubUser.github.io/$RepoName"

Write-Host "Cloning/updating repo $RepoName..." -ForegroundColor Cyan
if (-not (Test-Path $repoPath)) {
  git clone $remote
} else {
  Push-Location $repoPath
  git pull origin main
  Pop-Location
}

Write-Host "Mirroring dist/ → docs/ (excluding .vs)..." -ForegroundColor Cyan
# Remove old docs
if (Test-Path $docsDir) { Remove-Item $docsDir -Recurse -Force }
# Use robocopy to skip .vs folder
robocopy $distDir $docsDir /E /XD "$distDir\.vs"

Write-Host "Updating manifest URLs to $pagesUrl..." -ForegroundColor Cyan
$manifestPath = Join-Path $docsDir 'manifest.xml'
$content = Get-Content $manifestPath -Raw
$content = $content -replace 'https://localhost:8080', $pagesUrl
Set-Content $manifestPath -Value $content -Encoding UTF8

Write-Host "Committing & pushing changes..." -ForegroundColor Cyan
Push-Location $repoPath
git add docs
git commit -m "Deploy to GitHub Pages at $pagesUrl" --allow-empty
git push origin main
Pop-Location

Write-Host "`n✅ Deployment complete! Verify:" -ForegroundColor Green
Write-Host "  $pagesUrl/manifest.xml`n"
Write-Host "Then go to your repo’s Settings → Pages, set Source to main/docs, Save."
Write-Host "Finally, upload that manifest URL in the Microsoft 365 Admin Center."
