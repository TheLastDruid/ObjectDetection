# Contributing to ObjectDetection

Thank you for your interest in contributing to the ObjectDetection project! This document provides guidelines for contributing to this project.

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Submitting Changes](#submitting-changes)
- [Code Style](#code-style)
- [Testing](#testing)

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ObjectDetection.git
   cd ObjectDetection
   ```
3. **Set up the development environment** following the instructions in [README.md](README.md)

## 🛠️ Development Setup

### Prerequisites
- Python 3.8+
- Git
- Virtual environment support

### Setup Steps
1. Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

3. Run the setup script:
   ```powershell
   .\setup.ps1
   ```

## 🔄 Making Changes

### Before You Start
- Check the [issue tracker](https://github.com/YOUR_USERNAME/ObjectDetection/issues) for existing issues
- Create a new issue if you're planning a significant change
- Fork and create a feature branch for your changes

### Development Workflow
1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our code style guidelines

3. **Test your changes**:
   ```powershell
   # Test basic functionality
   python main.py --help
   
   # Test batch processing
   python batch_process.py --help
   
   # Test web interface
   python web_interface.py --help
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

## 📤 Submitting Changes

1. **Push your changes**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request** on GitHub with:
   - Clear description of the changes
   - Reference to any related issues
   - Screenshots if UI changes are involved

## 🎨 Code Style

### Python Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small

### Example:
```python
def process_image(image_path: str, model_path: str = "yolov8n.pt") -> dict:
    """
    Process a single image for object detection.
    
    Args:
        image_path: Path to the input image
        model_path: Path to the YOLO model file
        
    Returns:
        Dictionary containing detection results
    """
    # Implementation here
    pass
```

### PowerShell Scripts
- Use proper parameter validation
- Include help documentation
- Follow consistent naming conventions

## 🧪 Testing

### Manual Testing
Before submitting, ensure these work:

1. **Basic Detection**:
   ```powershell
   .\run.ps1 -Input "input/sample.jpg"
   ```

2. **Camera Functionality**:
   ```powershell
   .\camera.ps1 -Capture
   ```

3. **Batch Processing**:
   ```powershell
   .\batch.ps1 -InputPath "input" -Mode "images"
   ```

4. **Web Interface**:
   ```powershell
   .\web.ps1 -OpenBrowser
   ```

### Adding New Features
When adding new features:
- Include comprehensive error handling
- Add appropriate logging
- Update documentation
- Test with different model sizes
- Ensure PowerShell script compatibility

## 📝 Documentation

### Code Documentation
- Add docstrings to all public functions
- Include type hints where appropriate
- Comment complex algorithms or logic

### User Documentation
- Update README.md if adding new features
- Include usage examples
- Update help text in scripts

## 🐛 Bug Reports

When reporting bugs, include:
- Operating system and version
- Python version
- Complete error messages
- Steps to reproduce
- Expected vs actual behavior

## 💡 Feature Requests

For feature requests:
- Describe the use case
- Explain why it would be beneficial
- Consider implementation complexity
- Discuss potential alternatives

## 📋 Checklist for Contributors

Before submitting a PR, ensure:
- [ ] Code follows style guidelines
- [ ] All functions have docstrings
- [ ] Manual testing completed
- [ ] Documentation updated
- [ ] No sensitive information committed
- [ ] PowerShell scripts work on Windows
- [ ] Web interface remains functional

## 🤝 Community

- Be respectful and inclusive
- Help others when possible
- Share knowledge and best practices
- Follow the project's code of conduct

## 📞 Getting Help

If you need help:
- Check existing issues and documentation
- Create a new issue with detailed information
- Be patient and respectful when seeking assistance

Thank you for contributing to ObjectDetection! 🎯
