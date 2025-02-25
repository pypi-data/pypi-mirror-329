from pygeai.core.embeddings.managers import EmbeddingsManager
from pygeai.core.embeddings.models import EmbeddingConfiguration

manager = EmbeddingsManager()

inputs = [
    "Help me with Globant Enterprise AI",
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAAEElEQVR4nGK6HcwNCAAA//8DTgE8HuxwEQAAAABJRU5ErkJggg=="
]


configuration = EmbeddingConfiguration(
    inputs=inputs,
    model="awsbedrock/amazon.titan-embed-image-v1",
    encoding_format=None,
    dimensions=None,
    user=None,
    input_type=None,
    timeout=600,
    cache=False
)

response = manager.generate_embeddings(configuration)
print(response)