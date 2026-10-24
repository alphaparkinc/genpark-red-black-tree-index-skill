"""MCP Server for GenPark Red-Black Tree Index.
100% Python Standard Library.
"""

import json
import sys
from client import RedBlackTreeIndex

index = RedBlackTreeIndex()

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "insert_entry",
                        "description": "Insert or update a key-value entry in the Red-Black tree",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "key": {"type": "string"},
                                "value": {"type": "string"}
                            },
                            "required": ["key", "value"]
                        }
                    },
                    {
                        "name": "search_entry",
                        "description": "Search for a key in O(log N) time",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "key": {"type": "string"}
                            },
                            "required": ["key"]
                        }
                    },
                    {
                        "name": "range_query",
                        "description": "Execute an ordered range scan between min_key and max_key",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "min_key": {"type": "string"},
                                "max_key": {"type": "string"}
                            },
                            "required": ["min_key", "max_key"]
                        }
                    },
                    {
                        "name": "verify_invariants",
                        "description": "Verify Red-Black tree balancing and black height invariants",
                        "inputSchema": {"type": "object"}
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "insert_entry":
            k = args.get("key")
            v = args.get("value")
            index.insert(k, v)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": f"Inserted key: {k}"}]}
            }
        elif name == "search_entry":
            k = args.get("key")
            v = index.search(k)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps({"key": k, "value": v})}]}
            }
        elif name == "range_query":
            min_k = args.get("min_key")
            max_k = args.get("max_key")
            items = index.range_query(min_k, max_k)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(items, indent=2)}]}
            }
        elif name == "verify_invariants":
            inv = index.verify_invariants()
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(inv, indent=2)}]}
            }

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
