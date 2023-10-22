$ErrorActionPreference = "Stop"
$command = $args[0]


function Install {
    Write-Output "Installing client libraries"
    npm install
}


function Load-Env {
    get-content .env | foreach {
        $name, $value = $_.split('=')
        if ( $name -eq 'ENVIRONMENT') {
            return $value
        }
        #set-content env:\$name $value
    }
}

function Init-Client() {
    Write-Output "Initialising client"
    npm run init
}

function Init-Website-Deploy([string]$environment) {
    $key = "key=website_watcher_js/$environment/website_deploy/terraform.tfstate"
    Write-Output $key
    Set-Location terraform/website_deploy
    terraform init -backend-config $key -reconfigure
    $text = 'environment="' + $environment + '"'
    $text | Out-File -FilePath "terraform.tfvars" -Encoding utf8
    Set-Location ../..
}


function Build-Client() {
    Write-Output "Building client"
    npm run build
}


switch ($command) {
    # One-time setup
    "install" { Install }
    # Environment setup
    "init" { 
        $environment = Load-Env
        if ($environment) {
            Write-Output "Setting environment to: $environment"
            Init-Website-Deploy $environment
            Init-Client
        } else {
            Write-Output "Did not find the environment"
        }
    }
    default {
        Write-Output "Unrecognised command. See make.ps1 for list of valid commands."
    }
}
