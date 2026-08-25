$ErrorActionPreference = 'Stop'

$RepositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$SyncScript = Join-Path $RepositoryRoot 'scripts\sync_plugin_skill.py'

if (Get-Command python -ErrorAction SilentlyContinue) {
    & python $SyncScript
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    & py $SyncScript
} else {
    throw 'Python 3 is required to synchronize the plugin skill mirror.'
}

if ($LASTEXITCODE -ne 0) {
    throw "Skill synchronization failed with exit code $LASTEXITCODE."
}
