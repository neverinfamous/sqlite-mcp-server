#!/usr/bin/env python3
"""
Test script for SQLite MCP Server HTTP version (Smithery deployment)
"""

import asyncio
import json
import aiohttp
import sys
from pathlib import Path

async def test_smithery_server():
    """Test the HTTP MCP server endpoints."""
    base_url = "http://localhost:8000"
    
    async with aiohttp.ClientSession() as session:
        # Test health endpoint
        print("🔍 Testing health endpoint...")
        try:
            async with session.get(f"{base_url}/health") as resp:
                if resp.status == 200:
                    health_data = await resp.json()
                    print(f"✅ Health check: {health_data}")
                else:
                    print(f"❌ Health check failed with status {resp.status}")
                    return False
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return False
        
        # Test MCP info endpoint (GET)
        print("\n🔍 Testing MCP info endpoint (GET)...")
        try:
            async with session.get(f"{base_url}/mcp") as resp:
                if resp.status == 200:
                    info_data = await resp.json()
                    print(f"✅ MCP info: {json.dumps(info_data, indent=2)}")
                else:
                    print(f"❌ MCP info failed with status {resp.status}")
        except Exception as e:
            print(f"❌ MCP info failed: {e}")
        
        # Test MCP initialize request
        print("\n🔍 Testing MCP initialize request...")
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        try:
            async with session.post(
                f"{base_url}/mcp",
                json=mcp_request,
                headers={"Content-Type": "application/json"}
            ) as resp:
                if resp.status == 200:
                    mcp_data = await resp.json()
                    print(f"✅ MCP initialize: {json.dumps(mcp_data, indent=2)}")
                else:
                    print(f"❌ MCP initialize failed with status {resp.status}")
        except Exception as e:
            print(f"❌ MCP initialize failed: {e}")

        # Test tools/list request
        print("\n🔍 Testing tools/list request...")
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        try:
            async with session.post(
                f"{base_url}/mcp",
                json=tools_request,
                headers={"Content-Type": "application/json"}
            ) as resp:
                if resp.status == 200:
                    tools_data = await resp.json()
                    tools_list = tools_data.get('result', {}).get('tools', [])
                    print(f"✅ Available tools ({len(tools_list)}):")
                    for tool in tools_list[:5]:  # Show first 5 tools
                        print(f"   - {tool['name']}: {tool['description']}")
                    if len(tools_list) > 5:
                        print(f"   ... and {len(tools_list) - 5} more tools")
                else:
                    print(f"❌ Tools list failed with status {resp.status}")
        except Exception as e:
            print(f"❌ Tools list failed: {e}")

        # Test resources/list request
        print("\n🔍 Testing resources/list request...")
        resources_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "resources/list",
            "params": {}
        }
        
        try:
            async with session.post(
                f"{base_url}/mcp",
                json=resources_request,
                headers={"Content-Type": "application/json"}
            ) as resp:
                if resp.status == 200:
                    resources_data = await resp.json()
                    resources_list = resources_data.get('result', {}).get('resources', [])
                    print(f"✅ Available resources ({len(resources_list)}):")
                    for resource in resources_list:
                        print(f"   - {resource['uri']}: {resource['description']}")
                else:
                    print(f"❌ Resources list failed with status {resp.status}")
        except Exception as e:
            print(f"❌ Resources list failed: {e}")

        # Test a simple tool call
        print("\n🔍 Testing tool call (list_tables)...")
        tool_call_request = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "list_tables",
                "arguments": {}
            }
        }
        
        try:
            async with session.post(
                f"{base_url}/mcp",
                json=tool_call_request,
                headers={"Content-Type": "application/json"}
            ) as resp:
                if resp.status == 200:
                    tool_data = await resp.json()
                    print(f"✅ Tool call result: {json.dumps(tool_data, indent=2)}")
                else:
                    print(f"❌ Tool call failed with status {resp.status}")
        except Exception as e:
            print(f"❌ Tool call failed: {e}")

        print("\n🎉 SQLite MCP Server HTTP testing completed!")
        return True


async def test_with_config():
    """Test server with configuration parameters."""
    print("\n🔧 Testing with configuration parameters...")
    
    # Test with custom configuration via query parameters
    config_url = "http://localhost:8000/mcp?dbPath=/app/data/test.db&logLevel=debug&enableFTS=true"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(config_url) as resp:
                if resp.status == 200:
                    print("✅ Configuration parameters handled successfully")
                else:
                    print(f"❌ Configuration test failed with status {resp.status}")
        except Exception as e:
            print(f"❌ Configuration test failed: {e}")


if __name__ == "__main__":
    print("🧪 Testing SQLite MCP Server (Smithery HTTP version)")
    print("📋 Make sure to start the server first with: python src/server_http.py")
    print("🔗 Or test the Smithery deployment directly")
    print()
    
    # Check if server is running
    async def check_server():
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("http://localhost:8000/health", timeout=aiohttp.ClientTimeout(total=5)) as resp:
                    return resp.status == 200
        except:
            return False
    
    if not asyncio.run(check_server()):
        print("⚠️  Server not detected on localhost:8000")
        print("   Start the server with: python src/server_http.py")
        print("   Or test against a deployed Smithery instance")
        print()
    
    success = asyncio.run(test_smithery_server())
    
    if success:
        asyncio.run(test_with_config())
    
    print("\n✨ Testing complete!")
    sys.exit(0 if success else 1)
