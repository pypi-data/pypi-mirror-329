from .algorithms import bubble_sort, insertion_sort, selection_sort, merge_sort, quick_sort
from .algorithms import heap_sort, counting_sort, radix_sort, bucket_sort, tim_sort
from .algorithms import shell_sort, cocktail_shaker_sort, pigeonhole_sort, gnome_sort
from .algorithms import bitonic_sort, pancake_sort, flash_sort

# Optioneel: Voeg versie-informatie toe
__version__ = "0.1.0"

# Je kunt ook een '__all__' toevoegen om te bepalen welke symbolen in deze module beschikbaar zijn
__all__ = [
    'bubble_sort', 'insertion_sort', 'selection_sort', 'merge_sort', 'quick_sort',
    'heap_sort', 'counting_sort', 'radix_sort', 'bucket_sort', 'tim_sort', 'shell_sort',
    'cocktail_shaker_sort', 'pigeonhole_sort', 'gnome_sort', 'bitonic_sort', 'pancake_sort', 'flash_sort', '__version__'
]
