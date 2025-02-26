# IDV Package with Isolated Liveness Detection

This project implements an IDV (Identity Verification) package with an isolated liveness detection service. The architecture separates resource-intensive ML operations into a dedicated microservice for better resource management and scalability.

## Project Structure

```
.
├── idvpackage/           # Main IDV package
│   ├── ocr.py           # OCR and document processing
│   └── ...              # Other IDV components
│
└── liveness_api/        # Isolated Liveness Detection Service
    ├── app/
    │   ├── main.py      # FastAPI application
    │   └── liveness_detector.py  # ML model handling
    ├── spoof_resources/ # ML model resources
    ├── Dockerfile       # Container configuration
    └── requirements.txt # Service dependencies
```

## Architecture

The project uses a microservices architecture where:

1. The main IDV package handles document processing and orchestration
2. Liveness detection is offloaded to a separate service that:
   - Manages its own memory and resources
   - Can be scaled independently
   - Provides GPU acceleration when available
   - Handles cleanup of temporary resources

## Deployment

- The main IDV package can be installed as a Python package
- The liveness detection service is deployed separately on Hugging Face Spaces
- See `liveness_api/README.md` for detailed deployment instructions

## Benefits

- Improved resource management
- Independent scaling of components
- Better error isolation
- Simplified maintenance
- Optional GPU acceleration
- Reduced memory pressure on main package

## Usage

1. Install the IDV package
2. Deploy the liveness service
3. Set the `LIVENESS_API_ENDPOINT` environment variable
4. Use the IDV package as normal - it will automatically communicate with the liveness service
