# Multi-stage build for optimized Docker image
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage - minimal runtime image
FROM python:3.11-slim

WORKDIR /app

# Copy Python packages from builder stage
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY src/ ./src/
COPY data/ ./data/

# Ensure scripts are in PATH
ENV PATH=/root/.local/bin:$PATH

# Create necessary directories
RUN mkdir -p /app/data /app/logs

# Expose MCP server port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import socket; s=socket.socket(); s.connect(('localhost', 3000)); s.close()" || exit 1

# Run the MCP server
CMD ["python", "-m", "src.server"]

# Made with Bob