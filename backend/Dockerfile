# Build stage
FROM python:3.10-alpine AS build

# Copy the application code to the container
COPY . /app
WORKDIR /app

# Install the dependencies in a virtual environment
RUN apk add --no-cache build-base libffi-dev openssl-dev
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# Copy the entrypoint script and grant execute permission
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Run stage
FROM python:3.10-alpine

# Copy the virtual environment from the build stage
COPY --from=build /venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy the application code to the container
COPY --from=build /app /app
WORKDIR /app

# Expose the default Django port
EXPOSE 8000

# Start the Django development server
ENTRYPOINT ["/app/entrypoint.sh"]