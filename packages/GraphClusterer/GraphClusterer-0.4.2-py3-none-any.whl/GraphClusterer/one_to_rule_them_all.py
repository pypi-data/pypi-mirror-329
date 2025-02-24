from . import functions, evaluate, summarize, plot
from . import starry_graph as sg
import warnings
import os
import json
import cohere
import replicate
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


warnings.filterwarnings("ignore")

"""
Make an LLM provider class that inputs a model and key, and outputs an object that can be used to generate summaries.
(create a client object behind scenes).
"""


class LLMProvider:
    def __init__(self, model: str, key: str = None):
        """
        Initialize the LLM provider.
        :param model:  The model to use (str, either 'cohere' or 'replicate').
        :param key:  The API key for the model.
        """

        assert 'command-r' in model or 'llama' in model, ("Model must be either 'cohere' or 'replicate' "
                                                          "if you use the default class!")

        assert key is not None, "Key must be provided."
        if 'command-r' in model:
            self.client = cohere.Client(key)
        elif 'llama' in model:
            self.client = replicate.Client(key)

        self.model_name = model
        self.key = key

    def generate_response(self, prompt, max_tokens):
        """
        Generate a response for the given prompt.
        :param prompt:  The prompt to generate the response for.
        :param max_tokens:  The maximum number of tokens to generate.
        :return:
        """
        response = None  # Initialize the response.

        match self.model_name:
            case 'command-r-plus-08-2024':  # Use the Cohere model.
                response = self.client.generate(model=self.model_name,
                                                prompt=prompt, max_tokens=max_tokens)
                response = response.generations[0].text.strip()

            case 'meta/meta-llama-3.1-405b-instruct':  # Use the Replicate model.
                response = self.client.run(self.model_name, input={"prompt": prompt, "max_tokens": max_tokens})
                response = "".join(response)

        return response

    def reconnect(self):
        """
        Reconnect to the LLM provider.
        """
        if 'command-r' in self.model_name:
            self.client = cohere.Client(self.key)
        elif 'llama' in self.model_name:
            self.client = replicate.Client(self.key)


def run_graph_part(_name: str, _graph_kwargs: dict, _clustering_kwargs: dict, _draw_kwargs: dict,
                   _print_info: bool = False, _vertices=None, _edges=None, _distance_matrix=None):
    """
    Run the pipeline for the given name, graph_kwargs, kwargs, and draw_kwargs.
    :param _edges:  the edges of the graph.
    :param _vertices:  the vertices of the graph.
    :param _distance_matrix: the distance matrix for the embeddings.
    :param _print_info: whether to print the outputs.
    :param _name: the name of the embeddings file.
    :param _graph_kwargs: the parameters for the graph.
    :param _clustering_kwargs: the parameters for the clustering.
    :param _draw_kwargs: the parameters for the drawing.
    :return:
    """

    # create the graph.
    _G = functions.make_graph(_vertices, _edges, _distance_matrix, **_graph_kwargs)
    if _print_info:
        print(f"Graph created for '{_name}': {_G}")  # print the graph info.

    # cluster the graph.
    clusters, _G = functions.cluster_graph(_G, _name, **_clustering_kwargs)
    """
    # draw the graph.
    if wikipedia:
        # functions.draw_wiki_graph(_G, _name, **_draw_kwargs)
        functions.draw_wiki_graph(_G, _name, **_draw_kwargs)
    else:
        functions.draw_graph(_G, _name, **_draw_kwargs)
    """

    # print the results.
    if _print_info:
        print(f"{_draw_kwargs['method'].capitalize()} got {len(clusters)} "
              f"clusters for '{_name}' graph, with resolution coefficient of "
              f"{_clustering_kwargs['resolution']}.\n"
              f"Drew {int(_draw_kwargs['shown_percentage'] * 100)}% of the original graph.\n")

    return _G


def create_graph(_name, _graph_kwargs_: dict, _clustering_kwargs_: dict, _draw_kwargs_: dict, _vertices, _edges,
                 _distance_matrix=None):
    """
    Create the graph.
    :param _name:  the name of the graph.
    :param _edges:  the edges of the graph.
    :param _vertices:  the vertices of the graph.
    :param _distance_matrix: the distance matrix for the embeddings.
    :param _graph_kwargs_: the parameters for the graph.
    :param _clustering_kwargs_: the parameters for the clustering.
    :param _draw_kwargs_: the parameters for the drawing.
    :return:
    """

    _G = run_graph_part(_name, _graph_kwargs_, _clustering_kwargs_, _draw_kwargs_, False,
                        _vertices, _edges, _distance_matrix)

    return _G


def run_summarization(_name: str, _vertices, aspects, _print_info, cohere_key_, llama_key_) -> object:
    """
    Run the summarization for the given name and summarize_kwargs.
    :param _name: the name of the dataset.
    :param _vertices: the vertices of the graph.
    :param aspects: the aspects to focus on.
    :param _print_info: whether to print the outputs.
    :param cohere_key_: the coherence key for the summaries.
    :param llama_key_: the llama key for the summaries.
    :return:
    """
    # load the graph.
    _G = summarize.load_graph(_name)
    # filter the graph by colors.
    _subgraphs = summarize.filter_by_colors(_G, _print_info)
    # summarize each cluster.
    titles = summarize.summarize_per_color(_subgraphs, _name, _vertices, aspects, _print_info, cohere_key_, llama_key_)
    return titles


