## Getting started

1. Install libraries

```bash
npm install
```

2. Set target environment by populating a .env with the following

```bash
# The cloud environment to point to
ENVIRONMENT=dev
```

3. Initialise terraform to point at your environment

```bash
./make.ps1 init
```

4. Run locally

```bash
npm run dev
```

5. Build website

```bash
npm run build
```

6. Deploy website

```bash
cd terraform/website_deploy
terraform apply
```

7. To point to a local server, edit the API URL in `.env.local`
