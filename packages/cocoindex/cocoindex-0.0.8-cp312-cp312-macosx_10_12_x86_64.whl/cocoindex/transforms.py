"""All builtin transform ops."""
from collections.abc import Sequence
from typing import Annotated

import json
import sentence_transformers
from .typing import Float32, Vector, TypeAttr
from . import op

class ToMarkdown(op.TransformSpec):
    """Convert a blob to markdown."""

class SplitRecursively(op.TransformSpec):
    """Split a document (in string) recursively."""
    chunk_size: int
    chunk_overlap: int
    language: str | None = None

class SentenceTransformerEmbed(op.TransformSpec):
    """Run the sentence transformer"""
    model: str

@op.executor_class(gpu=True)
class SentenceTransformerEmbedExecutor:
    """Executor for SentenceTransformerEmbed."""

    spec: SentenceTransformerEmbed
    _model: sentence_transformers.SentenceTransformer

    def prepare(self, text = None):
        self._model = sentence_transformers.SentenceTransformer(self.spec.model, 3)
        dim = self._model.get_sentence_embedding_dimension()
        return Annotated[Sequence[Float32], Vector(dim=dim), TypeAttr("cocoindex.io/vector_origin_text", json.loads(text.analyzed_value))]

    def __call__(self, text: str) -> Sequence[Float32]:
        return self._model.encode(text).tolist()
