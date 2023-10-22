## Getting started

1. Install libraries

```bash
./make.ps1 install
```

2. Set target environment by populating a .env with the following

```
# If you change any of these variables, run "./make.ps1 init"

# The cloud environment to point to
ENVIRONMENT=dev

# True to make the local server use a local database
USE_LOCAL_INFRA=False

# When running the server locally, all incoming requests will be from this user
COGNITO_USER_ID='f8f6e81d-1e98-47d8-914c-6e54b3ed7ef4'
```

3. Initialise terraform to point at your environment

```bash
./make.ps1 init
```

4. Run unit tests

```bash
./make.ps test
```

5. Deploy server

```bash
cd terraform/foundation
terraform apply
cd ../infrastructure
terrafrm apply
```

6. Run API tests

```bash
./make.ps test-api
```
