# Obtener la lista de usuarios existentes en AD
$users = Get-ADUser -Filter *

# Mostrar la lista de usuarios con un número de índice
for ($i=0; $i -lt $users.Count; $i++) {
    Write-Host "$i. $($users[$i].Name)"
}

# Pedir al usuario que seleccione un usuario para eliminar
$userIndex = Read-Host "Seleccione un usuario para eliminar ingresando su número de índice:"

# Obtener el usuario seleccionado
$selectedUser = $users[$userIndex]

# Solicitar confirmación para eliminar el usuario
$confirm = Read-Host "¿Está seguro que desea eliminar $($selectedUser.Name)? (S/N)"

if ($confirm.ToLower() -eq "s") {
    
   
    # Eliminar el usuario seleccionado
    Remove-ADUser -Identity $selectedUser -Confirm:$false
    Write-Host "El usuario $($selectedUser.Name) ha sido eliminado correctamente."
} else {
    Write-Host "La eliminación del usuario $($selectedUser.Name) ha sido cancelada."
}
