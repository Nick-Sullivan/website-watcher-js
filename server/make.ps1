$ErrorActionPreference = "Stop"
$command = $args[0]


function Install {
    Write-Output "Installing server libraries"
    py -3.9 -m venv .venv  
    ./.venv/Scripts/activate
    pip install -r requirements.txt
    playwright install chromium
    deactivate
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
    $key = "key=website_watcher_js/$environment/infrastructure/terraform.tfstate"
    Write-Output $key
    Set-Location terraform/infrastructure
    terraform init -backend-config $key -reconfigure
    $text = 'environment="' + $environment + '"'
    $text | Out-File -FilePath "terraform.tfvars" -Encoding utf8
    Set-Location ../..
}

function Test-Server {
    Write-Output "Running unit tests for the server"
    ./.venv/Scripts/activate
    pytest tests/unit
    deactivate
}

function Test-Api {
    Write-Output "Running API tests for the server"
    ./.venv/Scripts/activate
    pytest tests/api
    deactivate
}

function Freeze {
    Write-Output "Updating requirements.txt"
    ./.venv/Scripts/activate
    pip freeze > requirements.txt
    deactivate
}

switch ($command) {
    # One-time setup
    "install" { Install }
    # Environment setup
    "init" { 
        $environment = Load-Env
        if ($environment) {
            Write-Output "Setting environment to: $environment"
            Init-Foundation $environment
            Init-Infrastructure $environment
        } else {
            Write-Output "Did not find the environment"
        }
    }
    # Testing
    "test" { 
        Test-Server
    }
    "test-api" { 
        Test-Api
    }
    # Adding new libraries
    "freeze" { Freeze }
    default {
        Write-Output "Unrecognised command. See make.ps1 for list of valid commands."
    }
}
