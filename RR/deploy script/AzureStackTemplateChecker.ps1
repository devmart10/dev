param (
    #At the minimum, one of these two parameters needs to be set (Domain Name is easier to know - myFQDN.onmicrosoft.com) 
    [String]$AzureStackAADDefaultDomainName = "devmart10gmail.onmicrosoft.com",
    [String]$AzureStackAADTenantID = "",
    #These parameters can be left like this, when using the Azure Stack POC environment
    [String]$AzureStackEnvironmentName= "Azure Stack",
    [String]$AzureStackEnvironmentFQDN= "azurestack.local",
    [String]$AzureStackSubscriptionName = "Default Provider Subscription",
    [String]$GARPath = "\\sofs\Share\CRP\GuestArtifactRepository",
    [String]$PIRPath = "\\sofs\Share\CRP\PlatformImages",
    #These parameters can be specified here or in the command line, if you want to avoid picking the template manually
    [String]$TemplatePath = ".",
    [String]$TemplateName = "template.json",
    #These parameters are used to determine how the script behaves in certain situations
    [bool]$CheckVMExtensions = $true,
    [bool]$CheckPlatformImages = $true,
    [string]$ResourceGroupName = "",
    [bool]$AutoPickResourceGroup = $true,
    [bool]$ValidateTemplateWithDefaultCmdlet = $true,
    [bool]$AlwaysSkipManualParameterEntry = $true,
    [Bool]$ListAzureStackDetails = $false
)

#https://azure.microsoft.com/en-us/documentation/articles/powershell-azure-resource-manager/

write-host -ForegroundColor gray "-----------------------------------"
write-host -ForegroundColor gray "Azure Stack Template Checker"
write-host -ForegroundColor gray "Did you know? You can also download ready-to-use templates from https://github.com/Azure/AzureStack-QuickStart-Templates"
write-host -ForegroundColor gray "-----------------------------------"

If (Get-AzureRmEnvironment -Name $AzureStackEnvironmentName)
    {
    write-host -ForegroundColor gray "["(date -format "HH:mm:ss")"] Connected to $AzureStackEnvironmentName at $AzureStackEnvironmentFQDN"
    }
    else
    {
    If (($AzureStackAADTenantID -eq "") -and  ($AzureStackEnvironmentName -ne ""))
        {
        $AzureStackAADDefaultDomainName = read-host "You are not already logged into the Azure Stack environment, and no Azure Active Directory Default Domain Name was specified in the script parameters . Please enter this domain name (typically myFQDN.onmicrosoft.com)."
        }
    If (($AzureStackAADTenantID -eq "") -and  ($AzureStackEnvironmentName -ne ""))
        {
        write-host -ForegroundColor gray "["(date -format "HH:mm:ss")"] Retrieving Azure Active Directory Tenant ID from Default Domain Name..."
        $AzureStackAADTenantID = (Invoke-WebRequest -Uri ('https://login.windows.net/'+($AzureStackAADDefaultDomainName)+'/.well-known/openid-configuration')|ConvertFrom-Json).token_endpoint.Split('/')[3]
        }
        else
        {
        write-host -ForegroundColor red "["(date -format "HH:mm:ss")"] ERROR: The Azure Active Directory Default Domain Name or Tenant ID have not been specified - cannot login to Azure Stack environment..."
        }
    If ($AzureStackAADTenantID -eq "")
        {
        write-host -ForegroundColor red "["(date -format "HH:mm:ss")"] ERROR: The Azure Active Directory Tenant ID could not be retrieved - cannot login to Azure Stack environment..."
        exit
        }
    write-host -ForegroundColor gray "["(date -format "HH:mm:ss")"] Connecting to $AzureStackEnvironmentName at $AzureStackEnvironmentFQDN...(Tenant ID is $AzureStackAADTenantID)"
    Add-AzureRmEnvironment -Name $AzureStackEnvironmentName -ActiveDirectoryEndpoint ("https://login.windows.net/$AzureStackAADTenantID/") -ActiveDirectoryServiceEndpointResourceId ("https://$($AzureStackEnvironmentFQDN)-api/") -ResourceManagerEndpoint ("https://api.$AzureStackEnvironmentFQDN/") -GalleryEndpoint ("https://gallery.$AzureStackEnvironmentFQDN:30016") -GraphEndpoint ("https://graph.windows.net")
    $Env = Get-AzureRmEnvironment 'Azure Stack'
    Add-AzureRmAccount -Environment $Env -Verbose
    }