def plot_bar(name: str, metrics_dict: dict):
    """
    Create and save a bar plot for the given metrics of a specific name and version.

    :param name: the name of the dataset.
    :param metrics_dict: Dictionary containing metrics the dataset.
    :return:
    """
    # Retrieve metrics for the specific name and version
    values = [
        metrics_dict['avg_index'],
        metrics_dict['largest_cluster_percentage'],
        metrics_dict['avg_relevancy'],
        metrics_dict['avg_coherence'],
        metrics_dict['avg_consistency'],
        metrics_dict['avg_fluency'],
        metrics_dict['success_rates']
    ]

    # Define the labels for the x-axis
    x_labels = [
        "Average\nIndex",
        "Largest\nCluster\nPercentage",
        "Average\nRelevancy",
        "Average\nCoherence",
        "Average\nConsistency",
        "Average\nFluency",
        "Success\nRate"
    ]

    # Define colors for each bar
    colors = [
        'red',  # Average Index
        'red',  # Largest Cluster Percentage
        'blue',  # Average Relevancy
        'blue',  # Average Coherence
        'blue',  # Average Consistency
        'blue',  # Average Fluency
        'orange'  # Success Rate
    ]
    if values[0] is None:  # If the avg_index is None, remove it from the plot
        values = values[1:]
        x_labels = x_labels[1:]
        colors = colors[1:]

    # Create the bar plot
    plt.figure(figsize=(10, 6))
    bars = plt.bar(x_labels, values, color=colors, edgecolor='black')

    # Set y-axis limits and labels
    plt.ylim(0, 1.1)
    plt.xlabel("Evaluation Metrics", fontsize=14)
    plt.ylabel("Score", fontsize=14)
    plt.title(f"Results for '{name}' Graph", fontsize=16, fontweight='bold')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Display the value above each bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            yval + 0.01,
            f"{yval:.2f}",
            ha='center', va='bottom', fontsize=12, fontweight='bold'
        )

    # Create custom legend
    legend_elements = [
        Patch(facecolor='red', edgecolor='black', label='Cluster Analysis'),
        Patch(facecolor='blue', edgecolor='black', label='Text Analysis'),
        Patch(facecolor='orange', edgecolor='black', label='Connection to Origin')
    ]

    # Position the legend on the left
    plt.legend(handles=legend_elements, fontsize=12, loc='upper left', bbox_to_anchor=(0, 1))

    # Adjust layout to make room for the legend on the left
    plt.tight_layout()  # Adjust the left margin

    # Define the folder path and file path
    full_path = f"Results/plots/"

    # Create the plots folder if it doesn't exist
    os.makedirs(full_path, exist_ok=True)

    full_path += f"{name}.png"

    # Save the plot
    try:
        plt.savefig(full_path)
        print(f"Plot saved at: {full_path}")
    except Exception as e:
        print(f"Error saving the plot: {e}")

    plt.show()  # Show the plot after saving
    plt.close()  # Clear the figure to free memory


