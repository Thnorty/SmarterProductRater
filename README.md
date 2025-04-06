# Smarter Product Rater

## Overview

This project enhances product rating systems for online shopping websites by implementing a weighted rating algorithm. It assigns importance weights to user reviews based on several criteria, ensuring that informative reviews have more impact on the overall product rating than non-informative ones.

## Weighting Criteria

Reviews are weighted based on:

- **Verified Purchase**: Weight multiplied by 1.5 for verified purchases
- **Images**: Weight multiplied by 2 for reviews with images
- **Text Content**: Weight multiplied by 2 for reviews with text
- **Spam Detection**: Weight multiplied by 0.4 for detected spam
- **Sentiment Mismatch**: Weight adjusted when actual rating differs from AI-predicted sentiment

## Models Used

- **Spam Detection**: Logistic regression model trained on YouTube Comments Spam Dataset
- **Sentiment Analysis**: BERT multilingual sentiment model (nlptown/bert-base-multilingual-uncased-sentiment)

## Dataset

The project uses Amazon Reviews Dataset, storing processed data in Hadoop Distributed File System (HDFS) in Parquet format.

## Project Files

- **create_spam_detection_model.py**: Trains logistic regression model for spam detection
- **add_is_spam_field.py**: Applies spam detection to each review
- **add_sentiment_score_field.py**: Processes reviews using BERT sentiment model
- **fix_jsonl.py**: Cleans and validates JSONL data format
- **upload_to_hdfs.py**: Converts data to Parquet format and uploads to HDFS
- **main.ipynb**: Main analysis notebook for weighting algorithm and visualizations

## Results

Our weighted rating system generally assigns lower ratings compared to Amazon's native system, especially for mid-range products. The approach tends to punish bad products and reward good products more significantly than Amazon's rating system.

## Contributors

- Oğuz Nurlu (211101069)
- Mete Gülsoy (211101040)
