import argparse
import json
from palo_alto import palo_alto_save
from juniper import juniper_save
from checkpoint import checkpoint_save

def to_ip_lists(json_object):
    results = {
        "nonspoofed": {
            "all": [],
            "unknown": [],
            "malicious": [],
        },
        "spoofable": {
            "all": [],
            "unknown": [],
            "malicious": [],
        }
    }

    for entry in json_object:
        ip = entry.get("ip")
        if ip is None:
            continue

        target_bin = "spoofable" if entry.get("spoofable", True) else "nonspoofed"
        target_list = "malicious" if entry.get("classification") == "malicious" else "unknown"
        results[target_bin]["all"].append(ip)
        results[target_bin][target_list].append(ip)
    
    return results



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Turns Grey Noise JSON into Palo Alto IP-list")
    parser.add_argument("--enriched_file", default="/tmp/ukraine_enriched.json", 
                        help="Path to downloaded Grey Noise ukraine_enriched.json file", required=False)
    parser.add_argument("--enriched_spoofable_file", default="/tmp/spoofable_enriched.json", 
                        help="Path to downloaded Grey Noise spoofable_enriched.json file", required=False)
    args = parser.parse_args()

    handlers = [palo_alto_save, juniper_save, checkpoint_save]

    with open(args.enriched_file, "rt") as file:
        with open(args.enriched_spoofable_file, "rt") as spoofable_file:
            entries = json.loads(file.read())
            entries.extend(json.loads(spoofable_file.read()))
            lists = to_ip_lists(entries)
            for handler in handlers:
                handler(lists)