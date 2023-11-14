## Steps I did to create

Install NextJS

```bash
npx create-next-app@latest
√ What is your project named? ... website
√ Would you like to use TypeScript? ... No
√ Would you like to use ESLint? ... Yes
√ Would you like to use Tailwind CSS? ... Yes
√ Would you like to use `src/` directory? ... No
√ Would you like to use App Router? (recommended) ... Yes
√ Would you like to customize the default import alias (@/*)? ... Yes
√ What import alias would you like configured? ... @/*
```

Install [Flowbite component library](https://www.flowbite-react.com/docs/getting-started/nextjs)

```bash
cd website
npm install --save autoprefixer postcss tailwindcss flowbite flowbite-react cookies-next
```

Install auth

```bash
npm install @aws-sdk/client-cognito-identity-provider aws-crt
```

Install esline VSCode extension, with this: https://stackoverflow.com/questions/68163385/parsing-error-cannot-find-module-next-babel

Install prettier VSCode extension, with this: https://nextjs.org/docs/pages/building-your-application/configuring/eslint#prettier

## Required tech

Python3.9
Docker desktop
Bruno
Terraform

## Getting started

./makefile.ps1 install
./makefile.ps1 deploy

Use VSCode Run to run the website locally

## Notes

https://tailwindcss.com/docs/grid-template-columns
https://flowbite.com/docs/getting-started/quickstart/
https://www.flowbite-react.com/docs/components/card#
https://github.com/tulupinc/flowbite-next-starter
https://ui.shadcn.com/docs/installation/next
https://nextui.org/docs/guide/installation

if docker desktop doesn't start
open administrator powershell

```bash
wsl -l -v
```

if not responding, go to installed apps & features, find Windows Subsystem for Linux, click advanced features. Click repair or reset, then reboot
then start with wsl.exe

## Rules

Able to run server locally with no internet connection (and hit with bruno/client/api tests)
Able to run server locally and point to cloud resources
Able to run client locally
Switching from local to development is in a single location
Able to spin up a custom environment
Minimal difference between CICD and dev setup
As few technologies as possible
Each endpoint has its own cloudwatch log group
Installing is a single command
A makefile can help, but all steps should be able to be done simply

# Notes

- apply before destroy
- don't mix local with CICD terraform
