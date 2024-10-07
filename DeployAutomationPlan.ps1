#Get PS Credential Object
$user = ""
$pass = ""
$secpasswd = ConvertTo-SecureString $pass -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential($user, $secpasswd)

$searchURI = "https://bfrootserver:8443/serverautomation/plan/master/planid"

$searchBody = @"
<?xml version='1.0' encoding='utf-8'?>
<sa-rest xmlns="http://iemfsa.tivoli.ibm.com/REST">
  <execute-plan action-name="Demo_AutomationPlan" prefetch="false">
    <step sequence="101" name="Apache%20-%20Stop%20Services">
      
    <target-set><computer name="bfvlcentapache" id="1614536093"> </computer></target-set></step>
    <step sequence="102" name="Lab_Baseline"><target-set><computer name="bfvlcentapache" id="1614536093"> </computer></target-set></step>
    <step sequence="103" name="Apache%20-%20Start%20Servivces">
      
    <target-set><computer name="bfvlcentapache" id="1614536093"> </computer></target-set></step>
    <schedule>
      <HasStartTime>false</HasStartTime>
      <StartDateTimeOffset>P0DT0H0M0S</StartDateTimeOffset>
      <HasEndTime>true</HasEndTime>
      <EndDateTimeOffset>P0DT1H0M0S</EndDateTimeOffset>
      <UseUTCTime>true</UseUTCTime>
    </schedule>
  </execute-plan>
</sa-rest>
"@

$headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
# Invoke-RestMethod -Method Post -Uri $searchURI -Credential $cred -Body $searchBody -ContentType "application/xml"
[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$searchResults = Invoke-RestMethod -Method Post -Uri $searchURI -Credential $cred -Body $searchBody -ContentType "application/xml" -Headers $headers
write-host $searchResults.OuterXml

$searchResults