#Get-AzureRmSubscription -SubscriptionName "Default Provider Subscription" | Select-AzureRmSubscription | out-null

$TestResourceGroup = $null
If ($ResourceGroupName ) {$TestResourceGroup = Get-AzureRmResourceGroup -Name $ResourceGroupName}
If (($ResourceGroupName -eq "") -or ($TestResourceGroup -eq $null))
    {
    If ($AutoPickResourceGroup)
        {
        $ResourceGroupName = ((Get-AzureRmResourceGroup | ? ProvisioningState -eq "Succeeded")[0]).ResourceGroupName
        If ($ResourceGroupName -eq "")
            {
            write-host -ForegroundColor red "["(date -format "HH:mm:ss")"] No Resource Group was found using the automatic discovery mechanism, Test-AzureRmResourceGroupDeployment will not be run..."
            $ValidateTemplateWithDefaultCmdlet = $false
            }
        }
        else
        {
        write-host -ForegroundColor red "["(date -format "HH:mm:ss")"] No Resource Group was specified to test the template (or an invalid one was specified), and `$AutoPickResourceGroup was not set, Test-AzureRmResourceGroupDeployment will not be run..."
        $ValidateTemplateWithDefaultCmdlet = $false
        }
    }

write-host -ForegroundColor gray "["(date -format "HH:mm:ss")"] Resource group $ResourceGroupName will be used for template validation - this is a read-only process and no actual deployment will happen"


    If ((Test-Path "$TemplatePath\$TemplateName") -and $TemplateName)
        {
        write-host -ForegroundColor gray "["(date -format "HH:mm:ss")"] Working with '$TemplateName' in location '$TemplatePath'..."
        }
        else
        {
        write-host -ForegroundColor gray "["(date -format "HH:mm:ss")"] Querying for template file to open..."
        [void] [System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")
        $OpenFileWindow = New-Object System.Windows.Forms.OpenFileDialog
        $OpenFileWindow.InitialDirectory = (Get-Location -PSProvider FileSystem).Path
        $OpenFileWindow.ShowHelp=$false
        $OpenFileWindow.Filter = "json files (*.json)|*.json";
        if($OpenFileWindow.ShowDialog() -eq "OK")
            {
            $TemplatePath = $OpenFileWindow.FileName.substring(0, $OpenFileWindow.FileName.LastIndexOf("\"))
            $TemplateName = ($OpenFileWindow.FileName.split("\")[$OpenFileWindow.FileName.split("\").Count-1])
            write-host -ForegroundColor gray "["(date -format "HH:mm:ss")"] Working with '$TemplateName' in location '$TemplatePath'..."
            }
            else
            {
            write-host -ForegroundColor red "["(date -format "HH:mm:ss")"] No JSON file was specified by user, exiting script..."
            exit
            }

        }

$Providers = (Get-AzureRmResourceProvider -ListAvailable)
If ($ListAzureStackDetails)
    {
    #Listing all providers
    write-host -ForegroundColor yellow "["(date -format "HH:mm:ss")"] Listing providers..."
    write-output ($Providers | ft)
    Foreach ($Provider in $Providers.ProviderNamespace)
        {
        write-host -ForegroundColor yellow "["(date -format "HH:mm:ss")"] Details for provider $Provider..."
        write-output ((Get-AzureRmResourceProvider -ProviderNamespace $Provider).ResourceTypes | ft)
        }
    }
    else
    {
    write-host -ForegroundColor gray "["(date -format "HH:mm:ss")"] Skipping details for local Azure Stack installation. You can set the `$ListAzureStackDetails parameters to change this behaviour..."
    }


cd $TemplatePath
write-host -ForegroundColor yellow "["(date -format "HH:mm:ss")"] Validating template with Test-AzureRmResourceGroupDeployment..."

If ((Test-Path (".\" + $TemplateName.split(".")[0] + ".parameters.json")) -ne $True)
    {
    If ($AlwaysSkipManualParameterEntry)
        {
        $ValidateTemplateWithDefaultCmdlet = $false
        }
        else
        {
        If ((Read-Host "Parameters file was not found for template $TemplateName. Do you want to run template validation with Test-AzureRmResourceGroupDeployment? This will require to enter parameters manually (Y/N)?") -ne "Y")
            {
            $ValidateTemplateWithDefaultCmdlet = $false
            }
        }
    }

If ($ValidateTemplateWithDefaultCmdlet)
    {
    write-host -ForegroundColor gray "["(date -format "HH:mm:ss")"] In particular, this should highlight issues in the parameters and variables sections"
    Test-AzureRmResourceGroupDeployment -ResourceGroupName $ResourceGroupName -TemplateFile .\$TemplateName -TemplateParameterFile (".\" + $TemplateName.split(".")[0] + ".parameters.json") -Verbose
    }
    else
    {
    write-host -ForegroundColor gray "["(date -format "HH:mm:ss")"] Skipping Test-AzureRmResourceGroupDeployment because of a parameter in the script,  because a resource group was not defined/discovered, or because manual parameter entry was not desired in the absence of a parameters file."
    }

write-host -ForegroundColor yellow "["(date -format "HH:mm:ss")"] Checking resources compatibility..."
$TemplatePS = (Get-Content "$TemplatePath\$TemplateName") -join "`r`n" | ConvertFrom-Json
Foreach ($Resource in $TemplatePS.resources)
    {
    $ResourceProviderNameSpace = $resource.type.Split("/")[0]
    $ResourceTypeName = $resource.type.Split("/")[1]
    $ResourceTypeProperties = (($Providers | ? ProviderNameSpace -eq $ResourceProviderNameSpace).resourcetypes | ? resourcetypename -eq $ResourceTypeName)
    If ($ResourceTypeProperties)
        {
        write-host -ForegroundColor green "["(date -format "HH:mm:ss")"] -- Resource type $ResourceTypeName from provider $ResourceProviderNameSpace is supported by Azure Stack"
        }
        else
        {
        write-host -ForegroundColor red "["(date -format "HH:mm:ss")"] -- Resource type $ResourceTypeName from provider $ResourceProviderNameSpace is NOT supported by Azure Stack"
        }
    }

write-host -ForegroundColor yellow "["(date -format "HH:mm:ss")"] Checking API version compatibility..."
Foreach ($Resource in $TemplatePS.resources)
    {
    $ResourceProviderNameSpace = $resource.type.Split("/")[0]
    $ResourceTypeName = $resource.type.Split("/")[1]
    $ItemToCheck = $Resource.apiversion
    $AllowedValues = (($Providers | ? ProviderNameSpace -eq $ResourceProviderNameSpace).resourcetypes | ? resourcetypename -eq $ResourceTypeName).apiversions
    If ($resource.apiversion -like "*variables*")
        {     
        $VariableToCheck = $Resource.apiversion.Split("'")[1]
        $ItemToCheck = ($TemplatePS.variables | gm -MemberType "noteproperty" | ? { $_.Name -eq $VariableToCheck}).definition.split("=")[1]
        }
    If ($ItemToCheck -like "*parameters*")
        {
        $DefaultValue = ((($TemplatePS.parameters | gm -MemberType "noteproperty" | ? { $_.Name -eq ($ItemToCheck.Split("'")[1])}).definition -split "defaultvalue=")[1] -split ";")[0]
        If (($DefaultValue) -and ($DefaultValue -inotin $AllowedValues))
            {write-host -ForegroundColor red "["(date -format "HH:mm:ss")"] -- WARNING : API version for resource type $($resource.type) will come from parameter named" $ItemToCheck.Split("'")[1] ". There is a default value, but it does not match the allowed values ($DefaultValue). Allowed Values for this resource type: $AllowedValues"}
        If (($DefaultValue) -and ($DefaultValue -iin $AllowedValues))
            {write-host -ForegroundColor green "["(date -format "HH:mm:ss")"] -- WARNING : API version for resource type $($resource.type) will come from parameter named" $ItemToCheck.Split("'")[1] ". There is a default value ($DefaultValue) that is part of the allowed values. Allowed Values for this resource type: $AllowedValues"}
        If ( -not $DefaultValue)
            {write-host -ForegroundColor red "["(date -format "HH:mm:ss")"] -- WARNING : API version for resource type $($resource.type) will come from parameter named" $ItemToCheck.Split("'")[1] ". There is no default value, but it does not match the allowed values. Allowed Values for this resource type: $AllowedValues"}
        }
        else
        {
        If ($ItemToCheck -iin $AllowedValues)
            {
            write-host -ForegroundColor green "["(date -format "HH:mm:ss")"] -- Resource type $($resource.type) leverages API version $ItemToCheck. Allowed Values are $AllowedValues"
            }
            else
            {
            write-host -ForegroundColor red "["(date -format "HH:mm:ss")"] -- Resource type $($resource.type) leverages API version $ItemToCheck. Allowed Values are $AllowedValues"
            }
        }
    }
   

write-host -ForegroundColor yellow "["(date -format "HH:mm:ss")"] Checking location compatibility..."
Foreach ($Resource in $TemplatePS.resources)
    {
    $ResourceProviderNameSpace = $resource.type.Split("/")[0]
    $ResourceTypeName = $resource.type.Split("/")[1]
    $ItemToCheck = $Resource.location
    $AllowedValues = (($Providers | ? ProviderNameSpace -eq $ResourceProviderNameSpace).resourcetypes | ? resourcetypename -eq $ResourceTypeName).locations
    If ($resource.location -like "*variables*")
        {        
        $VariableToCheck = $Resource.location.Split("'")[1]
        $ItemToCheck = ($TemplatePS.variables | gm -MemberType "noteproperty" | ? { $_.Name -eq $VariableToCheck}).definition.split("=")[1]
        }
    If ($ItemToCheck -like "*parameters*")
        {
        $DefaultValue = (((($TemplatePS.parameters | gm -MemberType "noteproperty" | ? { $_.Name -eq ($ItemToCheck.Split("'")[1])}).definition -split "defaultvalue=")[1] -split ";")[0]).trim("}")
        If (($DefaultValue) -and ($DefaultValue -inotin $AllowedValues))
            {write-host -ForegroundColor red "["(date -format "HH:mm:ss")"] -- WARNING : Location for resource type $($resource.type) will come from parameter named" $ItemToCheck.Split("'")[1] ". There is a default value, but it does not match the allowed values ($DefaultValue). Allowed Values for this resource type: $AllowedValues"}
        If (($DefaultValue) -and ($DefaultValue -iin $AllowedValues))
            {write-host -ForegroundColor green "["(date -format "HH:mm:ss")"] -- WARNING : Location for resource type $($resource.type) will come from parameter named" $ItemToCheck.Split("'")[1] ". There is a default value ($DefaultValue) that is part of the allowed values. Allowed Values for this resource type: $AllowedValues"}
        If ( -not $DefaultValue)
            {write-host -ForegroundColor red "["(date -format "HH:mm:ss")"] -- WARNING : Location for resource type $($resource.type) will come from parameter named" $ItemToCheck.Split("'")[1] ". There is no default value, but it does not match the allowed values. Allowed Values for this resource type: $AllowedValues"}
        }
        else
        {
        If ($ItemToCheck -iin $AllowedValues)
        {
            write-host -ForegroundColor green "["(date -format "HH:mm:ss")"] -- Resource type $($resource.type)  targets $ItemToCheck location. Allowed Values are $AllowedValues"
            }
            else
            {
            If ($ItemToCheck -like "*resourcegroup().location*")
                {write-host -ForegroundColor green "["(date -format "HH:mm:ss")"] -- Resource type $($resource.type) targets $ItemToCheck location. This usually comes from Azure Templates, but should also work with Azure Stack. Specific allowed Values are $AllowedValues"}
                else
                {write-host -ForegroundColor red "["(date -format "HH:mm:ss")"] -- Resource type $($resource.type) targets $ItemToCheck location. Allowed Values are $AllowedValues"}
            }
        }
    }

write-host -ForegroundColor yellow "["(date -format "HH:mm:ss")"] Testing URIs..."
$CheckURI = (Get-Content "$TemplatePath\$TemplateName") | Select-String -Pattern "blob.core.windows.net" -Context 3
If ($CheckURI)
    {
    write-host -ForegroundColor red "["(date -format "HH:mm:ss")"] -- WARNING : URI for blob.core.windows.net have been found in this template. If this is in a list of allowed values it may be acceptable. You should check the template. Small extract follows:"
    write-host $CheckURI
    }
    else
    {
    write-host -ForegroundColor green "["(date -format "HH:mm:ss")"] -- No URI for blob.core.windows.net have been found in this template."
    }

If ($CheckVMExtensions)
    {
    If (Test-Path $GARPath)
        {
        write-host -ForegroundColor yellow "["(date -format "HH:mm:ss")"] Testing VM extensions..."
        write-host -ForegroundColor gray "["(date -format "HH:mm:ss")"] -- Inventorying VM extensions from Azure Stack installation..."
        $VMExtensionsArray = @()
        Foreach ($VMExtensioPackage in (Get-ChildItem -Path $GARPath))
            {
            $tmpObject = select-object -inputobject "" Publisher, Type, Version
            $tmpObject.Publisher = ($VMExtensioPackage.Name.Split("_")[0]).Substring(0,$VMExtensioPackage.Name.Split("_")[0].LastIndexOf("."))
            $tmpObject.Type = ($VMExtensioPackage.Name.Split("_")[0]).Split(".")[$VMExtensioPackage.Name.Split("_")[0].Split(".").Count -1]
            $tmpObject.Version = [version]($VMExtensioPackage.Name.Split("_")[1].trim(".zip"))
            $VMExtensionsArray += $tmpObject
            }
        write-host -ForegroundColor gray "["(date -format "HH:mm:ss")"] -- Found" $VMExtensionsArray.Count "VM extensions in local Azure Stack installation."
        $VMExtensions = $TemplatePS.resources | ? type -eq "Microsoft.Compute/virtualMachines/extensions"
        If ($VMExtensions -eq $null)
            {
            $VMExtensions = ($TemplatePS.resources | ? type -eq "Microsoft.Compute/virtualMachines").resources | ? type -eq "extensions"
            }
        If ($VMExtensions -eq $null)
            {
            write-host -ForegroundColor gray "["(date -format "HH:mm:ss")"] -- No VM extensions are used in this template."
            }
        Foreach ($VMExtension in $VMExtensions)
            {
                $VersionToCheck = $VMExtension.properties.typeHandlerVersion
                If ($VersionToCheck.Split(".").Count -eq 2) {$VersionToCheck = $VersionToCheck + ".0.0"}
                If ($VersionToCheck.Split(".").Count -eq 1) {$VersionToCheck = $VersionToCheck + "0.0.0"}
                $VersionToCheck = [Version]$VersionToCheck
                $VersionsAvailable = ($VMExtensionsArray | ? Publisher -eq $VMExtension.properties.publisher | ? Type -eq $VMExtension.properties.type).Version | Sort-Object
 
                If ($VersionsAvailable -eq $null)
                    {
                    write-host -ForegroundColor red "["(date -format "HH:mm:ss")"] -- This template uses" $VMExtension.properties.type "version" $VMExtension.properties.typeHandlerVersion "(" $VMExtension.properties.publisher "), which was not found in the Azure Stack installation"
                    }
                    else
                    {
                    $MinVersionAvailable = $VersionsAvailable[0]
                    $MaxVersionAvailable = $VersionsAvailable[$VersionsAvailable.Count -1]
                    If ($VersionsAvailable -contains $VersionToCheck)
                        {
                        write-host -ForegroundColor green "["(date -format "HH:mm:ss")"] -- This template uses" $VMExtension.properties.type "version" $VMExtension.properties.typeHandlerVersion "(" $VMExtension.properties.publisher "), which is part of the available extensions on this Azure Stack installation"
                        }
                        else
                        {
                        If ($VersionToCheck -gt $MaxVersionAvailable)
                            {
                            write-host -ForegroundColor red "["(date -format "HH:mm:ss")"] -- This template uses" $VMExtension.properties.type "version" $VMExtension.properties.typeHandlerVersion "(" $VMExtension.properties.publisher "). A lower version $MaxVersionAvailable was found in this Azure Stack installation and needs to be upgraded."
                            }
                        If ($VersionToCheck -lt $MaxVersionAvailable)
                            {
                            If ($VMExtension.autoUpgradeMinorVersion -eq "true")
                                {
                                write-host -ForegroundColor green "["(date -format "HH:mm:ss")"] -- This template uses" $VMExtension.properties.type "version" $VMExtension.properties.typeHandlerVersion "(" $VMExtension.properties.publisher "). A higher version $MaxVersionAvailable was found in this Azure Stack installation, and can be used because autoUpgradeMinorVersion is set in the template."
                                }
                                else
                                {
                                write-host -ForegroundColor red "["(date -format "HH:mm:ss")"] -- This template uses" $VMExtension.properties.type "version" $VMExtension.properties.typeHandlerVersion "(" $VMExtension.properties.publisher "). A higher version $MaxVersionAvailable was found in this Azure Stack installation, and could be used if autoUpgradeMinorVersion was set in the template."
                                }
                            }
                        }
                    }
            }
        }
        else
        {
        write-host -ForegroundColor gray "["(date -format "HH:mm:ss")"] -- Guest Artifact Repository not specific or invalid, skipping testing VM extensions..."
        }
    }

write-host -ForegroundColor yellow "["(date -format "HH:mm:ss")"] Checking VM Sizes..."
$Resources = $TemplatePS.resources | ? type -eq "Microsoft.Compute/virtualMachines"
Foreach ($Resource in $Resources)
    {
    $ItemToCheck = $Resource.properties.hardwareprofile.vmsize
    $AllowedValues = (Get-AzureRmVMSize -Location westus).name
    If ($ItemToCheck -like "*variables*")
        {        
        $VariableToCheck = $ItemToCheck.Split("'")[1]
        $ItemToCheck = ($TemplatePS.variables | gm -MemberType "noteproperty" | ? { $_.Name -eq $VariableToCheck}).definition.split("=")[1]
        }
    If ($ItemToCheck -like "*parameters*")
        {
        $DefaultValue = ((($TemplatePS.parameters | gm -MemberType "noteproperty" | ? { $_.Name -eq ($ItemToCheck.Split("'")[1])}).definition -split "defaultvalue=")[1] -split ";")[0]
        If (($DefaultValue) -and ($DefaultValue -inotin $AllowedValues))
            {write-host -ForegroundColor red "["(date -format "HH:mm:ss")"] -- WARNING : Size for VM $($Resource.Name) will come from parameter named" $ItemToCheck.Split("'")[1] ". There is a default value, but it does not match the allowed values ($DefaultValue). Allowed Values for this resource type: $AllowedValues"}
        If (($DefaultValue) -and ($DefaultValue -iin $AllowedValues))
            {write-host -ForegroundColor green "["(date -format "HH:mm:ss")"] -- WARNING : Size for VM $($Resource.Name) will come from parameter named" $ItemToCheck.Split("'")[1] ". There is a default value ($DefaultValue) that is part of the allowed values. Allowed Values for this resource type: $AllowedValues"}
        If ( -not $DefaultValue)
            {write-host -ForegroundColor red "["(date -format "HH:mm:ss")"] -- WARNING : Size for VM $($Resource.Name) will come from parameter named" $ItemToCheck.Split("'")[1] ". There is no default value, but it does not match the allowed values. Allowed Values for this resource type: $AllowedValues"}
        }
        else
        {
        If ($ItemToCheck -iin $AllowedValues)
            {
            write-host -ForegroundColor green "["(date -format "HH:mm:ss")"] -- Size for VM $($Resource.Name) is $ItemToCheck. Allowed Values are $AllowedValues"
            }
            else
            {
            write-host -ForegroundColor red "["(date -format "HH:mm:ss")"] -- Size for VM $($Resource.Name) is $ItemToCheck. Allowed Values are $AllowedValues"}
            }
        }


If ($CheckPlatformImages)
    {
    If (Test-Path $PIRPath)
        {
        write-host -ForegroundColor yellow "["(date -format "HH:mm:ss")"] Checking Platform Images..."
        write-host -ForegroundColor gray "["(date -format "HH:mm:ss")"] -- Inventorying Platform Images from Azure Stack installation..."
        $PlatformImagesArray = @()
        Foreach ($PlatformImageManifest in (Get-ChildItem -Path $PIRPath -Include *.json -Recurse))
            {
            $ManifestFile = (Get-Content -Path $PlatformImageManifest) -join "`r`n" | ConvertFrom-Json
            $tmpObject = select-object -inputobject "" Name, Publisher, Offer, Sku, Version
            $tmpObject.Name = $PlatformImageManifest.DirectoryName.Split("\")[$PlatformImageManifest.DirectoryName.Split("\").Count-1]
            $tmpObject.Publisher = $ManifestFile.Publisher
            $tmpObject.Offer = $ManifestFile.Offer
            $tmpObject.Sku = $ManifestFile.Sku
            $tmpObject.Version = $ManifestFile.Version
            $PlatformImagesArray += $tmpObject
            }
        write-host -ForegroundColor gray "["(date -format "HH:mm:ss")"] -- Found" $PlatformImagesArray.Count "Platform images in local Azure Stack installation."

        $Resources = $TemplatePS.resources | ? type -eq "Microsoft.Compute/virtualMachines"
        Foreach ($Resource in $Resources)
            {
            $ItemToCheck = $Resource.properties.storageprofile.imagereference.sku
            $AllowedValues = $PlatformImagesArray.sku
            If ($ItemToCheck -like "*variables*")
                {        
                $VariableToCheck = $ItemToCheck.Split("'")[1]
                $ItemToCheck = ($TemplatePS.variables | gm -MemberType "noteproperty" | ? { $_.Name -eq $VariableToCheck}).definition.split("=")[1]
                }
            If ($ItemToCheck -like "*parameters*")
                {
                $DefaultValue = ((($TemplatePS.parameters | gm -MemberType "noteproperty" | ? { $_.Name -eq ($ItemToCheck.Split("'")[1])}).definition -split "defaultvalue=")[1] -split ";")[0]
                If (($DefaultValue) -and ($DefaultValue -inotin $AllowedValues))
                    {write-host -ForegroundColor red "["(date -format "HH:mm:ss")"] -- WARNING : SKU for VM $($Resource.Name) will come from parameter named" $ItemToCheck.Split("'")[1] ". There is a default value, but it does not match the allowed values ($DefaultValue). Allowed Values for this resource type: $AllowedValues"}
                If (($DefaultValue) -and ($DefaultValue -iin $AllowedValues))
                    {write-host -ForegroundColor green "["(date -format "HH:mm:ss")"] -- WARNING : SKU for VM $($Resource.Name) will come from parameter named" $ItemToCheck.Split("'")[1] ". There is a default value ($DefaultValue) that is part of the allowed values. Allowed Values for this resource type: $AllowedValues"}
                If ( -not $DefaultValue)
                    {write-host -ForegroundColor red "["(date -format "HH:mm:ss")"] -- WARNING : SKU for VM $($Resource.Name) will come from parameter named" $ItemToCheck.Split("'")[1] ". There is no default value, but it does not match the allowed values. Allowed Values for this resource type: $AllowedValues"}
                }
                else
                {
                If ($ItemToCheck -iin $AllowedValues)
                    {
                    write-host -ForegroundColor green "["(date -format "HH:mm:ss")"] -- SKU for VM $($Resource.Name) is $ItemToCheck. Allowed Values are $AllowedValues"
                    }
                    else
                    {
                    write-host -ForegroundColor red "["(date -format "HH:mm:ss")"] -- SKU for VM $($Resource.Name) is $ItemToCheck. Allowed Values are $AllowedValues"}
                    }
                }
        }
        else
        {
        write-host -ForegroundColor gray "["(date -format "HH:mm:ss")"] -- Platform Images Repository not specific or invalid, skipping checking Platform Images..."
        }
    }

write-host -ForegroundColor yellow "["(date -format "HH:mm:ss")"] Done!"

#################################################
# VERSION HISTORY
# v1.1
# - Updated ResourceGroup.Location() analysis (should work with Azure Stack)
# - Added more comprehensive logic to check for VM extensions, in the case of multiple versions present in the local Azure Stack installation
# - Added a check for situations when extensions are declared within virtual machines resources, as seen here : https://github.com/Azure/azure-quickstart-templates/blob/master/201-vm-monitoring-diagnostics-extension/azuredeploy.json
# - Fixed an issue with location detection, depending on the properties used in the template
# v1.0
# - Initial release
#################################################

