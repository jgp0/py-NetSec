# Definimos los parámetros
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

# Validamos los parámetros
if (-not ($UserName -and $EmailAddress -and $Department -and $JobTitle -and $Password)) {
    throw "Faltan los parámetros de entrada requeridos"
}

# Validamos la contraseña
$passwordString = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($Password))
$isValidPassword = $false
if ($passwordString -match "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\da-zA-Z]).{8,}$") {
    $isValidPassword = $true
}

if (-not $isValidPassword) {
    Write-Host "La contraseña no es válida. Debe contener al menos 8 caracteres, incluyendo mayúsculas, minúsculas, números y caracteres especiales"
    return
}

# Generamos una contraseña segura
$securePassword = ConvertTo-SecureString -String $passwordString -AsPlainText -Force

# Creamos un nuevo usuario en Active Directory
try {
New-ADUser -Name $UserName -SamAccountName $UserName -UserPrincipalName "$UserName@yourdomain.com" -EmailAddress $EmailAddress -Department $Department -Title $JobTitle 
-AccountPassword $securePassword -Enabled $true
} catch {
Write-Host "No se pudo crear la cuenta de usuario debido al siguiente error: $"
}

# Añadimos al usuario a su respectivo grupo y departamento
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

Write-Host "El usuario $UserName ha sido creado correctamente"