# Installation Guide

## System Requirements

- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum (4GB recommended)
- **Display**: 1024x768 minimum resolution

## Installation Steps

### Method 1: Using pip (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/Vikas8346/-Ai-based-maze-solver.git
   cd -Ai-based-maze-solver
   ```

2. **Create virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   python -c "import pygame, matplotlib, numpy; print('All dependencies installed successfully!')"
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

### Method 2: Manual Installation

If you encounter issues with requirements.txt:

```bash
pip install pygame==2.5.2
pip install matplotlib==3.8.2
pip install numpy==1.26.2
```

## Troubleshooting

### Pygame Installation Issues

**Windows:**
```bash
pip install pygame --upgrade
```

**macOS:**
```bash
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf
pip install pygame
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-pygame
```

### Matplotlib Backend Issues

If you see errors related to matplotlib display:

```bash
# Install tkinter
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS (already included)

# Windows (already included)
```

### Import Errors

If you see "ModuleNotFoundError":

1. Ensure you're in the project root directory
2. Activate your virtual environment
3. Reinstall dependencies

```bash
pip install -r requirements.txt --force-reinstall
```

## Platform-Specific Notes

### Windows
- Ensure Python is added to PATH
- Use PowerShell or Command Prompt
- May need to run as Administrator for first-time setup

### macOS
- May need Xcode Command Line Tools: `xcode-select --install`
- Use Terminal app
- Pygame may require SDL libraries via Homebrew

### Linux
- May need development packages: `sudo apt-get install python3-dev`
- For GUI, ensure X server is running
- Use any terminal emulator

## Docker Installation (Alternative)

If you prefer using Docker:

```dockerfile
# Create Dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    python3-tk

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py", "--console"]
```

Build and run:
```bash
docker build -t maze-solver .
docker run -it maze-solver
```

Note: GUI mode won't work in Docker without X11 forwarding.

## Verification

After installation, test all features:

```bash
# Test console mode
python main.py --console

# Test interactive mode
python main.py --interactive

# Run unit tests
python -m pytest tests/ -v
```

If all tests pass, you're ready to use the maze solver!

## Getting Help

If you encounter issues:

1. Check the [FAQ](FAQ.md)
2. Search existing [GitHub Issues](https://github.com/Vikas8346/-Ai-based-maze-solver/issues)
3. Create a new issue with:
   - Your OS and Python version
   - Complete error message
   - Steps to reproduce
