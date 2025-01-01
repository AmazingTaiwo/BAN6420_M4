# Import necessary libraries
import zipfile
import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import shutil

# Define paths
# Directory where the files will be extracted.
extracted_folder_path = 'Netflix_shows_movies/'
# Directory path for the files to be extracted.
zip_file_path = "netflix_data.zip"  # Path to the zip file.

# Check the existence of the target directory, if not, create it
if not os.path.exists(extracted_folder_path):
    os.makedirs(extracted_folder_path)

# Unzip the file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder_path)

print(f"Files extracted to {extracted_folder_path}")

# Rename the extracted file to 'Netflix_shows_movies.csv' (if needed)
extracted_files = os.listdir(extracted_folder_path)
for file in extracted_files:
    if file.endswith('.csv'):  # Assuming the file is a CSV
        os.rename(os.path.join(extracted_folder_path, file), os.path.join(extracted_folder_path, 'Netflix_shows_movies.csv'))

# List the files in the extracted folder to ensure it's done correctly
extracted_files = os.listdir(extracted_folder_path)
print(extracted_files)

# Load dataset (assuming a CSV format)
file_path = extracted_folder_path + 'Netflix_shows_movies.csv'  # Replace with the correct file name
df = pd.read_csv(file_path)

# Check for missing values
missing_data = df.isnull().sum()
print(f"Missing data:\n{missing_data}")

# Check the first few rows to ensure it's loaded correctly
print(df.head())

# Split the 'genre' column into individual genres
# Split by commas and explode the genres into individual rows
all_genres = df['listed_in'].str.split(',').explode().str.strip()  # Strip any extra spaces

# Count the occurrences of each genre
genre_counts = all_genres.value_counts()

# Print the updated DataFrame
print(df)
print(df.dtypes)

# Data Exploration
# Data Description
data_description = df.describe()  # Statistics for numerical columns Summary
print(data_description)

# Check available datatypes in the dataset
data_types = df.dtypes
print(f"Data types:\n{data_types}")

# Summarize categorical in listed_in column
print("\nUnique values in 'listed_in':")
print(df['listed_in'].value_counts())

# Summarize categorical in type column.
print("\nUnique values in 'type':")
print(df['type'].value_counts())

# Print ratings distribution and description.
print("\nRating distribution:")
print(df['rating'].describe())

# Data Cleansing for the 'listed_in' column
# Handle missing values and ensure it's of string type
df['listed_in'] = df['listed_in'].astype(str)

# Split 'listed_in' column by commas to create lists of genres
df['listed_in'] = df['listed_in'].str.split(',')  # Split genres/categories by comma

# Explode the 'listed_in' column to create a row for each genre
df_exploded = df.explode('listed_in')

# Clean up genre names by removing leading/trailing spaces and filter out empty genres
df_exploded['listed_in'] = df_exploded['listed_in'].str.strip()  # Remove spaces

# Step 4: Count the occurrences of each genre (listed_in)
genre_counts = df_exploded['listed_in'].value_counts()
print(genre_counts)

# Remove empty genre i.e listed_in
df_exploded = df_exploded[df_exploded['listed_in'] != '']

# Data Visualization using python libraries (Seaborn, pyplot and Matplotlib)
# Plot the most watched genres with listed_in column
plt.figure(figsize=(12, 8))
sns.barplot(x=genre_counts.index, y=genre_counts.values, palette='viridis')
plt.xticks(rotation=90)
plt.title("Most Watched Genres")
plt.xlabel("Genres")
plt.ylabel("Count")
plt.show()

# Convert 'rating' and 'listed_in' columns to numeric value.
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

# Plot for Distribution of Ratings with 'rating' column)
plt.figure(figsize=(8, 6))
sns.histplot(df['rating'], kde=True, color='blue', bins=30)
plt.title("Distribution of Ratings")
plt.xlabel("Ratings")
plt.ylabel("Frequency")
plt.show()

# Export or Save the most watched genres plot as an image.
plt.figure(figsize=(12, 8))
sns.barplot(x=genre_counts.index, y=genre_counts.values)
plt.xticks(rotation=90)
plt.title("Most Watched Genres")
plt.xlabel("Genres")
plt.ylabel("Count")
plt.savefig("most_watched_genres.png")

# Create a directory for saving all necessary files
output_dir = 'Netflix_analysis_output/'
os.makedirs(output_dir, exist_ok=True)

# Copy your Python scripts, visualizations, and dataset
shutil.copy("most_watched_genres.png", output_dir)

# Zip the output directory
shutil.make_archive('Netflix_analysis', 'zip', output_dir)