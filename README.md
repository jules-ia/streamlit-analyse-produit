# Analyse Produit

A Streamlit app deployed on Snowflake

## Quick Start

1. **Install dependencies:**
   ```bash
   conda env create -f environment.yml
   conda activate analyse_produit_env
   ```

2. **Configure Snowflake connection:**
   ```bash
   snowflake connection add analyse_produit \
     --account zq05791.europe-west4.gcp \
     --user YOUR_USERNAME \
     --password YOUR_PASSWORD \
     --warehouse WH_DEV \
     --database DHB_PROD \
     --schema DNR
   ```

3. **Deploy to Snowflake:**
   ```bash
   snowflake streamlit deploy \
     --connection analyse_produit \
     --name analyse_produit \
     --stage analyse_produit_stage \
     --warehouse WH_DEV
   ```

## Configuration

- **Account:** zq05791.europe-west4.gcp
- **Warehouse:** WH_DEV
- **Database:** DHB_PROD
- **Schema:** DNR
- **Stage:** analyse_produit_stage

## Development

Run locally:
```bash
streamlit run streamlit_app.py
```

## GitHub Actions Deployment

This project includes automated deployment to Snowflake via GitHub Actions.

### Setup GitHub Secrets

To enable automatic deployment, configure the following secrets in your GitHub repository:

1. Go to your repository → Settings → Secrets and variables → Actions
2. Add the following repository secrets:

```
SNOWFLAKE_PRIVATE_KEY=<your-private-key-content>
```

### Deployment Triggers

The workflow automatically deploys when:
- Code is pushed to `main` or `master` branch
- Pull requests are created/updated
- Manual trigger via GitHub Actions UI

### Manual Deployment

You can also deploy manually using the Snowflake CLI:

```bash
# Install dependencies
pip install streamlit snowflake-snowpark-python snowflake-cli-labs

# Deploy
snow streamlit deploy streamlit_app \
  --replace \
  --account zq05791.europe-west4.gcp \
  --user cloubet@jules.com \
  --private-key-file /home/clement/Documents/jules/keys/clement_loubet.pem \
  --authenticator SNOWFLAKE_JWT \
  --warehouse WH_DEV \
  --database DHB_PROD \
  --schema DNR \
  --role DHB_ENGINEER \
  --temporary-connection
```

## Author

Clement Loubet - cloubet@jules.com
