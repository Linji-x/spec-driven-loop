$ErrorActionPreference = 'Stop'

$RepositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$BuildScript = Join-Path $RepositoryRoot 'scripts\build_release.py'

if (Get-Command python -ErrorAction SilentlyContinue) {
    & python $BuildScript
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    & py $BuildScript
} else {
    throw 'Python 3 is required to build release archives.'
}

if ($LASTEXITCODE -ne 0) {
    throw "Release build failed with exit code $LASTEXITCODE."
}