def the_almighty_function(pipeline_kwargs: dict, summary_model=None, refinement_model=None):
    """
    Run the pipeline for the given parameters.
    The pipeline has the following steps:
    1. Create the graph. (either with embeddings or without)
    2. Cluster the graph.
    3. Summarize the clusters.
    4. Evaluate the success rate.
    5. Iteratively repeat steps 1-4.
    6. Plot the results and make the html component.

    The plot is then saved at 'Results/plots' folder, the summaries are saved at 'Results/summaries' folder,
    and the html component is saved at 'Results/html' folder.

    Both 'summary_model' (cohere) and 'refinement_model' (llama) can be either None
    (in this case we use the LLM_provided class with the respective model name and key), or a class object with a
    'generate_response' method that accepts a prompt and max tokens ass input.
    :param pipeline_kwargs:  The full pipeline parameters.
    :param summary_model:  The model to use for the summaries. (using a default provider if not provided)
    :param refinement_model:  The model to use for the refinement. (using a default provider if not provided)
    :return:
    """

    # Unpack the pipeline parameters
    graph_kwargs = pipeline_kwargs.get('graph_kwargs', {
        "size": 2000,
        "K": 5,
        "color": "#1f78b4"
    })
    clustering_kwargs = pipeline_kwargs.get('clustering_kwargs', {
        "method": "louvain",
        "resolution": 0.5,
        "save": True
    })
    """draw_kwargs = pipeline_kwargs.get('draw_kwargs', {
        "save": True,
        "method": "louvain",
        "shown_percentage": 0.3
    })"""
    print_info = pipeline_kwargs.get('print_info', False)
    iteration_num = pipeline_kwargs.get('iteration_num', 1)  # default is 1
    vertices = pipeline_kwargs.get('vertices', None)
    edges = pipeline_kwargs.get('edges', None)
    name = pipeline_kwargs.get('name', "")
    distance_matrix = pipeline_kwargs.get('distance_matrix', None)
    aspects = pipeline_kwargs.get('aspects', None)  # expecting a list of aspects

    if summary_model is None:
        summary_model = LLMProvider(pipeline_kwargs.get('summary_model_name', 'command-r-plus-08-2024'),
                                    pipeline_kwargs.get('cohere_key', None))
    if refinement_model is None:
        refinement_model = LLMProvider(pipeline_kwargs.get('refinement_model_name',
                                                           'meta/meta-llama-3.1-405b-instruct'),
                                       pipeline_kwargs.get('llama_key', None))

    assert vertices is not None, "Vertices must be provided."

    # Create the graph.
    G = functions.make_graph(vertices, edges, distance_matrix, **graph_kwargs)

    # Set default value to rel, coh, con, flu, sr.
    rel, coh, con, flu, sr = 0, 0, 0, 0, 0

    # Iteratively repeat the followings:
    """
    1. Cluster the graph.
    2. Summarize the clusters.
    3. Evaluate the success rate.
    4. Update the edges using STAR graph.
    """
    kill_switch = False  # Kill switch to stop the iterations if the success rate is 1.
    for i in range(iteration_num):
        if print_info:
            print(f"Starting iteration {i + 1}...")
            print(f"Clustering the graph for '{name}'...")
        # Cluster the graph.
        functions.cluster_graph(G, name, **clustering_kwargs)

        if print_info:
            print(50 * "-")
            print(f"Summarizing the clusters for '{name}'...")
        # Summarize the clusters.
        run_summarization(name, vertices, aspects, print_info, summary_model, refinement_model)

        G = functions.load_graph(name)  # Load the graph

        # Evaluate the success rate and create the STAR graph
        if print_info:
            print(50 * "-")
            print(f"Evaluating the success rate for '{name}'...")
        sr = sg.starr(name, vertices, G, summary_model)

        # Check if the kill switch is activated
        if sr == -1:
            kill_switch = True
            break  # Should already have a fully summarized graph.

        if print_info:
            print(f"Success rate for '{name}' in iteration {i + 1}: {sr:.4f}")
            print(50 * "-")
            print(f"Updating the edges using STAR graph for '{name}'...")

        # Update the edges.
        G = sg.update(name, G)
        if print_info:
            print("Edges updated using STAR graph.")
            print(50 * "-")

    # Load the graph
    G = functions.load_graph(name)

    # Evaluate and plot the metrics
    cluster_scores = functions.evaluate_clusters(name, distance_matrix)  # Evaluate the clusters

    # Improve the summaries iteratively
    for iter_ in range(iteration_num):
        rel, coh, con, flu, scores = evaluate.metrics_evaluations(name, vertices, G, summary_model)
        if print_info:
            print(f"Metrics for '{name}' in iteration {iter_ + 1}:")
            print(f"Relevancy: {rel:.2f}, Coherence: {coh:.2f}, Consistency: {con:.2f}, Fluency: {flu:.2f}")
            print(50 * "-" if iter_ < iteration_num - 1 else "")
        if kill_switch:
            break
        summarize.improve_summaries(name, vertices, scores, summary_model, refinement_model)

    # Update the metrics dictionary

    # Check if the avg_index exists (i.e. we have more than one value to unpack in cluster_scores)
    if isinstance(cluster_scores, tuple):
        avg_index, largest_cluster_percentage = cluster_scores
    else:
        avg_index = None
        largest_cluster_percentage = cluster_scores

    # Update the metrics dictionary
    metrics_dict = {
        'avg_index': avg_index,
        'largest_cluster_percentage': largest_cluster_percentage,
        'avg_relevancy': rel,
        'avg_coherence': coh,
        'avg_consistency': con,
        'avg_fluency': flu,
        'success_rates': sr
    }

    # Update the JSON file with the new metrics
    try:
        known_metrics = json.load(open("metrics.json", "r"))
    except FileNotFoundError:
        known_metrics = {
            "avg_index": {},
            "largest_cluster_percentage": {},
            "avg_relevancy": {},
            "avg_coherence": {},
            "avg_consistency": {},
            "avg_fluency": {},
            "success_rates": {}
        }
    known_metrics["avg_index"][name] = avg_index
    known_metrics["largest_cluster_percentage"][name] = largest_cluster_percentage
    known_metrics["avg_relevancy"][name] = rel
    known_metrics["avg_coherence"][name] = coh
    known_metrics["avg_consistency"][name] = con
    known_metrics["avg_fluency"][name] = flu
    known_metrics["success_rates"][name] = sr

    with open("metrics.json", "w") as f:  # Save the updated metrics
        json.dump(known_metrics, f, indent=4)

    # Plot the metrics for the current dataset
    plot_bar(name, metrics_dict)

    # Create the html component.
    plot.plot(name, vertices)
