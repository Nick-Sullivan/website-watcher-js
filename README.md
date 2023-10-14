## Creating

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

## Getting Started

First, run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/basic-features/font-optimization) to automatically optimize and load Inter, a custom Google Font.

## Notes

https://tailwindcss.com/docs/grid-template-columns
https://flowbite.com/docs/getting-started/quickstart/
https://www.flowbite-react.com/docs/components/card#
https://github.com/tulupinc/flowbite-next-starter
https://ui.shadcn.com/docs/installation/next
https://nextui.org/docs/guide/installation
