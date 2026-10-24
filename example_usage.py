"""Example usage for GenPark Red-Black Tree Index.
100% Python Standard Library.
"""

from client import RedBlackTreeIndex

def main():
    tree = RedBlackTreeIndex()
    
    # Store timestamped telemetry records
    timestamps = [100, 250, 150, 300, 50, 200, 180, 400]
    for ts in timestamps:
        tree.insert(ts, f"telemetry_payload_at_{ts}")
        
    print("Tree Size:", tree.size)
    print("Invariants:", tree.verify_invariants())
    
    val = tree.search(200)
    print("Search ts=200:", val)
    
    # Range scan from 150 to 300
    results = tree.range_query(150, 300)
    print("Range Query [150, 300]:", results)

if __name__ == "__main__":
    main()
