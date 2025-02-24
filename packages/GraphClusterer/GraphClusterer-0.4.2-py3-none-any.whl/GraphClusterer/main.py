import warnings

import pandas as pd
import pickle as pkl
import os
import json

from . import one_to_rule_them_all, calc_energy

warnings.filterwarnings("ignore")
WIKIPEDIA = ["apple", "car", "clock", "London", "turtle"]
REFAEL = ['3D printing', "additive manufacturing", "autonomous drones", "composite material", "hypersonic missile",
          "nuclear reactor", "quantum computing", "scramjet", "smart material", "wind tunnel"]
ALL_NAMES = WIKIPEDIA + REFAEL


def download_data():
    """
    Download the data (3D printing papers and graph) from the repository (github.com/yoelAshkenazi/GraphClusterer).
    :return:
    """
    print("Downloading the 3D printing dataset...")

    # make sure the data directory exists
    os.makedirs('data', exist_ok=True)

    vertices_url = ('https://raw.githubusercontent.com/yoelAshkenazi/GraphClusterer/master/data/graphs'
                    '/3D%20printing_papers.csv')
    edges_url = ('https://raw.githubusercontent.com/yoelAshkenazi/GraphClusterer/master/data/graphs'
                 '/3D%20printing_graph.csv')

    # vertices.
    df = pd.read_csv(vertices_url)
    df.to_csv('data/3D printing_papers.csv', index=False)

    # edges.
    df = pd.read_csv(edges_url)
    df.to_csv('data/3D printing_graph.csv', index=False)


def load_params(config_file_path=''):
    # If the path is wrong, configure a default config file.
    if not os.path.exists(config_file_path) or config_file_path == '':
        print(f"Config file not found at {config_file_path}. Making a default config file.")
        config_file_path = 'config.json'
        default_config_content = {
            "graph_kwargs": {
                "size": 2000,
                "K": 5,
                "color": "#1f78b4"
            },

            "clustering_kwargs": {
                "method": "louvain",
                "resolution": 0.5,
                "save": True
            },

            "draw_kwargs": {
                "save": True,
                "method": "louvain",
                "shown_percentage": 0.3
            },

            "name": "3D printing",  # Using 3d printing dataset by default.
            "vertices_path": "data/3D printing_papers.csv",  # vertices.
            "edges_path": "data/3D printing_graph.csv",  # edges.
            "distance_matrix_path": "",  # distances.

            "iteration_num": 2,
            "print_info": True,
            "allow_user_prompt": True
        }
        if 'cohere_key' not in default_config_content:
            key_ = input("Please enter your Cohere API key: ")
            default_config_content['cohere_key'] = key_

        if 'llama_key' not in default_config_content:
            key_ = input("Please enter your LLAMA API key: ")
            default_config_content['llama_key'] = key_

        with open(config_file_path, 'w') as _f:
            json.dump(default_config_content, _f)

        # Download the data from the repository (github.com/yoelAshkenazi/GraphClusterer).
        if not os.path.exists('data/3D printing_papers.csv'):
            download_data()  # Download the data.

        return default_config_content  # Return the default config file.

    with open(config_file_path, 'r') as _f:
        _params = json.load(_f)

    if 'cohere_key' not in _params:
        key_ = input("Please enter your Cohere API key: ")
        _params['cohere_key'] = key_

    if 'llama_key' not in _params:
        key_ = input("Please enter your LLAMA API key: ")
        _params['llama_key'] = key_

    return _params


def get_distance_matrix(path_, name_, lb=0.9, ub=5.0):
    if path_ == "" or not os.path.exists(path_):  # If the path is empty or wrong, create a new distance matrix.
        print("No distance matrix provided. Creating a distance matrix...")
        dists = calc_energy.compute_energy_distance_matrix(name_, lb, ub, 5)
        # Save the distance matrix to path.
        dir_name = 'data/distances'
        output_name = name_ + '_energy_distance_matrix.pkl'
        os.makedirs(dir_name, exist_ok=True)
        with open(dir_name + '/' + output_name, 'wb') as f:
            pkl.dump(dists, f)
        return dists
    with open(path_, 'rb') as f:  # Load the distances.
        distances_ = pkl.load(f)
    return distances_  # Return the distances.


def run_pipeline(config_path_=""):
    """
    Run the pipeline.
    :return:
    """
    config_path = config_path_

    params = load_params(config_path)

    # Set the parameters for the pipeline.
    pipeline_kwargs = {
        'graph_kwargs': params['graph_kwargs'],
        'clustering_kwargs': params['clustering_kwargs'],
        'draw_kwargs': params['draw_kwargs'],
        'print_info': params['print_info'],
        'iteration_num': params['iteration_num'],
        'vertices': pd.read_csv(params['vertices_path']),
        'edges': pd.read_csv(params['edges_path']) if params['edges_path'] != "" else None,
        'distance_matrix': get_distance_matrix(params['distance_matrix_path'], params['name'],
                                               params.get('lb', 0.9), params.get('ub', 5.0)),
        'name': params['name'],
        'cohere_key': params['cohere_key'],
        'llama_key': params['llama_key']
    }

    if params["allow_user_prompt"]:  # If the user prompt is allowed.
        user_aspects = input("Enter the aspects you want to focus on, separated by commas: ").split(",")
        pipeline_kwargs['aspects'] = user_aspects

    # Run the pipeline.
    print("Starting the pipeline...\n\n\n")
    one_to_rule_them_all.the_almighty_function(pipeline_kwargs)


if __name__ == '__main__':

    run_pipeline()
