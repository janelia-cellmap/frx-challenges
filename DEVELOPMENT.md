# Development Setup

This guide will help you set up the application for local development using podman-compose.

## Prerequisites

- Python 3.12+
- Podman and podman-compose installed
- Git

## Quick Start

### 1. Clone the repository

```bash
git clone <repository-url>
cd frx-challenges
```

### 2. Run the setup script

This script creates necessary directories, copies .env.example to .env, and checks that prerequisites are installed:

```bash
./setup-dev.sh
```

After running the script, review and update the `.env` file with your settings if needed.

### 3. Start the development environment

```bash
# Build and start the containers
podman-compose up --build

# Or run in detached mode
podman-compose up -d --build
```

The application will be available at http://localhost:8000

### 4. Run database migrations

In a new terminal, run:

```bash
podman-compose exec web python manage.py migrate
```

### 5. Create a superuser (optional)

```bash
podman-compose exec web python manage.py createsuperuser
```

### 6. Collect static files

```bash
podman-compose exec web python manage.py collectstatic --noinput
```

## Development Workflow

### Running management commands

```bash
podman-compose exec web python manage.py <command>
```

### Viewing logs

```bash
# All logs
podman-compose logs -f

# Web service logs only
podman-compose logs -f web
```

### Stopping the environment

```bash
podman-compose down
```

### Rebuilding after dependency changes

```bash
podman-compose down
podman-compose up --build
```

## Local Development without Containers

If you prefer to run Django directly on your machine:

### 1. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
pip install -r dev-requirements.txt
```

### 3. Run migrations

```bash
cd frx_challenges
python manage.py migrate
```

### 4. Start the development server

```bash
python manage.py runserver
```

**Note:** For the evaluation harness to work, you need podman running and accessible:

```bash
export DOCKER_HOST=unix:///run/podman/podman.sock
```

## Directory Structure

- `frx_challenges/` - Django project root
  - `frx_challenges/` - Django settings and configuration
  - `web/` - Main web application
  - `manage.py` - Django management script
- `harness/` - Evaluation harness
- `data/` - Created by podman-compose for persistent data
  - `db/` - SQLite database
  - `uploads/` - Submission uploads
  - `outputs/` - Evaluation results

## Troubleshooting

### Podman socket not found

Make sure the podman socket is running:

```bash
systemctl --user enable --now podman.socket
systemctl --user status podman.socket
```

On macOS, the podman machine needs to be running:

```bash
podman machine start
```

### Permission issues with volumes

If you encounter permission errors with mounted volumes, you may need to adjust the volume mounts in `docker-compose.yml` or run podman-compose with appropriate user mapping.

### Container cannot spawn evaluation containers

The web container needs access to the podman socket. Verify:
1. The socket path is correct in docker-compose.yml
2. The container has appropriate permissions (privileged mode is enabled)

## Configuration

### Authentication in Development

By default, the production application uses GitHub OAuth exclusively. In development mode (when `DEBUG = True`), the application automatically allows Django's built-in authentication:

- GitHub OAuth is disabled (`SOCIALACCOUNT_ONLY = False`)
- Standard Django login is available at `/admin/login/`
- You can create and use local superuser accounts
- No GitHub OAuth setup required for local development

This is configured in `frx_challenges/settings.py` lines 204-208.

### Overriding Settings

Application settings can be overridden using YAML configuration files thanks to `django-yamlconf`. Create a `config.yaml` file in the `frx_challenges/` directory to override any settings:

```yaml
SITE_NAME: "My Custom Challenge"
MAX_RUNNING_EVALUATIONS: 5
```
