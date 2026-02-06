# Docker Compose and Just Command Setup

Each Qwen3 app folder now includes:
- `docker-compose.yml` - Docker Compose configuration to run the app
- `Dockerfile` - Docker image definition
- `justfile` - Command shortcuts using [Just](https://github.com/casey/just)

## Prerequisites

1. **Docker & Docker Compose**: Install from [docker.com](https://docs.docker.com/get-docker/)
2. **NVIDIA Docker Runtime**: For GPU support, install [nvidia-docker](https://github.com/NVIDIA/nvidia-docker)
3. **Just** (optional): Install from [just.systems](https://just.systems/)
4. **HuggingFace Token**: Set your HF token as an environment variable:
   ```bash
   export HF_TOKEN="your_huggingface_token_here"
   ```

## Quick Start

### Using Just (Recommended)

Each app folder contains a `justfile` with convenient commands:

```bash
cd Qwen3-ASR

# Show available commands
just

# Build and start the app
just build
just up

# View logs
just logs

# Stop the app
just down
```

### Using Docker Compose Directly

```bash
cd Qwen3-ASR

# Build and start
docker-compose build
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## Available Commands (Just)

Each `justfile` provides these commands:

- `just build` - Build the Docker image
- `just up` - Start the application in detached mode
- `just up-logs` - Start the application with logs
- `just down` - Stop the application
- `just restart` - Restart the application
- `just logs` - View application logs
- `just status` - Check container status
- `just clean` - Remove containers and volumes
- `just rebuild` - Clean rebuild and restart
- `just shell` - Open a shell in the container
- `just run-local` - Run the app locally (without Docker)
- `just install` - Install dependencies locally

## App Folders and Ports

Each app is configured to run on a different port to avoid conflicts:

| App Folder | Port | URL |
|------------|------|-----|
| Qwen-Image-2512 | 7860 | http://localhost:7860 |
| Qwen-Image-Edit-2511 | 7861 | http://localhost:7861 |
| Qwen-Image-Layered | 7862 | http://localhost:7862 |
| Qwen3-ASR | 7863 | http://localhost:7863 |
| Qwen3-TTS | 7864 | http://localhost:7864 |
| Qwen3-TTS-Voice-Design | 7865 | http://localhost:7865 |

## Environment Variables

Set these environment variables before running:

```bash
# Required: Your HuggingFace token
export HF_TOKEN="your_token_here"

# Optional: Gradio server settings (already configured in docker-compose.yml)
export GRADIO_SERVER_NAME="0.0.0.0"
export GRADIO_SERVER_PORT="7860"
```

## Running Multiple Apps Simultaneously

You can run multiple apps at the same time since they use different ports:

```bash
# Terminal 1
cd Qwen3-ASR && just up-logs

# Terminal 2
cd Qwen3-TTS && just up-logs
```

## Troubleshooting

### GPU Not Detected
Ensure NVIDIA Docker runtime is installed and configured:
```bash
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

### Port Already in Use
Check if the port is already in use:
```bash
lsof -i :7860
```

Change the port in `docker-compose.yml` if needed:
```yaml
ports:
  - "7870:7860"  # Use 7870 on host instead
```

### Permission Denied
Add your user to the docker group:
```bash
sudo usermod -aG docker $USER
newgrp docker
```

## Development

### Local Development (without Docker)

```bash
cd Qwen3-ASR

# Install dependencies
just install
# or
pip3 install -r requirements.txt

# Run the app
just run-local
# or
python3 app.py
```

### Accessing Container Shell

```bash
cd Qwen3-ASR
just shell
# or
docker-compose exec qwen3-asr bash
```

## Notes

- Each app maintains its own HuggingFace model cache in a Docker volume
- Containers restart automatically unless stopped with `just down`
- GPU support requires NVIDIA Docker runtime
- The apps require significant GPU memory to run
