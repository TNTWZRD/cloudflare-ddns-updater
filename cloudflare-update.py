import requests
import sys
import json

## Load Pertinate Files
Secret = json.load(open("secret.json"))
ZoneList = json.load(open("zonelist.json"))

# Create Headers
headers = {'content-type': 'application/json', 'Authorization': 'Bearer '+Secret["DNSAPI-TOKEN"]}

# ## Get IP
IP = requests.get("https://api.ipify.org").text

## Make Sure we have a valid IP
if IP == "":
    sys.exit("No Public IP cant update!")
else:
    print("Public IP Found: "+IP)

## Create dictionary to fill with records that need updating
toUpdate = []

## Loop through each zone, and each domain in that zone to see if they need updating
for ZoneIdentifier in ZoneList:
    for RecordName in ZoneList[ZoneIdentifier]:
        print("Checking " + ZoneIdentifier + " : " + RecordName)
        record = requests.get("https://api.cloudflare.com/client/v4/zones/"+ZoneIdentifier+"/dns_records?name="+RecordName, headers=headers).json()
        if "error" not in record:
            if(record["result_info"]["count"] == 0):
                print(ZoneIdentifier + " : " + RecordName + " || Invalid Record, Check spelling or create record")
                break
            for result in record["result"]:
                if(result["type"] != "A"): break
                if(result["content"] != IP):
                    toUpdate.append({"ZoneID": result["zone_id"], "RecordID": result["id"], "Proxy": result["proxied"], "RecordName": result["name"]})
        else:
            print(ZoneIdentifier + " : " + RecordName + " || Invalid Record, Check spelling or create record")
            print(record)

## Exit if all records are current
if(len(toUpdate) == 0): sys.exit("All records current, No updating required!")

# Update Records with new IP
for record in toUpdate:
    data = {"type":"A","name":record["RecordName"],"content":IP,"ttl":1,"proxied":record["Proxy"]}
    update = requests.put("https://api.cloudflare.com/client/v4/zones/" + record["ZoneID"] + "/dns_records/" + record["RecordID"], data = json.dumps(data), headers=headers).json()
    if(update["success"]): print("Updated "+record["RecordName"]+" With new IP: "+ IP)
    else: print("ERROR: " + update)
