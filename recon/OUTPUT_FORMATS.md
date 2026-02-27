# Output and Reporting Formats

Super_red_team_bot supports standardized output and reporting formats to ensure results are easy to parse, analyze, and share.

## Recommended Formats
- **JSON**: Preferred for structured data (endpoints, parameters, findings, logs)
- **CSV**: For tabular data exports
- **HTML/Markdown**: For human-readable reports
- **Screenshots/Images**: Store in `recon/Screenshots/` with descriptive filenames

## Output Directory Structure
- All output should be saved under the `recon/` directory or a user-specified output directory.
- Use subfolders for logs, screenshots, and responses as needed.

## Example JSON Output (endpoints.json)
```json
[
  {
    "url": "https://example.com/api/v1/user",
    "method": "GET",
    "auth_required": true,
    "parameters": ["id", "token"]
  }
]
```

## Example CSV Output
```
url,method,auth_required,parameters
https://example.com/api/v1/user,GET,true,"id;token"
```

## Example Markdown/HTML Report
```
# Reconnaissance Report

## Endpoints
- `GET https://example.com/api/v1/user` (auth required)

## Parameters
- id
- token
```

## Best Practices
- Always include timestamps and context in reports.
- Use consistent field names and data types.
- Document any custom output formats in the module or plugin README.

See the main README for more details on running modules and generating reports.
