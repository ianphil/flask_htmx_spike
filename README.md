# Flask-HTMX Application

This is a simple web application built with Flask and HTMX that demonstrates GitHub OAuth authentication and basic user management.

## Features

- GitHub OAuth authentication
- User session management
- SQLite database integration with SQLAlchemy
- Dynamic content loading with HTMX
- User listing functionality

## Prerequisites

- Python 3.6+
- GitHub OAuth application credentials
- uv (Modern Python package installer and environment manager)

## Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd flask-htmx-spike
   ```

2. Install the required packages:
   ```
   uv sync
   ```

3. Create a `.env` file in the project root with the following variables:
   ```
   SECRET_KEY=your_secret_key_here
   GITHUB_CLIENT_ID=your_github_client_id
   GITHUB_CLIENT_SECRET=your_github_client_secret
   ```

   To obtain GitHub OAuth credentials:
   - Go to GitHub → Settings → Developer settings → OAuth Apps → New OAuth App
   - Set the Authorization callback URL to `http://localhost:5000/auth`

## Running the Application

Start the Flask development server:
```
uv run app.py
```

The application will be available at `http://localhost:5000`.

## Usage

- Visit the homepage at `http://localhost:5000/`
- Click "Log in" to authenticate with GitHub
- Once logged in, you can:
  - View dynamic content loaded with HTMX at `/update-section`
  - See all users in the database at `/users`
  - Log out using the logout button

## HTMX Integration

This application uses HTMX to update page content without full page reloads. The `update-section` endpoint demonstrates how to load partial HTML content dynamically.

## Database

The application uses SQLite with SQLAlchemy for user data storage. The database file will be created automatically as `users.db` when you first run the application.
