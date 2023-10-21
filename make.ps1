$ErrorActionPreference = "Stop"
$command = $args[0]


function Install-Client {
    Write-Output "Installing client libraries"
    Set-Location client
    npm install
    Set-Location ..
}

function Install-Server {
    Write-Output "Installing server libraries"
    Set-Location server
    py -3.9 -m venv .venv  
    ./.venv/Scripts/activate
    pip install -r requirements.txt
    playwright install chromium
    deactivate
    Set-Location ..
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
    Set-Location client
    npm run init
    Set-Location ..
}

function Init-Foundation([string]$environment) {
    $key = "key=website_watcher_js/$environment/foundation/terraform.tfstate"
    Write-Output $key
    Set-Location terraform/foundation
    terraform init -backend-config $key -reconfigure
    $text = 'environment="' + $environment + '"'
    $text | Out-File -FilePath "terraform.tfvars" -Encoding utf8
    Set-Location ../..
}

function Init-Infrastructure([string]$environment) {
    $key = "key=website_watcher_js/$environment/infra/terraform.tfstate"
    Write-Output $key
    Set-Location terraform/infrastructure
    terraform init -backend-config $key -reconfigure
    $text = 'environment="' + $environment + '"'
    $text | Out-File -FilePath "terraform.tfvars" -Encoding utf8
    Set-Location ../..
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


function Test-Server {
    Write-Output "Running unit tests for the server"
    ./server/.venv/Scripts/activate
    pytest server/tests/unit
    deactivate
}

function Test-Api {
    Write-Output "Running API tests for the server"
    ./server/.venv/Scripts/activate
    pytest server/tests/api
    deactivate
}

function Build-Client() {
    Write-Output "Building client"
    Set-Location client
    npm run build
    Set-Location ..
}
###


# TODO remove from terraform

function Website-Build {
    Write-Output "Building website"
    Set-Location terraform/website_build
    terraform apply
    Set-Location ../..
}

function Deploy-Website {
    Write-Output "Deploying website"
    Set-Location terraform/environments/stage/website_deploy
    terraform apply
    Set-Location ../../../..
}

function Freeze {
    Write-Output "Updating server/requirements.txt"
    Set-Location server
    ./.venv/Scripts/activate
    pip freeze > requirements.txt
    Set-Location ..
    deactivate
}



switch ($command) {
    # One-time setup
    "install" { 
        Install-Server 
        Install-Client
    }
    # Environment setup
    "init" { 
        $environment = Load-Env
        if ($environment) {
            Write-Output "Setting environment to: $environment"
            Init-Foundation $environment
            Init-Infrastructure $environment
            Init-Website-Deploy $environment
        } else {
            Write-Output "Did not find the environment"
        }
    }
    # Building client
    "build" {
        Build-Client
    }
    # Testing
    "test" { 
        Test-Server
    }
    "test-api" { 
        Test-Api
    }

    # Building website
    "website-build" { Website-Build }
    "website-deploy" { Website-Deploy }



    "apply" { 
        Foundation-Apply
        Infra-Apply
        Build-Website
        Deploy-Website
    }


    "deploy-foundation" {
        Init-Foundation
        Deploy-Foundation 
    }
    "deploy-infra" { Deploy-Infrastructure }
    "deploy-website" { Deploy-Website }
    "website-build" { Build-Website }
    "freeze" { Freeze }


    default {
        Write-Output "Unrecognised command. See make.ps1 for list of valid commands."
    }
}
