# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /backend/auth

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Make port 5003 available to the world outside this container
EXPOSE 5003

# Run app.py when the container launches
CMD ["python", "app.py"]