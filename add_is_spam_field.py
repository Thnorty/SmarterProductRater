import json
import joblib
from tqdm import tqdm

# Set up spam detection models
print("Loading spam detection model...")
folder_name = "is_spam_models"
# Load the model and vectorizer
spam_detection_model = joblib.load(f'{folder_name}/spam_model.joblib')
spam_detection_vectorizer = joblib.load(f'{folder_name}/spam_vectorizer.joblib')

def detect_spam(text):
    if text is None or text.strip() == "":
        return 0
    try:
        # Convert to a simple list representation
        text_vector = spam_detection_vectorizer.transform([text])
        prediction = int(spam_detection_model.predict(text_vector)[0])
        return prediction
    except Exception as e:
        # In case of errors, return 0 (not spam)
        print(f"Error in spam detection: {e}")
        return 0

# Input and output file paths
json_file = "appliances_with_sentiment_score.jsonl"
output_file = "appliances_with_sentiment_score_and_is_spam.jsonl"

# Process each line in the JSON file and add is_spam field
print(f"Processing {json_file}...")

# Read and process each line
with open(json_file, 'r', encoding='utf-8') as f_in, open(output_file, 'w', encoding='utf-8') as f_out:
    # Count lines for progress bar
    total_lines = sum(1 for _ in open(json_file, 'r', encoding='utf-8'))
    
    # Process each line with progress bar
    for line in tqdm(f_in, total=total_lines, desc="Processing reviews", mininterval=0, maxinterval=float('inf'), miniters=10000):
        try:
            # Parse the JSON line
            data = json.loads(line)
            
            # Extract text field (adjust the field name if needed)
            review_text = data.get("text", "")
            
            # Get spam detection result
            is_spam = detect_spam(review_text)
            
            # Add is_spam field to the data
            data["is_spam"] = is_spam
            
            # Write updated JSON line to the output file
            f_out.write(json.dumps(data, ensure_ascii=False) + '\n')
        except json.JSONDecodeError:
            print(f"Skipping invalid JSON line: {line.strip()}")
        except Exception as e:
            print(f"Error processing line: {e}")

print(f"Processing complete. Spam detection results added to {output_file}")