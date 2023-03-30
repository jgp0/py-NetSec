# Define input parameters
param(
    [Parameter(Mandatory=$true)]
    [string]$UserName,

    [Parameter(Mandatory=$true)]
    [string]$EmailAddress,

    [Parameter(Mandatory=$true)]
    [string]$Department,

    [Parameter(Mandatory=$true)]
    [string]$JobTitle,

    [Parameter(Mandatory=$true)]
    [SecureString]$Password
)

# Validate input parameters
if (-not ($UserName -and $EmailAddress -and $Department -and $JobTitle -and $Password)) {
    throw "Missing required input parameter(s)"
}

# Validate the password
$passwordString = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($Password))
$isValidPassword = $false
if ($passwordString -match "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\da-zA-Z]).{8,}$") {
    $isValidPassword = $true
}

if (-not $isValidPassword) {
    Write-Host "Password is not valid. It must contain at least 8 characters, including uppercase, lowercase, numbers, and special characters."
    return
}

# Generate secure password
$securePassword = ConvertTo-SecureString -String $passwordString -AsPlainText -Force

# Create new user account in Active Directory
try {
New-ADUser -Name $UserName -SamAccountName $UserName -UserPrincipalName "$UserName@yourdomain.com" -EmailAddress $EmailAddress -Department $Department -Title $JobTitle -AccountPassword $securePassword -Enabled $true
} catch {
Write-Host "Failed to create user account due to the following error: $"
}

# Add user to appropriate groups based on department and job title
$groupNames = @()
if ($Department -eq "Sales") {
$groupNames += "Sales Group"
} elseif ($Department -eq "Marketing") {
$groupNames += "Marketing Group"
}

if ($JobTitle -eq "Manager") {
$groupNames += "Managers Group"
}

foreach ($groupName in $groupNames) {
Add-ADGroupMember -Identity $groupName -Members $UserName
}

Write-Host "User account $UserName has been created successfully"