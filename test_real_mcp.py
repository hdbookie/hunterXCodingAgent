#!/usr/bin/env python3
"""
Quick test of real MCP connection to Supabase
"""

import os
import asyncio
from fastmcp_integration import AsyncMCPSupabaseAdapter

async def test_real_mcp():
    """Test real MCP operations with working integration."""

    print("🌊 Testing Real MCP Connection to Supabase")
    print("=" * 50)

    # Set the access token
    os.environ['SUPABASE_ACCESS_TOKEN'] = 'sbp_bf4a3adc3e90f80b70777eea873d3c95ab41d7ba'

    adapter = AsyncMCPSupabaseAdapter()

    try:
        # Test 1: Get project URL
        print("🔗 Getting project URL...")
        url_result = adapter.get_project_url()
        print(f"   URL: {url_result}")

        # Test 2: List tables
        print("\n📋 Listing database tables...")
        tables_result = adapter.list_tables()
        print(f"   Tables: {tables_result}")

        # Test 3: Get anonymous key
        print("\n🔑 Getting anonymous key...")
        key_result = adapter.get_anon_key()
        print(f"   Key: {key_result[:50]}..." if len(str(key_result)) > 50 else f"   Key: {key_result}")

        # Test 4: Security advisors
        print("\n🔒 Checking security advisors...")
        advisors_result = adapter.get_advisors()
        print(f"   Advisors: {str(advisors_result)[:100]}...")

        print("\n" + "=" * 50)
        print("✅ All MCP operations successful!")
        print("🎉 FastMCP → Supabase integration is fully operational!")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        adapter.close()

if __name__ == "__main__":
    asyncio.run(test_real_mcp())