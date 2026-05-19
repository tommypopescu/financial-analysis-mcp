# Financial Analysis MCP Server Starter Script
# This script connects to the OMV server and starts the MCP server via SSH

param(
    [string]$ServerIP = "192.168.1.7",
    [string]$Username = "root",
    [string]$ContainerName = "financial-analysis-mcp"
)

# SSH command to start MCP server
$sshCommand = "docker exec -i $ContainerName python -m src.server"

# Execute via SSH (requires SSH keys to be configured)
ssh "$Username@$ServerIP" $sshCommand

# Made with Bob
