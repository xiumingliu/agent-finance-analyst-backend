# Finance analyst agent (backend)

This is an AI agent for finance related tasks such as cash flow analysis based on a company's general ledge data.

## Deploy to Azure Contianer App

- Push to ACR: 

```bash
bash scripts/build_push.sh v0.x.x
```

- Create a new app revision with the latest image