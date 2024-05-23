# Run.sh script

This repository contains a simple bash script to automate the process of pulling a Python container image and composing containers using Podman.

- Script Overview
    - The script performs the following tasks:

- Sets up signal trapping: Captures SIGINT and SIGTERM signals to exit gracefully.
    - Pulls a Python container image: Uses podman pull to fetch the python:3.12-rc-slim-buster image.
    - Composes containers: Uses podman compose up to start the container composition

# Event Management Application with Docker Compose

This project is a multi-service event management application, leveraging Docker Compose to orchestrate the various microservices and their respective databases.

## Table of Contents
- Services
- Volumes
- Networks
- Running the Project
- Shutting Down the Project
- Environment Variables
- Services

## Build and start all services:

- Start all services without rebuilding:

    - docker-compose up

- Stop all running services:

    - docker-compose down

- Stop and remove all volumes:

    - docker-compose down -v

## Environment Variables
A pre-made .env file will be provided. If you want to change these variables make sure to set the following environment variables in a .env file or in your environment before running the project:

- CALENDAR_DB_NAME
- DB_USER
- DB_PASSWORD
- CALENDAR_DB_HOST
- EVENTS_DB_NAME
- EVENTS_DB_HOST
- ENGAGEMENT_DB_NAME
- ENGAGEMENT_DB_HOST
- AUTH_DB_NAME
- AUTH_DB_HOST

These variables are used to configure the PostgreSQL databases for each service.


# Frontend
This is a simple Flask-based web application for managing events, user authentication, and engagement. The application allows users to log in, register, create events, view events, and manage event invites.

## Application Flow
Login/Register:

- Access the home page at '/':

    If not logged in, you will be redirected to the login page.
    Use the login form or navigate to the registration page to create a new account.

- View Events:

    - Once logged in, the home page will display a list of public events.
    - You can create new events using the form provided on the home page.

- Manage Calendar:

    - Access the calendar at /calendar to view your events.
    - Share your calendar with other users via the /share route.

- View and Respond to Invites:

    - Access your invites at /invites.
    - - Respond to invites directly from the invites page.

## Routes

- Home Page: /

    - Displays login page if not authenticated.
    - Displays list of public events if authenticated.
- Event Creation: /event (POST)

    - Creates a new event and sends invites.
- Calendar: /calendar (GET, POST)

    - Displays the calendar for the logged-in user or specified   - user.
- Share Calendar: /share (GET, POST)

    - Shares your calendar with another user.
- View Event: /event/<eventid> (GET)

    - Displays details for a specific event.
- Login: /login (POST)

    - Authenticates a user and starts a session.
- Register: /register (POST)

    - Registers a new user.
- View Invites: /invites (GET)

    - Displays invites for the logged-in user.
- Process Invite: /invites (POST)

    - Processes the response to an invite.
- Logout: /logout (GET)

    - Logs out the current user.

# Database Schema and Configuration

This repository contains the SQL scripts for creating the database schema and the PostgreSQL configuration file. Below is an overview of the database structure and the configuration settings.

## Database Schema
The database consists of four main tables and one custom type, which facilitate a basic calendar and event management system.

### Tables

- calendar

    - This table manages the relationship between two users in a calendar context.

- engagement
    - This table tracks the engagement status of users with events.

- events
    - This table stores information about events.

- users
    - This table manages user information.

## PostgreSQL Configuration
The PostgreSQL configuration file provided contains settings for various aspects of the PostgreSQL server. Here is a brief overview:

- Connection Settings: Includes parameters for listening addresses, ports, and connection limits.

- Authentication: Settings for authentication timeouts and password encryption methods.

- Resource Usage: Parameters for managing memory, disk usage, and kernel resources.

- Logging and Reporting: Configurations for logging destinations, log rotation, and log levels.

- Write-Ahead Logging (WAL): Settings for ensuring data integrity and recovery.

- Replication: Parameters for setting up replication between primary and standby servers.

- Query Tuning: Options for optimizing query performance.
For detailed descriptions and usage of each parameter, please refer to the official PostgreSQL documentation.

## Database Setup:

Run the SQL scripts to create the database schema.
Ensure PostgreSQL is properly configured and running.
Configuration:

Adjust the provided postgresql.conf file according to your environment and requirements.
Reload or restart the PostgreSQL server to apply the changes.
This setup forms a basic calendar and event management system with user authentication and event invitation tracking. Adjust the schema and configurations as needed to fit specific use cases and performance requirements.

# Backend

This repository contains the backend API for a calendar and event management system. It is built using FastAPI and follows a modular structure with separate routes for authentication, calendar sharing, engagements, events, and user management.

## Project Structure
- app.py: The main entry point for the FastAPI application.
- models/: Contains Pydantic models for request validation.
- routers/: Contains route handlers for different functionalities.
- wrappers/: Contains functions that interact with the database or perform core logic.

## API Endpoints
### Authentication
- Router: authrouter

    - POST /register: Register a new user.
    - POST /login: Login a user.

### Calendar Sharing
- Router: calendarRouter

    - POST /calendar: Share a calendar with another user.
    - GET /calendar: Get all calendars.
    - GET /calendar/{user}: Get shared calendars for a user.

### Engagements
- Router: engageRouter

    - POST /engage: Invite a user to an event.
    - GET /engage: Get all engagements.
    - GET /engage/{user}: Get engagements for a user.
    - PUT /engage: Update an engagement status.

### Events
- Router: eventsRouter

    - POST /events/create: Create a new event.
    - GET /events: Get all events.
    - GET /events/{event_id}: Get event details by ID.

### User Management
- Router: userRouter

    - GET /user/{username}: Get user details by username.
    - GET /user: Get all users.

## Error Handling

All endpoints return appropriate HTTP status codes and error messages when exceptions occur. The common status code used for exceptions is 404 Not Found.