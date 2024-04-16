#Define Parameters
$AdminCenterURL = "https://sharepointtestfreetrial-admin.sharepoint.com/"
$SiteURL = "https://sharepointtestfreetrial.sharepoint.com/sites/ImeaExampleWebsite2"
$SiteTitle = "Imea Example Website 2"
$SiteOwner = "savem.freetrial1@sharepointTestFreeTrial.onmicrosoft.com"
$Template = "STS#0" #Classic Team Site
$Timezone = 1 #Abudhabi
 
Try
{
    #Connect to Tenant Admin
    Connect-PnPOnline -URL $AdminCenterURL
     
    #Check if site exists already
    $Site = Get-PnPTenantSite | Where {$_.Url -eq $SiteURL}
 
    If ($Site -eq $null)
    {
        #sharepoint online pnp powershell create site collection
        New-PnPTenantSite -Url $SiteURL -Owner $SiteOwner -Title $SiteTitle -Template $Template -TimeZone $TimeZone -RemoveDeletedSite
        write-host "Site Collection $($SiteURL) Created Successfully!" -foregroundcolor Green
    }
    else
    {
        write-host "Site $($SiteURL) exists already!" -foregroundcolor Yellow
    }
}
catch {
    write-host "Error: $($_.Exception.Message)" -foregroundcolor Red
}