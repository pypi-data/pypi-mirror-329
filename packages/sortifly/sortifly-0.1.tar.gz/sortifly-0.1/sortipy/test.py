import random
import time
import matplotlib.pyplot as plt
import numpy as np

def generate_dataset(size):
    """Genereer een willekeurige dataset van opgegeven grootte."""
    return [random.randint(0, 10000) for _ in range(size)]

def compare_sort_algorithms(sort_functions, dataset_sizes, save_location=None):
    """Vergelijk meerdere sorteeralgoritmes op basis van tijd voor verschillende datasetgroottes."""
    # Controleer de grenzen van de invoerparameters
    if len(sort_functions) > 10:
        raise ValueError("Maximaal 10 sorteeralgoritmes toegestaan.")
    if len(dataset_sizes) > 5:
        raise ValueError("Maximaal 5 datasetgroottes toegestaan.")
    
    # Lijst voor de resultaten van elke sorteerfunctie
    results = {func.__name__: [] for func in sort_functions}

    # Voor elke datasetgrootte, test de sorteeralgoritmes
    for size in dataset_sizes:
        print(f"Testen met dataset grootte: {size}")
        dataset = generate_dataset(size)

        for sort_function in sort_functions:
            duration = _test_sort_algorithm(sort_function, dataset_size=size, show_graph=False)  # Geen grafiek voor elke individuele test
            results[sort_function.__name__].append(duration)

    # Resultaten visualiseren in een grafiek
    _plot_comparison_graph(results, dataset_sizes, save_location)

def _test_sort_algorithm(sort_function, dataset_size, show_graph=False):
    """Test een sorteeralgoritme en geef de tijd op basis van de datasetgrootte."""
    # Genereer de dataset op basis van de dataset_size
    dataset = generate_dataset(dataset_size)

    start_time = time.time()

    # Sorteer de dataset met de meegegeven functie
    sorted_dataset = sort_function(dataset)

    end_time = time.time()
    duration = end_time - start_time

    print(f"{sort_function.__name__} duurde: {duration:.6f} seconden")

    if show_graph:
        # Grafiek tonen van de dataset voor en na het sorteren
        _plot_comparison(dataset, sorted_dataset)

    return duration

def _plot_comparison(original, sorted_data):
    """Toon een grafiek van de originele en gesorteerde dataset."""
    plt.figure(figsize=(10, 6))

    # Creëer een index voor de x-as
    x = np.arange(len(original))

    plt.subplot(1, 2, 1)
    plt.plot(x, original, label='Origineel')
    plt.title("Originele Dataset")
    
    plt.subplot(1, 2, 2)
    plt.plot(x, sorted_data, label='Gesorteerd', color='g')
    plt.title("Gesorteerde Dataset")

    plt.tight_layout()
    plt.show()

def _plot_comparison_graph(results, dataset_sizes, save_location):
    """Toon een grafiek van de vergelijkingen tussen verschillende algoritmes."""
    plt.figure(figsize=(10, 6))

    for algorithm, durations in results.items():
        plt.plot(dataset_sizes, durations, label=algorithm)

    plt.xlabel("Dataset Grootte")
    plt.ylabel("Tijd (seconden)")
    plt.title("Vergelijking van Sorteeralgoritmes")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Als save_location is gegeven, sla de afbeelding op
    if save_location:
        plt.savefig(save_location)
        print(f"Grafiek opgeslagen op: {save_location}")
    else:
        plt.show()

# Dit zorgt ervoor dat alleen de functie `compare_sort_algorithms` publiekelijk beschikbaar is
__all__ = ["compare_sort_algorithms"]