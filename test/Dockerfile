# Stage 1: Install dependencies using uv
FROM python:3.11-slim as builder

WORKDIR /usr/src/app

# Install uv itself using pip. This is the recommended bootstrap method.
RUN pip install uv

# Copy project requirements
COPY ./requirements.txt ./

# Use uv to create wheel files for all dependencies, including the debugger.
# This command is much faster than the pip equivalent.
# We include debugpy and ptvsd here to ensure they are part of the final installation.
RUN uv pip install --system -r requirements.txt "ptvsd>=4.2" "debugpy>=1.6" \
    && rm -rf /root/.cache/uv

# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# The CMD remains exactly the same, as debugpy is now correctly installed in this stage.
CMD ["python", "-m", "debugpy", "--wait-for-client", "--listen", "0.0.0.0:5678", "main.py"]