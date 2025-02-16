
import json

with open("/Users/asuss/Desktop/PP2/lab4/sample-data.json") as file:
    data = json.load(file)

print("Interface Status")
print("=" * 82)
print(f"{'DN':<50} {'Description':<20} {'Speed':<8} {'MTU':<6}")
print("-" * 82)

for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]
    
    dn = attributes["dn"]
    description = attributes.get("descr", "")  
    speed = attributes["speed"]
    mtu = attributes["mtu"]

    print(f"{dn:<50} {description:<20} {speed:<8} {mtu:<6}")
