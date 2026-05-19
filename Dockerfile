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

# Expose MCP server port (not used for stdio, but kept for future HTTP support)
EXPOSE 3000

# Health check - verify Python and dependencies are working
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import mcp; import yfinance; import pandas" || exit 1

# Keep container alive - MCP server will be started by Bob via docker exec
# This is the correct approach for stdio-based MCP servers
CMD ["tail", "-f", "/dev/null"]

# Made with Bob
