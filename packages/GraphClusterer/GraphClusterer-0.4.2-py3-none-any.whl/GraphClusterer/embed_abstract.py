"""
Yuli Tshuva
"""

import pickle
import pandas as pd
import os
from sentence_transformers import SentenceTransformer
import warnings
warnings.filterwarnings("ignore")

# Load the model
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')


def make_embedding_file(name, source_path):
    """
    Create an embedding file for a given dataset.
    :param name:  Name of the dataset
    :param source_path:  Path to the dataset (the vertices.csv file)
    :return:
    """
    assert source_path is not None, "Source path is None. Please provide a valid path to the dataset."

    source_name = source_path.split('/')[-1].split('.')[0]

    # Read the data
    data = pd.read_csv(source_path)
    print(f"Creating embeddings for {name} dataset from '{source_path}'...")
    # Get abstracts
    abstracts, ids = list(data['abstract'].fillna("")), list(data['id'])
    print(f"Number of abstracts: {len(abstracts)}")
    # Split into sentences
    abstracts = [abstract.split('. ') for abstract in abstracts]
    # Set a dictionary to save the embeddings
    embeddings_dict = {}
    # Iterate through the abstracts and encode them
    for _id, abstract in zip(ids, abstracts):
        # Add back the '.' to the end of each sentence
        abstract = [sentence + '.' for sentence in abstract]
        # Encode the abstract
        embeddings = model.encode(abstract)
        # Save the embeddings
        embeddings_dict[_id] = embeddings
    # Save the embeddings
    print(f"Saving embeddings to 'data/embeddings/{source_name}_embeddings.pkl'...")
    try:
        with open(f"data/embeddings/{source_name}_embeddings.pkl", 'wb') as f:
            pickle.dump(embeddings_dict, f)
    except OSError:
        dir_ = 'data/embeddings'
        os.makedirs(dir_, exist_ok=True)
        with open(f"data/embeddings/{source_name}_embeddings.pkl", 'wb') as f:
            pickle.dump(embeddings_dict, f)

    return embeddings_dict  # Return the embeddings
