# Eye911 - Emergency Response Integration System

![Emergency Response](https://img.shields.io/badge/Emergency-Response-red)
![Python](https://img.shields.io/badge/Python-3.12-blue)

Eye911 is a sophisticated emergency response data integration system that aggregates and analyzes critical information from multiple sources including PulsePoint, NHTSA, and other emergency data feeds.

## Key Features

- **Multi-source Integration**: Combines data from PulsePoint, NHTSA FARS, and other emergency APIs
- **Real-time Analysis**: Processes and analyzes emergency response patterns
- **Dataset Mode**: Supports both live API and offline dataset modes
- **Comprehensive Documentation**: Detailed API integration guides and data mapping specifications
- **Production Ready**: Includes monitoring and deployment configurations

## Installation

```bash
# Clone the repository
git clone https://github.com/djval79/eye911.git
cd eye911

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```python
from core.integration import EmergencyResponseSystem

# Initialize with dataset mode
ers = EmergencyResponseSystem(
    pulsepoint_mode='dataset',
    nhtsa_mode='dataset',
    dataset_path='data/'
)

# Run analysis
results = ers.analyze_temporal_patterns()
```

## Documentation

- [API Integration Guide](docs/api_integration.md)
- [PulsePoint Data Mapping](docs/lafd_to_pulsepoint_mapping.md)
- [Production Checklist](docs/production_checklist.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
