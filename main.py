# Import necessary libraries
import zipfile
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import shutil

# Define paths
zip_file_path = "netflix_data.zip"  # Path to the zip file
unzip_dir = 'Netflix_shows_movies'  # Directory where the files will be extracted
renamed_file = ['Netflix_shows_movies/netflix_data.csv', 'Netflix_shows_movies/Netflix_shows_movies.csv']  # Files to rename

# Step 1: Check if the target directory exists, if not, create it
if not os.path.exists(unzip_dir):
    os.makedirs(unzip_dir)

# Step 2: Unzip the file
try:
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(unzip_dir)
    print(f"Files extracted to {unzip_dir}")
except FileNotFoundError:
    print(f"Error: The file '{zip_file_path}' does not exist.")
except zipfile.BadZipFile:
    print(f"Error: The file '{zip_file_path}' is not a valid zip file.")
except Exception as e:
    print(f"An error occurred: {e}")

# Step 3: Check if the files are extracted and rename them if necessary
for original, renamed in zip(renamed_file, renamed_file[1:]):
    try:
        # Renaming extracted file
        os.rename(original, renamed)
        print(f"Renamed file from {original} to {renamed}")
    except FileNotFoundError:
        print(f"Error: File {original} not found to rename.")
    except Exception as e:
        print(f"An error occurred while renaming: {e}")

# Unzip the dataset
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder_path)

# List the files in the extracted folder to ensure it's done correctly
extracted_files = os.listdir(extracted_folder_path)
print(extracted_files)

# Load dataset (assuming a CSV format)
file_path = extracted_folder_path + 'Netflix_shows_movies.csv'  # Replace with the correct file name
df = pd.read_csv(file_path)

# Check for missing values
missing_data = df.isnull().sum()
print(f"Missing data:\n{missing_data}")

# Fill missing values (this is one possible approach)
# You can use mean, median, or mode, depending on the column type
df.fillna(df.mean(), inplace=True)  # For numerical columns
df.fillna(df.mode().iloc[0], inplace=True)  # For categorical columns

# Alternatively, you can drop rows or columns with too many missing values
# df.dropna(inplace=True)

# Data Description
data_description = df.describe()  # Summary statistics for numerical columns
print(data_description)

# Checking the datatypes
data_types = df.dtypes
print(f"Data types:\n{data_types}")

# Check correlation between numeric features
correlation = df.corr()
print(f"Correlation matrix:\n{correlation}")

# Most Watched Genres (Assuming the dataset has a 'genre' column)
genre_counts = df['genre'].value_counts()

# Plot the most watched genres
plt.figure(figsize=(10, 6))
sns.barplot(x=genre_counts.index, y=genre_counts.values)
plt.xticks(rotation=90)
plt.title("Most Watched Genres")
plt.xlabel("Genres")
plt.ylabel("Count")
plt.show()

# 2. Distribution of Ratings (Assuming there's a 'rating' column)
plt.figure(figsize=(8, 6))
sns.histplot(df['rating'], kde=True, color='blue', bins=30)
plt.title("Distribution of Ratings")
plt.xlabel("Ratings")
plt.ylabel("Frequency")
plt.show()

# Save the most watched genres plot as an image
plt.figure(figsize=(10, 6))
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


# Write the README file
with open(output_dir + 'README.txt', 'w') as file:
    file.write(readme_content)

# Zip the output directory
shutil.make_archive('Netflix_analysis', 'zip', output_dir)

