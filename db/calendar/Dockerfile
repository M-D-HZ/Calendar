# syntax=docker/dockerfile:1
FROM postgres:16.2-bookworm

# Set the working directory inside the container
WORKDIR /db/calendar

# Copy the SQL scripts to the working directory
COPY calendar.sql /docker-entrypoint-initdb.d/

# Command to run the SQL scripts
CMD ["postgres"]