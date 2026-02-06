# Project Steering for Weekly Projects

## Directory Structure
- `weekN/`: Sub-directories for weekly projects, where N is the week number
  - `agents/`: Individual agent logic directories, as needed
    - `agent_name/`: logic, tests, and local dependencies\
  - `backend/`: For API or other backend services, as needed
  - `etc/`: Configuration management
    - `environment.sh`: Source of truth for all injectable parameters
  - `frontend/`: For frontend user interfaces, as needed
  - `iac/`: Infrastructure as Code templates
  - `makefile`: Root orchestration for builds, deployments, and local runs
  - `.gitignore`: Ignore all files and directories that should not be committed

## Build & Command Tooling
- **Primary Interface**: Always check the `makefile` for available commands before suggesting custom scripts
- **Config Injection**: Commands must source `etc/environment.sh`
- **Dependency Management (Python)**: Use `uv`
  - Commands: `uv pip install`, `uv venv`
  - Each agent in `agents/` should have its own `.venv` managed via `uv`
- **Dependency Management (TypeScript)**: Use `npm`
  - Ensure `node_modules` stay within the specific `agents/<agent_name>` directory

## Coding Standards
### Python
- Use Type Hints for all function signatures
- Prefer `unittest` for testing within agent subdirectories
- Follow PEP 8 style guidelines

### TypeScript
- Use ESM (ECMAScript Modules)
- Strict typing required (no `any` unless absolutely necessary)

### AWS IaC
- Follow the principle of least privilege in IAM templates within `iac/`
- Use environment-based naming conventions (e.g., `resource-name-${STAGE}`)
- Deployments use AWS SAM CLI

## Deployment Workflow
1. Update parameters in `etc/environment.sh`
2. Execute via `make <target>`
