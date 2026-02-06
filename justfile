# Root Justfile for managing all Qwen3 apps

# Default recipe to display help
default:
    @just --list

# Show status of all apps
status:
    @echo "=== Qwen-Image-2512 ==="
    @cd Qwen-Image-2512 && docker compose ps || true
    @echo "\n=== Qwen-Image-Edit-2511 ==="
    @cd Qwen-Image-Edit-2511 && docker compose ps || true
    @echo "\n=== Qwen-Image-Layered ==="
    @cd Qwen-Image-Layered && docker compose ps || true
    @echo "\n=== Qwen3-ASR ==="
    @cd Qwen3-ASR && docker compose ps || true
    @echo "\n=== Qwen3-TTS ==="
    @cd Qwen3-TTS && docker compose ps || true
    @echo "\n=== Qwen3-TTS-Voice-Design ==="
    @cd Qwen3-TTS-Voice-Design && docker compose ps || true

# Build all Docker images
build-all:
    @echo "Building all apps..."
    cd Qwen-Image-2512 && docker compose build
    cd Qwen-Image-Edit-2511 && docker compose build
    cd Qwen-Image-Layered && docker compose build
    cd Qwen3-ASR && docker compose build
    cd Qwen3-TTS && docker compose build
    cd Qwen3-TTS-Voice-Design && docker compose build
    @echo "All apps built successfully!"

# Start all apps
up-all:
    @echo "Starting all apps..."
    cd Qwen-Image-2512 && docker compose up -d
    cd Qwen-Image-Edit-2511 && docker compose up -d
    cd Qwen-Image-Layered && docker compose up -d
    cd Qwen3-ASR && docker compose up -d
    cd Qwen3-TTS && docker compose up -d
    cd Qwen3-TTS-Voice-Design && docker compose up -d
    @echo "All apps started!"
    @echo "\nAccess the apps at:"
    @echo "  - Qwen-Image-2512:         http://localhost:7860"
    @echo "  - Qwen-Image-Edit-2511:    http://localhost:7861"
    @echo "  - Qwen-Image-Layered:      http://localhost:7862"
    @echo "  - Qwen3-ASR:               http://localhost:7863"
    @echo "  - Qwen3-TTS:               http://localhost:7864"
    @echo "  - Qwen3-TTS-Voice-Design:  http://localhost:7865"

# Stop all apps
down-all:
    @echo "Stopping all apps..."
    cd Qwen-Image-2512 && docker compose down || true
    cd Qwen-Image-Edit-2511 && docker compose down || true
    cd Qwen-Image-Layered && docker compose down || true
    cd Qwen3-ASR && docker compose down || true
    cd Qwen3-TTS && docker compose down || true
    cd Qwen3-TTS-Voice-Design && docker compose down || true
    @echo "All apps stopped!"

# View logs from all apps
logs-all:
    @echo "Showing logs from all apps (Ctrl+C to exit)..."
    docker compose -f Qwen-Image-2512/docker-compose.yml logs -f &
    docker compose -f Qwen-Image-Edit-2511/docker-compose.yml logs -f &
    docker compose -f Qwen-Image-Layered/docker-compose.yml logs -f &
    docker compose -f Qwen3-ASR/docker-compose.yml logs -f &
    docker compose -f Qwen3-TTS/docker-compose.yml logs -f &
    docker compose -f Qwen3-TTS-Voice-Design/docker-compose.yml logs -f &
    wait

# Clean all containers and volumes
clean-all:
    @echo "Cleaning all apps..."
    cd Qwen-Image-2512 && docker compose down -v || true
    cd Qwen-Image-Edit-2511 && docker compose down -v || true
    cd Qwen-Image-Layered && docker compose down -v || true
    cd Qwen3-ASR && docker compose down -v || true
    cd Qwen3-TTS && docker compose down -v || true
    cd Qwen3-TTS-Voice-Design && docker compose down -v || true
    @echo "All apps cleaned!"

# Individual app commands

# Qwen-Image-2512
build-image-2512:
    cd Qwen-Image-2512 && docker compose build

up-image-2512:
    cd Qwen-Image-2512 && docker compose up -d

down-image-2512:
    cd Qwen-Image-2512 && docker compose down

logs-image-2512:
    cd Qwen-Image-2512 && docker compose logs -f

# Qwen-Image-Edit-2511
build-image-edit:
    cd Qwen-Image-Edit-2511 && docker compose build

up-image-edit:
    cd Qwen-Image-Edit-2511 && docker compose up -d

down-image-edit:
    cd Qwen-Image-Edit-2511 && docker compose down

logs-image-edit:
    cd Qwen-Image-Edit-2511 && docker compose logs -f

# Qwen-Image-Layered
build-image-layered:
    cd Qwen-Image-Layered && docker compose build

up-image-layered:
    cd Qwen-Image-Layered && docker compose up -d

down-image-layered:
    cd Qwen-Image-Layered && docker compose down

logs-image-layered:
    cd Qwen-Image-Layered && docker compose logs -f

# Qwen3-ASR
build-asr:
    cd Qwen3-ASR && docker compose build

up-asr:
    cd Qwen3-ASR && docker compose up -d

down-asr:
    cd Qwen3-ASR && docker compose down

logs-asr:
    cd Qwen3-ASR && docker compose logs -f

# Qwen3-TTS
build-tts:
    cd Qwen3-TTS && docker compose build

up-tts:
    cd Qwen3-TTS && docker compose up -d

down-tts:
    cd Qwen3-TTS && docker compose down

logs-tts:
    cd Qwen3-TTS && docker compose logs -f

# Qwen3-TTS-Voice-Design
build-tts-voice-design:
    cd Qwen3-TTS-Voice-Design && docker compose build

up-tts-voice-design:
    cd Qwen3-TTS-Voice-Design && docker compose up -d

down-tts-voice-design:
    cd Qwen3-TTS-Voice-Design && docker compose down

logs-tts-voice-design:
    cd Qwen3-TTS-Voice-Design && docker compose logs -f
