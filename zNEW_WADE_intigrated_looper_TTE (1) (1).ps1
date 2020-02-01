C:\Users\Public\ps-azure\start-windowsazure.ps1
wa -LoadFromLocal

$WorkItemStore = connect-azuretfs

$team = 'WINDOWSAZUREOPERATIONSCENTER\WADE'
$icmCreateDate = (Get-Date).AddDays(-60).ToString("yyyy-MM-ddTHH:mm:ss")
$uri = 'https://icm.ad.msft.net/api/cert/incidents?$filter=(CreateDate gt datetime'''+$icmCreateDate+''' and OwningTeamId eq '''+$Team+''') and Status eq ''Active'' and OwningContactAlias eq null'
$myICMCertificate = Get-ChildItem Cert:\CurrentUser\my | Where-Object {$_.subject -match "icm.ad.msft.net"}

Function Show-MessageBox ($MessageTitle,$MessageBody)
{
    if (!$global:MsgBoxLoaded)
    {
        $source = @"
            using System;
            using System.Runtime.InteropServices;

            public class MsgBox
            {
                [DllImport("user32.dll", CharSet = CharSet.Auto)]
                public static extern int MessageBox(IntPtr hWnd, String text, String caption, int options);

                [STAThread]
                public static void Main(string[] args) {}
                
                [STAThread]
                public static int Show(string title, string text)
                {
                    return MessageBox(IntPtr.Zero, text, title, 4097);
                }
            }
"@

        Add-Type -TypeDefinition $source

        if ($?) { $global:MsgBoxLoaded = $true }
    }

    [MsgBox]::Show($MessageTitle,$MessageBody);
}

function get-ActionableWorkItemsRDTask()
{
#GET THE TFS OBJECT 

$arr1=@()
If($WorkItemStore)
{

#$workitems = $WorkItemStore.Query(@"
#SELECT [System.Id], [System.WorkItemType], [System.Title], [System.AssignedTo], [System.State], [Microsoft.RD.IncidentType], [Microsoft.Azure.Incident.SubType]  FROM WorkItems WHERE [System.TeamProject] = 'RD'  AND ( [System.WorkItemType] = 'RDIncident'  AND  [Microsoft.RD.IncidentType] = 'Deployment'  AND  [System.State] = 'Triage'  AND [Source] = 'Deployment Infrastructure'  AND  [System.AreaPath] = 'RD\CloudManagement\WADE'  AND  [Microsoft.Azure.Incident.Environment] IN ('Production', 'Stage')  AND  [System.AssignedTo] = 'WA Deployment Engineering')  ORDER BY [System.Id]
#"@)

$RDTaskitems = $WorkItemStore.Query(@"
SELECT [System.Id], [System.WorkItemType], [System.Title], [System.AssignedTo], [Microsoft.VSTS.Common.Priority], [Microsoft.VSTS.Common.Triage] FROM WorkItems WHERE [System.TeamProject] = 'RD'  AND  [System.WorkItemType] = 'RDTask'  AND  [System.State] = 'Active'  AND  [System.AreaPath] NOT UNDER 'RD\CloudManagement\WADE\In Service' AND  [System.AssignedTo] = 'WA Deployment Engineering' AND [Microsoft.VSTS.Common.Triage] = 'Approved'  AND [Microsoft.Azure.WorkStatus] = 'Not Started' ORDER BY [System.Id]
"@)



#Write-Host "Found $($workitems.Count) Incidents `n" -ForegroundColor Green
Write-Host "Found $($RDTaskitems.Count) RDTask `n" -ForegroundColor Green

$date = Get-Date 

$dep_To_Start=@()
$planned_at=@()

$DeploymentTasks=$WorkItemStore.Query(@"
SELECT [System.Id], [System.WorkItemType], [System.Title], [System.AssignedTo], 
[System.State] FROM WorkItems WHERE [System.TeamProject] = 'RD'  AND ( [System.WorkItemType] = 'DeploymentTask' 
AND  [System.AssignedTo] = 'WA Deployment Engineering' AND  ([System.State] = 'Awaiting Deployment' Or  [System.State] = 'Pending' ) and [Microsoft.VSTS.Scheduling.BaselineStartDate]>='$($date.AddDays(-1).ToShortDateString())' and [Microsoft.VSTS.Scheduling.BaselineStartDate]<='$($date.AddDays(1).ToShortDateString())')ORDER BY [System.Id]
"@)
Write-Host "Total scheduled deployments in Queue $($DeploymentTasks.count) Deployments `n " -ForegroundColor Green
if($DeploymentTasks.count -gt 0){
#Write-Host "  Below are $($DeploymentTasks.count) Deployments :-`n " -ForegroundColor Green
#Write-host "_______________________________________________________________________________________________________"
#Write-Host "|ID__________|_______________________Title__________________________________|PlannedSTartDate|-->State"

foreach($ITEM IN $DeploymentTasks)
{
foreach($field1 in $item.Fields)
{
if($field1.Name -eq 'Planned start Date'){
$start_time=(Get-Date $field1.value)
$id=$item.Id
$title=$item.Title
$state=$item.State
$time_left=New-TimeSpan -Start $date -End ($start_time)
if(($time_left.Days -eq 0) -and ($time_left.hours -eq 0) )
		{
			IF(($time_left.Minutes -le 0) -and ($time_left.Minutes -ge -35))
				{
				if($flag1 -eq 0)
					{
					Write-Host " `n Below Deployments to start immediately `n" -ForegroundColor Red
					}
					Write-Host "ID:$($id  ) Title:$($title) were scheduled for time:$($start_time) overdue:$($time_left.Minutes) Minutes `n"
					$flag1=1
				}
			elseIF($time_left.Minutes -ge 0)
				{

				if($flag2 -eq 0)
				{
				Write-Host "`n Deployments to start in less than an hour `n " -ForegroundColor Yellow
				}
				Write-Host "ID:$($id  ) Title:$($title) in next : $($time_left.Minutes) Minutes at time:$($start_time) `n"
				$flag2=1
				}
$dep_To_Start+=$time_left.Minutes
    }

}
}
}

}

$uni=$dep_To_Start | Select-Object -Unique
if($dep_To_Start.Count -ge 0){
foreach($d in $uni)
{
$count=0
foreach($item in $dep_To_Start)
{
if($d -eq $ITEM){$count+=1}
}
Write-Host ("--->$($count) deployment to start in $($d) min") -BackgroundColor White -ForegroundColor Blue
}
}

$i=0
foreach($ITEM in $dep_To_Start){
if($ITEM -gt 0 -and ($ITEM -eq 30 -or $ITEM%10 -eq 0)){$i=1}
elseif($ITEM -le -31){$i=0}
elseif(($ITEM -le -25 )-and ($ITEM -ge -31 )){$i=1}
elseif($ITEM -le 0 -and $ITEM%2 -eq 0){$i=1}

}

#if ((($workitems.Count -gt 0) -or ($RDTaskitems.Count -gt 0) -and $i -eq 0)-or ($i -eq 1))
if ((($RDTaskitems.Count -gt 0) -and $i -eq 0)-or ($i -eq 1))
{

$MessageTitle =" New RDtask found"
$MessageBody = "Found RDTasks/Sheduled Deployments in WADE In Queue. Please check WADE Queue ASAP. Press OK or Cancel to view the incidents. "
$result= Show-MessageBox $MessageTitle  $MessageBody

#Write-Host "Below are the RDIncidents in WADE In Queue" -ForegroundColor Green
#$workitems | Select ID,Title | ft -a 
Write-Host "Below are the RDTask and Sheduled Deployments" -ForegroundColor Yellow
$RDTaskitems | Select ID,Title | ft -a 
#Start-Sleep -Seconds 10
}

}
else 
{
    Write-Error "ERROR: Connection to TFS is not available" -ForegroundColor "Yellow"
}

}

function get-ActionableWorkItemsRTO()
{
#GET THE TFS OBJECT 

$arr1=@()
If($WorkItemStore)
{

#$workitems = $WorkItemStore.Query(@"
#SELECT [System.Id], [System.WorkItemType], [System.Title], [System.AssignedTo], [System.State], [Microsoft.RD.IncidentType], [Microsoft.Azure.Incident.SubType]  FROM WorkItems WHERE [System.TeamProject] = 'RD'  AND ( [System.WorkItemType] = 'RDIncident'  AND  [Microsoft.RD.IncidentType] = 'Deployment'  AND  [System.State] = 'Triage'  AND [Source] = 'Deployment Infrastructure'  AND  [System.AreaPath] = 'RD\CloudManagement\WADE'  AND  [Microsoft.Azure.Incident.Environment] IN ('Production', 'Stage')  AND  [System.AssignedTo] = 'WA Deployment Engineering')  ORDER BY [System.Id]
#"@)

$RDTaskitems = $WorkItemStore.Query(@"
SELECT [System.Id], [System.WorkItemType], [System.Title], [System.AssignedTo], [Microsoft.VSTS.Common.Priority], [Microsoft.VSTS.Common.Triage] FROM WorkItems WHERE [System.TeamProject] = 'RD'  AND  [System.WorkItemType] = 'RDTask'  AND  [System.State] = 'Active'  AND  [System.AreaPath] NOT UNDER 'RD\CloudManagement\WADE\In Service' AND  [System.AssignedTo] = 'WA Deployment Engineering' AND [Microsoft.Azure.Incident.OwnerTeam] = 'Windows Azure Operations Center/WADE' AND [Microsoft.Azure.WorkStatus] = 'Not Started' AND [Microsoft.RD.KeywordSearch] CONTAINS 'WADE_RTO' ORDER BY [System.Id]
"@)

#Write-Host "Found $($workitems.Count) Incidents `n" -ForegroundColor Green
Write-Host "Found $($RDTaskitems.Count) RDTask `n" -ForegroundColor Green


#if ((($workitems.Count -gt 0) -or ($RDTaskitems.Count -gt 0) -and $i -eq 0)-or ($i -eq 1))
if ($RDTaskitems.Count -gt 0)
{
$MessageTitle = " NEW RTO found"

$MessageBody = "Found New RTO RDTasks in WADE In Queue. Please check WADE RTO Queue ASAP. Press OK or Cancel to view the incidents. "

$result= Show-MessageBox $MessageTitle  $MessageBody

$RDTaskitems | Select ID,Title | ft -a 


}

}
else 
{
    Write-Error "ERROR: Connection to TFS is not available" -ForegroundColor "Yellow"
}

}


Function Get-IcmIncidentsInTriage
{Write-Host "$(Get-Date): Retrieving IcM Incidents" 
    $attemptStart = Get-Date
    Try
    {
        $icmQuery = Invoke-RestMethod -uri $uri -Certificate $myICMCertificate

        $sev2 =  $icmQuery.value | ?{$_.Severity -lt 3}
    }
    Catch    {
        $_.Exception.Message        
    }

    if ($sev2)
    {        
             
              $text=
"
¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦ 


$($sev2.Id):   $($sev2.Title)`n`n Sev2 incident Please check Triage Queue ASAP.`n`nPress OK to view the incidents

¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦
"
       
       
        $title = "New Sev 2 Incident"
        $messageBox = New-Object -ComObject Wscript.Shell 
        
        $promptResult = $messageBox.Popup($text,0,$title, 4097)
        if ($promptResult -eq 1)
        {
            $id = $sev2 | Select-Object ID     
            foreach ($item in $id)
            {  
                $incidentUrl = "https://icm.ad.msft.net/imp/IncidentDetails.aspx?id="+$item.id
                Start-Process $incidentUrl 
            }
        }  
        
    }


    if ($icmQuery.value.Count -gt 0)
    {        
        $global:lastIcmIncidentsFound = $attemptStart
        
        $name = $icmQuery.value | Select -expandproperty 'Title'
  $icm1 = @()

        ForEach ($ComputerDataName in $name)

{

 $icm1 +=($ComputerDataName).Split(' ')[0]

    

}
    
        $sev = $icmQuery.value | Select -expandproperty Severity

        $text = "Found IcM Incidents in Triage.`n`nTitle :$icm1`n`nSeverity : $sev`n`n`Please check Triage Queue ASAP.Press OK to view the incidents, 
                
      "
        $title = "IcM Incidents Count :$($icmQuery.value.Count) "
        $messageBox = New-Object -ComObject Wscript.Shell 
        
        $promptResult = $messageBox.Popup($text,0,$title, 4097)
        if ($promptResult -eq 1)
        {
            $id = $icmQuery.value | Select-Object ID     
            foreach ($item in $id)
            {  
                $incidentUrl = "https://icm.ad.msft.net/imp/IncidentDetails.aspx?id="+$item.id
                Start-Process $incidentUrl 
            }
        }   
        $border="`n*********************************************************************************`n" 
        $border 
       
        Write-Host "Found IcM Incidents in Triage."  -ForegroundColor red
        Write-Host " `n`nTitle :$icm1`n`nSeverity : $sev.  "  -ForegroundColor Green
        Write-Host "`n`nPlease check Triage Queue ASAP.Press OK to view the incidents`n`n"
        $border 
        
    }
    else 
    {

    Write-Host " `nthere are no incident to acknowledge`n" -ForegroundColor Green
    }



}

function TFS-Incident
 
{

$Incidents = $WorkItemStore.Query(@"
SELECT * FROM WorkItems WHERE [System.TeamProject] = 'RD'  
AND  [System.WorkItemType] = 'RDIncident'  AND  [System.State] = 'TRIAGE'  AND  [Microsoft.RD.IncidentType] = 'Deployment'  AND 
 [Microsoft.Azure.Incident.Environment] = 'Production'  AND  [Microsoft.VSTS.Common.Source] = 'Deployment Infrastructure'  
 AND ([Microsoft.Azure.Incident.OwnerTeam] = 'Windows Azure Operations Center/WADE' or [System.AssignedTo] = 'WA Deployment Engineering')
and  [System.AreaPath] UNDER 'RD\CloudManagement\WADE' and [Microsoft.IcM.Id] = '$Null'
    ORDER BY [System.CreatedDate] desc
"@)

if ($Incidents.Count -gt 0)
{

$date = (Get-Date)

$Blockers = @()
  $x = @()

  $Global:order = $null

  $x=$Incidents[0].Fields.name  

  for ($i = 0; $i -lt $x.Count ; $i++)
  { 
      
      if ($x[$i] -eq 'ICMID')
      {

      $order = $i

      }
  }

  
foreach ($item in $Incidents)
{ 



$time =  ((NEW-TIMESPAN –Start ($item.CreatedDate.Addminutes(60))  -End (get-date)).TotalMinutes)
   
    if ( $time -ge 0 )

    {

    $Blockers += $item
    
    
    }
}

  if ($Blockers.Count -gt 0)
  {   
  
  
$text = "found $($Blockers.Count) blockers without incident "

$Blockers | select Id,title | ft -AutoSize

$MessageBody = "found $($Blockers.Count) blockers without ICM incident "
$MessageTitle = "No ICM incident found for blocker"
$result= Show-MessageBox $MessageTitle  $MessageBody

}

}

}

function Get-IncidentsNearTTE
{

$uri = 'https://icm.ad.msft.net/api/cert/incidents?$filter=(CreateDate gt datetime'''+$icmCreateDate+''' and OwningTeamId eq '''+$Team+''') and Status eq ''Active''  and  CustomFieldGroups/any(cfg:cfg/CustomFields/any(cf:cf/Name eq ''substatus'' and cf/Type eq ''Enum'' and cf/Value eq ''Blocked''))'
$icmQuery1 = Invoke-RestMethod -uri $uri -Certificate $myICMCertificate

$uri1 = 'https://icm.ad.msft.net/api/cert/incidents?$filter=(CreateDate gt datetime'''+$icmCreateDate+''' and OwningTeamId eq '''+$Team+''') and Status eq ''Active'''
$icmQuery2 = Invoke-RestMethod -uri $uri1 -Certificate $myICMCertificate 

