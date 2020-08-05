from typing import List, Union, Any

import numpy as np
import transformers as trf

from whatlies.embedding import Embedding
from whatlies.embeddingset import EmbeddingSet


class HFTransformersLanguage:
    """
    This language class can be used to load Hugging Face Transformer models and use them to obtain
    representation of input string(s) as [Embedding][whatlies.embedding.Embedding] or
    [EmbeddingSet][whatlies.embeddingset.EmbeddingSet].

    Important:
        To use this language class, either of TensorFlow or PyTorch should be installed.

    Arguments:
        model_name_or_path: A string which is the name or identifier of a model from
            [Hugging Face model repository](https://huggingface.co/models), or is the path to a local directory
            which contains a pre-trained transformer model files.
        **kwargs: Additional key-value pair argument(s) which is passed to `transformers.pipeline` function.

    **Usage**:

    ```python
    > from whatlies.language import HFTransformersLanguage
    > lang = HFTransformersLanguage('bert-base-cased')
    > lang['today is a nice day']
    > lang = HFTransformersLanguage('gpt2')
    > lang[['day and night', 'it is as clear as day', 'today the sky is clear']]
    ```
    """

    def __init__(self, model_name_or_path: str, **kwargs: Any) -> None:
        self.model = trf.pipeline(
            task="feature-extraction", model=model_name_or_path, **kwargs
        )

    def __getitem__(self, query: Union[str, List[str]]):
        """
        Retreive a single embedding or a set of embeddings.

        Arguments:
            query: A single string or a list of strings

        Returns:
            An instance of [Embedding][whatlies.embedding.Embedding] (when `query` is a string)
            or [EmbeddingSet][whatlies.embeddingset.EmbeddingSet] (when `query` is a list of strings).
            The embedding vector is computed as the sum of hidden-state representaions of tokens
            (excluding special tokens, e.g. [CLS]).

        **Usage**

        ```python
        > from whatlies.language import HFTransformersLanguage
        > lang = HFTransformersLanguage('bert-base-cased')
        > lang['today is a nice day']
        > lang = HFTransformersLanguage('gpt2')
        > lang[['day and night', 'it is as clear as day', 'today the sky is clear']]
        ```
        """
        if isinstance(query, str):
            return self._get_embedding(query)
        return EmbeddingSet(*[self._get_embedding(q) for q in query])

    def _get_embedding(self, query: str):
        features = np.array(self.model(query, padding=False)[0])
        special_tokens_mask = self.model.tokenizer(
            query, return_special_tokens_mask=True, return_tensors="np"
        )["special_tokens_mask"][0]
        vec = features[np.logical_not(special_tokens_mask)].sum(axis=0)
        return Embedding(query, vec)
