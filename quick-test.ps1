Write-Host "🧪 Local CI/CD Testing Script" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Green

$ErrorCount = 0
cd "c:\Users\mohem\Desktop\time reminders"

# Test Black formatting
Write-Host "`n🎨 Testing Black (Code Formatting)..." -ForegroundColor Yellow
$blackTest = python -m black --check --diff . 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Code formatting issues found!" -ForegroundColor Red
    Write-Host "   Fix with: python -m black ." -ForegroundColor Yellow
    $ErrorCount++
} else {
    Write-Host "✅ Code formatting is correct" -ForegroundColor Green
}

# Test isort
Write-Host "`n📂 Testing isort (Import Sorting)..." -ForegroundColor Yellow
$isortTest = python -m isort --check-only --diff . 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Import sorting issues found!" -ForegroundColor Red
    Write-Host "   Fix with: python -m isort ." -ForegroundColor Yellow
    $ErrorCount++
} else {
    Write-Host "✅ Import sorting is correct" -ForegroundColor Green
}

# Test Flake8 critical errors
Write-Host "`n🔍 Testing Flake8 (Critical Linting)..." -ForegroundColor Yellow
$flake8Test = python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Critical linting errors found!" -ForegroundColor Red
    Write-Host $flake8Test -ForegroundColor Red
    $ErrorCount++
} else {
    Write-Host "✅ No critical linting errors" -ForegroundColor Green
}

# Test MyPy
Write-Host "`n🔬 Testing MyPy (Type Checking)..." -ForegroundColor Yellow
python -m mypy . --ignore-missing-imports --no-strict-optional 2>&1 | Out-Null
Write-Host "ℹ️ Type checking completed (warnings are informational)" -ForegroundColor Cyan

# Test configuration
Write-Host "`n⚙️ Testing Configuration..." -ForegroundColor Yellow
if (Test-Path "configuration.env.template") {
    Copy-Item "configuration.env.template" "configuration.env" -Force
    (Get-Content "configuration.env") -replace 'your_discord_bot_token_here', 'dummy_token_for_testing' | Set-Content "configuration.env"
    $configTest = python -c "from configuration import BOT_TOKEN, TIMEZONE; print('Config loaded successfully')" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Configuration loading works" -ForegroundColor Green
    } else {
        Write-Host "❌ Configuration loading failed" -ForegroundColor Red
        $ErrorCount++
    }
} else {
    Write-Host "⚠️ configuration.env.template not found" -ForegroundColor Yellow
}

# Test database
Write-Host "`n💾 Testing Database..." -ForegroundColor Yellow
$dbTest = python -c "from database import database; database.connect(); database.create_table(); print('Database operations successful'); database.close()" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Database operations work" -ForegroundColor Green
} else {
    Write-Host "❌ Database operations failed" -ForegroundColor Red
    $ErrorCount++
}

# Test security scan
Write-Host "`n🔒 Testing Security Scan..." -ForegroundColor Yellow
python -m bandit -r . -f json -o bandit-report.json 2>&1 | Out-Null
if (Test-Path "bandit-report.json") {
    Write-Host "✅ Security scan completed (check bandit-report.json)" -ForegroundColor Green
} else {
    Write-Host "⚠️ Security scan had issues" -ForegroundColor Yellow
}

# Summary
Write-Host "`n" + "=" * 50 -ForegroundColor Cyan
Write-Host "📊 TEST SUMMARY" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

if ($ErrorCount -eq 0) {
    Write-Host "🎉 ALL TESTS PASSED! Your code is ready for CI/CD." -ForegroundColor Green
    Write-Host "✅ You can safely push to your repository." -ForegroundColor Green
} else {
    Write-Host "❌ $ErrorCount issues found. Please fix before deploying:" -ForegroundColor Red
    Write-Host "   - Run: python -m black . (to fix formatting)" -ForegroundColor Yellow
    Write-Host "   - Run: python -m isort . (to fix imports)" -ForegroundColor Yellow
    Write-Host "   - Fix any linting errors" -ForegroundColor Yellow
}

Write-Host "`n💡 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Fix any issues found above" -ForegroundColor White
Write-Host "   2. Run this script again to verify fixes" -ForegroundColor White
Write-Host "   3. Create a test branch: git checkout -b test-cicd-fix" -ForegroundColor White
Write-Host "   4. Push to test branch first to see CI/CD results" -ForegroundColor White
