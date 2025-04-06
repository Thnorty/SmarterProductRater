import json

input_path = "c:/Users/otota/Desktop/401Project/datas/appliances/meta_Appliances.jsonl"
output_path = "c:/Users/otota/Desktop/401Project/datas/appliances/meta_Appliances_cleaned.jsonl"

def convert_keys_to_lowercase(obj):
    if isinstance(obj, dict):
        return {k.lower().replace(' ', '_'): convert_keys_to_lowercase(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_keys_to_lowercase(item) for item in obj]
    return obj

with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
    for line in infile:
        try:
            # Parse the JSON object
            data = json.loads(line)
            
            # Convert all keys to lowercase with underscores
            data = convert_keys_to_lowercase(data)
                
            # Write the cleaned JSON object
            outfile.write(json.dumps(data) + '\n')
        except json.JSONDecodeError:
            print(f"Skipping invalid JSON line: {line[:50]}...")

print(f"Cleaned file saved to {output_path}")