$unblockedincidents  =   $icmQuery2.value | ?{$_.id -notin $icmQuery1.value.id}


    $attemptStart = [DateTime]::Now.ToUniversalTime()
  

    $Severity=@{Expression={$_.Severity};label="Severity"}
    $ID=@{label="Incident";Expression={$_.ID}}
    $IcmOnCall=@{Expression={$_.OwningContactAlias};label="On-Call"}
    $IncidentTitle=@{Expression={$_.Title};label="Title";Width=25}
    $sev2SLALeft=@{label="SLA Left_min";Expression={14 - (($attemptStart - ([datetime]$_.CreateDate)).TotalMinutes.Tostring('#.##'))}}
    $sev3SLALeft=@{label="SLA Left_min";Expression={179 - (($attemptStart - ([datetime]$_.CreateDate)).TotalMinutes.Tostring('#.##'))}}
    $sev4SLALeft=@{label="SLA Left_min";Expression={479 - (($attemptStart - ([datetime]$_.CreateDate)).TotalMinutes.Tostring('#.##'))}}

    $text1 = "Found Incidents near to SLA, Please check and Escalate/Mitigate"
    $title = "IcM Incidents near SLA"


    $sev2SLA = $unblockedincidents | ? {$_.Severity -eq 2 -or $_.Severity -eq 1 -and (($attemptStart - ([datetime]$_.CreateDate)).TotalMinutes -ge 05) -and (($attemptStart - ([datetime]$_.CreateDate)).TotalMinutes -le 45)} | Format-Table  $Severity,$ID,$sev2SLALeft,$IncidentTitle | Out-String
    $sev3SLA = $unblockedincidents | ? {$_.Severity -eq 3 -and (($attemptStart - ([datetime]$_.CreateDate)).TotalMinutes -ge 150) -and (($attemptStart - ([datetime]$_.CreateDate)).TotalMinutes -le 185)} | Format-table $Severity,$ID,$sev3SLALeft,$IncidentTitle | Out-String
    $sev4SLA = $unblockedincidents | ? {$_.Severity -eq 4 -and (($attemptStart - ([datetime]$_.CreateDate)).TotalMinutes -ge 450) -and (($attemptStart - ([datetime]$_.CreateDate)).TotalMinutes -le 485)} | Format-table $Severity,$ID,$sev4SLALeft,$IncidentTitle | Out-String 
  


    if (($sev2SLA.Length -ne 0) -or ($sev3SLA.length -ne 0) -or ($sev4SLA.Length -ne 0))
   {
      $banner=
      "
      ██████████████████████████████████████
       INCIDENTS  NEAR  TO  SLA  
       PLEASE  CHECK  AND  ESCALATE  
      ██████████████████████████████████████
      "
        $slaText = $banner + $sev2SLA + $sev3SLA + $sev4SLA
        Write-Host "Found Incidents near to SLA, please check and escalate/Mitigiate" -ForegroundColor Red
        $messageBox = New-Object -ComObject Wscript.Shell 
        $promptResult = $messageBox.Popup($slatext,0,$title, 4097) 
       if ($promptResult -eq 1){
       $icmid = $unblockedincidents | select-Object ID
       #$icmid
          foreach ($item in $icmid)
            {  
             $incidentUrl = "https://icm.ad.msft.net/imp/IncidentDetails.aspx?id="+$item.id
             Start-Process $incidentUrl
            }
         }
        Write-Host $sev2SLA, $sev3SLA, $sev4SLA -ForegroundColor Yellow          
    }
    else 
    {
        write-host "$(Get-Date): No incident found near to SLA!" -ForegroundColor Green
    } 

    } 


while(1)
{

try{

$date = Get-Date 
Write-Host "$date : Querying Items in WADE Queue "
get-ActionableWorkItemsRDTask
Start-Sleep 10 
TFS-Incident
Start-Sleep 10 
get-ActionableWorkItemsRTO
Start-Sleep 10 
 Get-IncidentsNearTTE
 Start-Sleep 10

Write-Host "Sleeping for 10 Seconds"
if($myICMCertificate)
{
        
        Write-Host ""
        Get-IcMIncidentsInTriage
        $sleepDuration = 0
                Write-Host "Sleeping for $sleepDuration seconds"
       Start-Sleep -Seconds $sleepDuration
    
}
else
{
    Write-Host "ICM TriageLooper Certificate not found. Please install and retry" -ForegroundColor Yellow
}

}
catch
{

write-host "There is an exception in the looper please check the powershell window for more details "
  $MessageBody = "There is an exception in the looper please check the powershell window for more details "
$MessageTitle = " Exception in the looper"
$result= Show-MessageBox $MessageTitle $MessageBody
}

}

