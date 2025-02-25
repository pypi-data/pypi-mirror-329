# Maya CLI - Developer Documentation

## Overview
Maya CLI is a command-line interface (CLI) designed to assist in AI project generation, optimization, security enforcement, and best practices validation. This documentation provides a guide on how to use each CLI command effectively.

## Installation
Before using Maya CLI, ensure that the required dependencies are installed:
```sh
pip install -r requirements.txt
```

## Commands
### 1. Create a New AI Project
#### Command:
```sh
maya create <project_name>
```
#### Description:
Creates a new AI project structure.

#### Example:
```sh
maya create my_ai_project
```

### 2. Check Best Practices
#### Command:
```sh
maya check_best_practices [folder] [filename]
```
#### Description:
Validates Python code against best practices.

#### Example:
```sh
maya check_best_practices api my_script.py
```

### 3. Set Environment Variable
#### Command:
```sh
maya set_env <key> <value>
```
#### Description:
Sets a key-value pair in the `.env` file.

#### Example:
```sh
maya set_env OPENAI_API_KEY my_api_key
```

### 4. Optimize AI Scripts
#### Command:
```sh
maya optimize [target]
```
#### Description:
Optimizes AI scripts with caching and async processing.

#### Example:
```sh
maya optimize my_project
```

### 5. Enforce API Security
#### Command:
```sh
maya isSecured <target> [filename]
```
#### Description:
Checks and enforces API security measures including authentication, encryption, and rate limiting.

#### Example:
```sh
maya isSecured api my_api.py
```

### 6. Check Code Ethics
#### Command:
```sh
maya check_ethics <target> [filename]
```
#### Description:
Validates code efficiency, accuracy, and best practices.

#### Example:
```sh
maya check_ethics my_project
```

### 7. Generate Documentation
#### Command:
```sh
maya doc <target> <filename>
```
#### Description:
Generates a `README.md` documentation for the given file.

#### Example:
```sh
maya doc api my_script.py
```

### 8. Generate Codex Report
#### Command:
```sh
maya codex <target> <filename>
```
#### Description:
Provides an in-depth analysis and recommendations for the given file.

#### Example:
```sh
maya codex ai_model model.py
```

### 9. Enforce Compliance & Regulation
#### Command:
```sh
maya regulate <target> [filename]
```
#### Description:
Ensures compliance with GDPR, CCPA, AI Act, and ISO 42001 AI governance standards.

#### Example:
```sh
maya regulate my_project
```

## Logging
Maya CLI logs all operations in `maya_cli.log`. Check this file for debugging and issue tracking.

## Contact
For support or feature requests, reach out to the development team via GitHub or email.