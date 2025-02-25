from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from inspect import Signature
from typing import List, Optional

from .book_procedure_signature import BookProcedureSignature
from .concept_descriptor import ConceptDescriptor
from .example import Example
from .parameter_concept_bind import ParameterConceptBind


@dataclass
class BookProcedureDescriptor:
    id: str
    english_signature: BookProcedureSignature
    python_signature: Signature
    parameter_concept_map: List[ParameterConceptBind]
    examples: List[Example] = field(default_factory=list)
    filter_capable: bool = False
    page_capable: bool = False
    connection_required: bool = False
    override_connection_required: Optional[bool] = None
    outputs: Optional[List[ConceptDescriptor]] = None
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    filter_argument_position: Optional[int] = None
    offset_argument_position: Optional[int] = None
    limit_argument_position: Optional[int] = None

    @property
    def input_concepts(self) -> Optional[List[ConceptDescriptor]]:
        input_concepts = []

        for parameter_concept in self.parameter_concept_map:
            input_concepts.extend(parameter_concept.concepts)

        return input_concepts if len(input_concepts) != 0 else None

    @property
    def output_concepts(self) -> Optional[List[ConceptDescriptor]]:
        return self.outputs

    @property
    def filter_argument_name(self) -> Optional[str]:
        return self.argument_name(self.filter_argument_position)

    @property
    def offset_argument_name(self) -> Optional[str]:
        return self.argument_name(self.offset_argument_position)

    @property
    def limit_argument_name(self) -> Optional[str]:
        return self.argument_name(self.limit_argument_position)

    @property
    def filter_has_default(self) -> Optional[bool]:
        return self.has_default(self.filter_argument_position)

    @property
    def offset_has_default(self) -> Optional[bool]:
        return self.has_default(self.offset_argument_position)

    @property
    def limit_has_default(self) -> Optional[bool]:
        return self.has_default(self.limit_argument_position)

    def argument_name(self, pos: Optional[int]) -> Optional[str]:
        if pos is None:
            return None
        parameters = list(self.python_signature.parameters.keys())
        if len(parameters) > pos:
            return parameters[pos]
        return None

    def has_default(self, pos: Optional[int]) -> Optional[bool]:
        if pos is None:
            return None

        parameters = list(self.python_signature.parameters.values())

        if 0 <= pos < len(parameters):
            return parameters[pos].default is not inspect.Parameter.empty

        return None
