# Google Drive folder ID
$folderID = "11f_gsqnwHH1Iq9WUzKZNqF8IJ3pRWoeR"

$modelFiles = @(
    @{ name = "potato.keras"; dest = "models/disease" },
    @{ name = "tomato.keras"; dest = "models/disease" },
    @{ name = "maize.keras"; dest = "models/disease" },
    @{ name = "yolo_leaf_best.pt"; dest = "models/yolo" },
    @{ name = "yolo_lesion_best.pt"; dest = "models/yolo" },
    @{ name = "u2net.pth"; dest = "models/u2net" }
)

Write-Host "This script will download model weights from Google Drive, compute checksums, and prepare a local git commit (will NOT push)." -ForegroundColor Cyan

# Check if gdown is installed
try {
    $gdwnVer = python -m pip show gdown 2>&1 | Select-String "Version"
    Write-Host "gdown found: $gdwnVer" -ForegroundColor Green
} catch {
    Write-Host "gdown not found. Installing..." -ForegroundColor Yellow
    python -m pip install gdown
}

# Create model directories
foreach ($m in $modelFiles) {
    $dir = $m.dest
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

Write-Host "Downloading files from Google Drive folder..."
python -m gdown --folder-id $folderID --quiet

# Organize downloaded files into proper subfolders (if gdown downloaded folder structure)
if (Test-Path $folderID) {
    Write-Host "Organizing files into models/ subdirectories..."
    $dlFolder = $folderID
    
    foreach ($m in $modelFiles) {
        $filename = $m.name
        $destdir = $m.dest
        $source = Join-Path $dlFolder $filename
        $target = Join-Path $destdir $filename
        
        if (Test-Path $source) {
            Move-Item -Path $source -Destination $target -Force
            Write-Host "Moved $filename to $destdir" -ForegroundColor Green
        }
    }
    
    Remove-Item -Recurse -Force $dlFolder
}

# Compute checksums
$checksumFile = "models/checksums.txt"
if (Test-Path $checksumFile) { Remove-Item $checksumFile }
foreach ($m in $modelFiles) {
    $filepath = Join-Path $m.dest $m.name
    if (Test-Path $filepath) {
        $hash = Get-FileHash -Algorithm SHA256 -Path $filepath
        "$($hash.Hash)  $filepath" | Out-File -FilePath $checksumFile -Append -Encoding utf8
    }
}

Write-Host "Checksums written to $checksumFile" -ForegroundColor Green

# Ensure Git LFS is initialized
Write-Host "Ensuring Git LFS is initialized and .gitattributes present..."
git lfs install

Write-Host "Files downloaded. Review changes. Commit now? (Y/N)" -NoNewline
$resp = Read-Host
if ($resp -match '^[Yy]') {
    git add models .gitattributes models/checksums.txt WEIGHTS_URLS.md
    git commit -m "Add model weights (via gdown) and checksums"
    Write-Host "Committed locally. Run 'git push' when ready." -ForegroundColor Green
} else {
    Write-Host "Skipped commit. Files are downloaded locally in 'models/'." -ForegroundColor Yellow
}
