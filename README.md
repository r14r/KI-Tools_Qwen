# KI-Tools_Qwen

A collection of Qwen3 AI applications with Docker Compose and Just command automation.

## 📦 Available Apps

This repository contains 6 Qwen3-powered applications using Gradio:

| App | Description | Port |
|-----|-------------|------|
| **Qwen-Image-2512** | Image generation with Qwen | 7860 |
| **Qwen-Image-Edit-2511** | Image editing capabilities | 7861 |
| **Qwen-Image-Layered** | Layered image processing | 7862 |
| **Qwen3-ASR** | Automatic Speech Recognition (52+ languages) | 7863 |
| **Qwen3-TTS** | Text-to-Speech synthesis | 7864 |
| **Qwen3-TTS-Voice-Design** | Custom voice design TTS | 7865 |

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- NVIDIA GPU with CUDA support (recommended)
- NVIDIA Docker runtime
- HuggingFace account and token
- Just (optional, for convenient commands)

### Run a Single App

```bash
# Set your HuggingFace token
export HF_TOKEN="your_token_here"

# Navigate to any app folder
cd Qwen3-ASR

# Build and start
just build
just up

# Access at http://localhost:7863
```

### Run All Apps

```bash
# From repository root
export HF_TOKEN="your_token_here"

just build-all
just up-all

# Access apps at ports 7860-7865
```

## 📖 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Step-by-step examples and usage patterns
- **[DOCKER_SETUP.md](DOCKER_SETUP.md)** - Detailed Docker and Just setup guide
- **[.env.example](.env.example)** - Environment variable template

## 🛠️ Available Commands

Each app folder includes a `justfile` with these commands:

```bash
just build      # Build Docker image
just up         # Start app (detached)
just up-logs    # Start app with logs
just down       # Stop app
just logs       # View logs
just status     # Check status
just clean      # Remove containers and volumes
just rebuild    # Full rebuild
just shell      # Open container shell
just run-local  # Run without Docker
just install    # Install dependencies locally
```

Root-level commands (from repository root):

```bash
just build-all  # Build all apps
just up-all     # Start all apps
just down-all   # Stop all apps
just status     # Check all apps status
just clean-all  # Clean all apps

# Individual app commands
just up-asr     # Start ASR
just up-tts     # Start TTS
just logs-asr   # View ASR logs
# ... and more
```

## 📋 Project Structure

```
KI-Tools_Qwen/
├── Qwen-Image-2512/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── justfile
├── Qwen-Image-Edit-2511/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── justfile
├── Qwen-Image-Layered/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── justfile
├── Qwen3-ASR/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── justfile
├── Qwen3-TTS/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── justfile
├── Qwen3-TTS-Voice-Design/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── justfile
├── justfile (root - manage all apps)
├── DOCKER_SETUP.md
├── QUICKSTART.md
├── .env.example
└── README.md
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file from the template:

```bash
cp .env.example .env
# Edit .env and add your HuggingFace token
```

Or export directly:

```bash
export HF_TOKEN="your_huggingface_token"
```

### Custom Ports

Edit `docker-compose.yml` in any app folder to change ports:

```yaml
ports:
  - "8000:7860"  # Change 8000 to your desired port
```

## 🐛 Troubleshooting

### GPU Not Detected
```bash
# Check NVIDIA driver
nvidia-smi

# Test NVIDIA Docker runtime
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

### Port Already in Use
```bash
# Find process using port
lsof -i :7860

# Kill process or change port in docker-compose.yml
```

### Permission Denied
```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

For more troubleshooting, see [DOCKER_SETUP.md](DOCKER_SETUP.md).

## 📚 Resources

- [Qwen3-ASR](https://huggingface.co/collections/Qwen/qwen3-asr)
- [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS)
- [Docker Documentation](https://docs.docker.com/)
- [Just Command Runner](https://just.systems/)

## 📄 License

See individual app folders for license information.

## 🤝 Contributing

Contributions are welcome! Please ensure:

1. Docker Compose files follow the existing pattern
2. Justfiles include all standard commands
3. Documentation is updated
4. Apps use unique ports

## ⚠️ Requirements

- **GPU**: NVIDIA GPU with 8GB+ VRAM (recommended for optimal performance)
- **RAM**: 16GB+ system RAM
- **Disk**: 50GB+ free space for models and Docker images
- **OS**: Linux with NVIDIA drivers (Windows/Mac with WSL2/Docker Desktop)

## 🎯 Next Steps

1. Read [QUICKSTART.md](QUICKSTART.md) for detailed examples
2. Choose an app to run
3. Set your HF_TOKEN
4. Run `just build && just up`
5. Access the app in your browser!

## 💡 Tips

- Use `just` for convenient commands
- Run multiple apps on different ports
- Models are cached in Docker volumes
- Check logs with `just logs` if issues occur
- GPU is required for reasonable performance
