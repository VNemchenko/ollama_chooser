# ollama_chooser

This project uses Docker Compose to run the `ollama/ollama` image.

## Deployment

Pushes to the `main` branch trigger the workflow in `.github/workflows/deploy.yaml` which syncs the project files to your server and brings up the containers using Docker Compose. Set `SERVER_IP`, `SERVER_USER` and `DEPLOY_KEY` in your repository secrets.
