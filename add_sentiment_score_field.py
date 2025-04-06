import json
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from tqdm import tqdm

# Set up device and models for sentiment analysis
print("Loading sentiment analysis model...")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
sentiment_analysis_model = "nlptown/bert-base-multilingual-uncased-sentiment"
sentiment_tokenizer = AutoTokenizer.from_pretrained(sentiment_analysis_model)
sentiment_model = AutoModelForSequenceClassification.from_pretrained(sentiment_analysis_model).to(device)

# Sentiment analysis function
def get_sentiment_score(text):
    if text is None or text.strip() == "":
        return 3  # Neutral score for empty text
    try:
        inputs = sentiment_tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        if device.type == "cuda":
            inputs = {k: v.to(device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = sentiment_model(**inputs)
        
        sentiment_score = torch.argmax(outputs.logits, dim=1).item() + 1
        return sentiment_score
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return 3  # Return neutral score in case of error

# Input and output file paths
json_file = "appliances.jsonl"
output_file = "appliances_with_sentiment_score.jsonl"

# Process each line in the JSON file and add sentiment scores
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
            
            # Extract text (adjust the field name if needed)
            review_text = data.get("text", "")
            
            # Get sentiment score for the rating text
            sentiment_score = get_sentiment_score(review_text)
            
            # Add sentiment score to the data
            data["sentiment_score"] = sentiment_score
            
            # Write updated JSON line to the output file
            f_out.write(json.dumps(data, ensure_ascii=False) + '\n')
        except json.JSONDecodeError:
            print(f"Skipping invalid JSON line: {line.strip()}")
        except Exception as e:
            print(f"Error processing line: {e}")

print(f"Processing complete. Sentiment scores added to {output_file}")
