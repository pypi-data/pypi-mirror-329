# WiFlip repository  
All python source files of WiFlip.

WiFlip is an application that communicates with any PPS4 Clone through wifi.  
The main benefit of wiflip is game reprogramming (on Recel System 3 MPU Clones) 
One can also emulate the switch matrix of the pinball or test the pysical switches of the pin one by one.

Miniprinter emulation is available, so that one can modify the non volatile ram. 

Coils can be checked individually.

Replication of the display, on a PC or Mac, allows you for diagnosing the real displays.

Additional protections are available for coils.

# Prerequisites  
## Python libraries  
1. pyqt5==5.15.11
2. requests
3. bs4

   
# Make an executable with pyinstaller  
That's as easy as bonjour:  
`pyinstaller wiflip.spec`

[wiflip.spec](https://github.com/garzol/wiflip/blob/tracer/wiflip.spec) resides in this repo.
# Signing the executable (PC)
All informations collected from there:  
https://gist.github.com/PaulCreusy/7fade8d5a8026f2228a97d31343b335e
> :warning: **Warning**  
> Signing the executable will not prevent Windows smartscreen from complaining harshly about the resulting binary. You also have to get on board with Microsoft's developpers plan. And even if you do, it could still complain.

### Create certificate
```Powershell
New-SelfSignedCertificate -Type Custom -Subject "CN=AA55 consulting, E=phd@aa55.fr" -KeyUsage DigitalSignature -FriendlyName "WiFlip" -CertStoreLocation "Cert:\CurrentUser\My" -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.3", "2.5.29.19={text}") -NotAfter "samedi 30 novembre 2028 14:44:59"
```

The date for not after can be deduced from powershell command `get-date`

To see if the command succeeded, enter the following commands :

```Powershell
Set-Location Cert:\CurrentUser\My
Get-ChildItem | Format-Table FriendlyName, Thumbprint, Subject
```

Save the thumbprint displayed next to the name of your certificate, you will need it for the next step.

### Export the certificate

```Powershell
$password = ConvertTo-SecureString -String "pwd" -Force -AsPlainText 
Export-PfxCertificate -cert "Cert:\CurrentUser\My\<YourThumbprint>" -FilePath certificate.pfx -Password $password
```
### Sign the exe
```Powershell
signtool sign /f .\certificate.pfx /p "pwd" /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 wiflip.exe
``` 

# Make a Windows installer with innosetup
## Signing the installer too
The script contains the following lines:  
```
[Setup]
SignTool=signtool
```

`signtool` is the name of the powershell command that must be given from the menu tools>configure sign tool, such as:
```
"signtool.exe" sign /f "C:\Users\garzo\git\wiflip2\dist\certificatel.pfx" /fd SHA256 /t http://timestamp.comodoca.com/authenticode /p "pwd" $f
```
> :warning: **Warning**  
> Look at the difference between the two signing commands: The latter does not contain  `/td SHA256`.

# Checking the executable's digest
Starting from dec 1st, 2024, all WiFlip exes will be delivered as links for an installer with the supplied self-signing certificatel.pfx. The hash of the app will also be communicated. 

With this measures taken, there are good probabilities that the integrity of the code be preserved, even though you never know.

But, well, you can check the hash, you can check and/or install the certificate from here. That's not nothing!

Checking the hash, as follows:  
```Powershell
Get-FileHash .\wiflip.exe -Algorithm SHA256 | Format-List
```


