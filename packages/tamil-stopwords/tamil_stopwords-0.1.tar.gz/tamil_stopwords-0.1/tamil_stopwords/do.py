# Read from a comma-separated file and convert to line-separated format

input_file = "tamil_stopwords.txt"  # Input file with comma-separated stopwords
output_file = "tamil_stopwords_cleaned.txt"       # Output file with unique stopwords (one per line)

# Read the file and process the words
with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

# Split by comma, remove extra spaces, and remove duplicates
stopwords = set(word.strip() for word in content.split(","))  # Using a set to remove duplicates

# Write to a new file with one stopword per line
with open(output_file, "w", encoding="utf-8") as f:
    for word in sorted(stopwords):  # Sort for consistency
        f.write(word + "\n")

print(f"✅ Conversion complete! Stopwords saved to {output_file}")
