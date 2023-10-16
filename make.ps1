$ErrorActionPreference = "Stop"
$command = $args[0]


function Build {
    Write-Output "Building client"
    Set-Location client
    npm run build
    Set-Location ..
}

function Deploy-Foundation {
    Write-Output "Deploying foundation"
    Set-Location terraform/environments/stage/foundation
    terraform apply
    Set-Location ../../../..
}

function Deploy-Infrastructure {
    Write-Output "Deploying infrastructure"
    Set-Location terraform/environments/stage/infrastructure
    terraform apply
    Set-Location ../../../..
}

function Deploy-Website {
    Write-Output "Deploying website"
    Set-Location terraform/environments/stage/website
    terraform apply
    Set-Location ../../../..
}

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

function Freeze {
    Write-Output "Updating server/requirements.txt"
    Set-Location server
    ./.venv/Scripts/activate
    pip freeze > requirements.txt
    Set-Location ..
    deactivate
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



switch ($command) {
    "build" { Build }
    "deploy" { 
        Deploy-Foundation
        Deploy-Infrastructure
        Deploy-Website
    }
    "deploy-foundation" { Deploy-Foundation }
    "deploy-infra" { Deploy-Infrastructure }
    "deploy-website" { Deploy-Website }
    "freeze" { Freeze }
    "install" { 
        Install-Server 
        Install-Client 
    }
    "test" { 
        Test-Server
    }
    "test-api" { 
        Test-Api
    }
    default {
        Write-Output "Unrecognised command. See make.ps1 for list of valid commands."
    }
}
