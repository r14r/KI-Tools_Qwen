# Quick Start Examples

This guide provides step-by-step examples for running the Qwen3 apps using Docker Compose and Just.

## Prerequisites Check

Before starting, verify you have the necessary tools:

```bash
# Check Docker installation
docker --version
docker-compose --version

# Check NVIDIA Docker runtime (for GPU support)
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi

# Check Just installation (optional but recommended)
just --version

# Check if HF_TOKEN is set
echo $HF_TOKEN
```

If any of these fail, refer to [DOCKER_SETUP.md](DOCKER_SETUP.md) for installation instructions.

## Example 1: Running a Single App (Qwen3-ASR)

### Using Just (Recommended)

```bash
# 1. Navigate to the app folder
cd Qwen3-ASR

# 2. Set your HuggingFace token
export HF_TOKEN="your_token_here"

# 3. Build the Docker image
just build

# 4. Start the application
just up

# 5. Check the logs
just logs

# 6. Access the app at http://localhost:7863

# 7. Stop the app when done
just down
```

### Using Docker Compose Directly

```bash
# 1. Navigate to the app folder
cd Qwen3-ASR

# 2. Set your HuggingFace token
export HF_TOKEN="your_token_here"

# 3. Build and start
docker-compose build
docker-compose up -d

# 4. View logs
docker-compose logs -f

# 5. Access the app at http://localhost:7863

# 6. Stop when done
docker-compose down
```

## Example 2: Running Multiple Apps

### Using the Root Justfile

```bash
# From the repository root
cd /path/to/KI-Tools_Qwen

# Set your HuggingFace token
export HF_TOKEN="your_token_here"

# Build all apps (this will take a while)
just build-all

# Start all apps
just up-all

# Check status of all apps
just status

# Access the apps:
# - Qwen-Image-2512:         http://localhost:7860
# - Qwen-Image-Edit-2511:    http://localhost:7861
# - Qwen-Image-Layered:      http://localhost:7862
# - Qwen3-ASR:               http://localhost:7863
# - Qwen3-TTS:               http://localhost:7864
# - Qwen3-TTS-Voice-Design:  http://localhost:7865

# Stop all apps when done
just down-all
```

### Running Specific Apps from Root

```bash
# Start only ASR
just up-asr

# Start only TTS
just up-tts

# View ASR logs
just logs-asr

# View TTS logs
just logs-tts

# Stop ASR
just down-asr
```

## Example 3: Development Workflow

### Make Changes and Test

```bash
cd Qwen3-ASR

# Edit files in your favorite editor
vim app.py

# Rebuild and restart to see changes
just rebuild

# Or rebuild without cache
just clean
just build
just up

# View logs in real-time
just logs
```

### Debug Inside Container

```bash
cd Qwen3-ASR

# Start the app
just up

# Open a shell in the running container
just shell

# Inside the container, you can:
# - Check Python environment: python3 --version
# - Check installed packages: pip3 list
# - Run manual tests: python3 -c "import gradio; print(gradio.__version__)"
# - Check CUDA: python3 -c "import torch; print(torch.cuda.is_available())"

# Exit the shell
exit
```

## Example 4: Using Environment Variables

### Option 1: Using .env File

```bash
# 1. Copy the example file
cp .env.example .env

# 2. Edit .env and add your token
nano .env

# 3. Docker Compose will automatically load .env
cd Qwen3-ASR
docker-compose up -d
```

### Option 2: Inline Environment Variables

```bash
cd Qwen3-ASR
HF_TOKEN="your_token_here" docker-compose up -d
```

### Option 3: Export for Session

```bash
# Set for current terminal session
export HF_TOKEN="your_token_here"

# This will be available for all docker-compose commands
cd Qwen3-ASR
just up
```

## Example 5: Managing Resources

### Check Resource Usage

```bash
# View Docker stats
docker stats

# Check disk usage
docker system df

# List all running containers
docker ps

# List all containers (including stopped)
docker ps -a
```

### Clean Up Resources

```bash
# Clean specific app
cd Qwen3-ASR
just clean

# Clean all apps (from root)
just clean-all

# Remove unused Docker resources
docker system prune -a

# Remove all volumes (WARNING: deletes model caches)
docker volume prune
```

## Example 6: Troubleshooting

### Check Container Logs

```bash
cd Qwen3-ASR

# View recent logs
just logs

# View logs with timestamps
docker-compose logs -f --timestamps

# View logs for last 100 lines
docker-compose logs --tail=100
```

### Restart Container

```bash
cd Qwen3-ASR

# Restart without rebuilding
just restart

# Full rebuild
just rebuild
```

### Check Container Status

```bash
cd Qwen3-ASR

# Check if container is running
just status

# Or use docker commands
docker ps | grep qwen3-asr
```

## Example 7: Port Conflicts

If a port is already in use, you can change it:

```bash
cd Qwen3-ASR

# Edit docker-compose.yml
nano docker-compose.yml

# Change the port mapping (e.g., 7863 -> 8000)
# ports:
#   - "8000:7860"

# Rebuild and restart
just rebuild

# Access at http://localhost:8000
```

## Example 8: Running Without GPU

If you don't have a GPU or want to run on CPU:

```bash
cd Qwen3-ASR

# Edit docker-compose.yml and remove the deploy section
nano docker-compose.yml

# Remove these lines:
#   deploy:
#     resources:
#       reservations:
#         devices:
#           - driver: nvidia
#             count: all
#             capabilities: [gpu]

# Save and rebuild
just rebuild
```

**Note:** Running on CPU will be significantly slower.

## Example 9: Viewing Available Commands

```bash
# Show all commands for an app
cd Qwen3-ASR
just

# Show all commands from root
cd /path/to/KI-Tools_Qwen
just
```

## Example 10: Monitoring All Apps

```bash
# From root, check all app statuses
just status

# View logs from all apps (in separate terminals)
# Terminal 1
cd Qwen3-ASR && just logs

# Terminal 2
cd Qwen3-TTS && just logs

# Terminal 3
cd Qwen-Image-2512 && just logs
```

## Tips and Best Practices

1. **Always set HF_TOKEN** before starting apps
2. **Use `just` commands** for convenience
3. **Monitor logs** when first starting an app
4. **Check GPU availability** if you have issues
5. **Clean up regularly** to save disk space
6. **Use different ports** to run multiple apps simultaneously
7. **Keep Docker updated** for best performance
8. **Use volumes** for persistent model caches (already configured)

## Common Issues

### "Permission denied" error
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### "Port already in use"
```bash
# Find what's using the port
lsof -i :7863

# Kill the process or change the port in docker-compose.yml
```

### "NVIDIA driver not found"
```bash
# Check NVIDIA driver
nvidia-smi

# Install NVIDIA Docker runtime
# See DOCKER_SETUP.md for instructions
```

### "Out of memory"
```bash
# Check available GPU memory
nvidia-smi

# Reduce model size or close other GPU applications
```

## Next Steps

- Read [DOCKER_SETUP.md](DOCKER_SETUP.md) for detailed documentation
- Explore individual app READMEs for app-specific features
- Customize docker-compose.yml for your needs
- Add more apps using the same pattern

## Getting Help

If you encounter issues:

1. Check the logs: `just logs`
2. Verify GPU availability: `nvidia-smi`
3. Check Docker status: `docker ps`
4. Review DOCKER_SETUP.md for troubleshooting
5. Check HuggingFace model access permissions
