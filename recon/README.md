# Recon Module Guide

The `recon/` directory stores data and modules related to reconnaissance activities.

## Structure
- `Burp logs/`         # Store Burp Suite logs here
- `endpoints.json`     # Discovered endpoints
- `params.json`        # Discovered parameters
- `Screenshots/`       # Screenshots from recon
- `responses/`         # HTTP responses and artifacts

## Adding Recon Modules
- Place scripts or tools for recon in this directory or subfolders.
- Document each module's usage and output format.

## Data Handling
- Sensitive data (screenshots, logs) should be handled securely and is ignored by .gitignore.
- Standardize output formats (JSON preferred) for easy integration.

## Example Workflow
1. Run endpoint discovery tool, output to `endpoints.json`.
2. Run parameter discovery, output to `params.json`.
3. Collect screenshots and responses as needed.

See the main README for more details.
