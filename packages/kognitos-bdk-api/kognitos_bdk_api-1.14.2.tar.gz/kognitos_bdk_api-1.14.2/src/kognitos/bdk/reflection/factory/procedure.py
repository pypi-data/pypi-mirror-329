from __future__ import annotations

import inspect
from inspect import Signature
from types import NoneType
from typing import List, Optional, Tuple, Union

from ...api import FilterExpression, NounPhrase
from ...docstring import Docstring
from ...errors import SignatureError
from ..book_procedure_descriptor import BookProcedureDescriptor
from ..book_procedure_signature import BookProcedureSignature
from ..concept_descriptor import ConceptDescriptor
from ..example import Example
from ..factory.parameter_concept import ParameterConceptFactory
from ..parameter_concept_bind import ParameterConceptBind
from .concept import ConceptFactory


def noun_phrase_to_parameter(noun_phrase: NounPhrase) -> str:
    name = noun_phrase.modifiers.copy() if noun_phrase.modifiers else []
    name.append(noun_phrase.head)

    return "_".join(name)


def find_noun_phrase_path(target_or_object: Optional[List[NounPhrase]], noun_phrases: List[NounPhrase]) -> Optional[List[NounPhrase]]:
    if not target_or_object:
        return None

    len_target_or_object = len(target_or_object)
    len_noun_phrases = len(noun_phrases)

    for start in range(len_target_or_object - len_noun_phrases + 1):
        if target_or_object[start : start + len_noun_phrases] == noun_phrases:
            return target_or_object[: start + len_noun_phrases]

    return None


class BookProcedureFactory:
    @classmethod
    def create(
        cls, identifier: str, english_signature: BookProcedureSignature, python_signature: Signature, docstring: Docstring, override_connection_required: bool
    ) -> BookProcedureDescriptor:
        # by default no procedure is filter enabled
        filter_capable = False
        filter_argument_position: Optional[int] = None

        # by default no procedure is page enabled
        page_capable = False
        offset_argument_position: Optional[int] = None
        limit_argument_position: Optional[int] = None

        # parameter concept map
        pcm: List[ParameterConceptBind] = []

        # add mapping for each part of speech
        for pos in ("object", "target"):
            english_pos: Optional[List[NounPhrase]] = getattr(english_signature, pos, None)
            if english_pos:
                python_pos_parameter = python_signature.parameters.get(pos)
                if python_pos_parameter:
                    parameter_pos_annotation = getattr(
                        python_pos_parameter.annotation,
                        "__origin__",
                        python_pos_parameter.annotation,
                    )
                    if parameter_pos_annotation and issubclass(parameter_pos_annotation, Tuple):
                        concepts = [
                            ConceptFactory.from_noun_phrase_and_annotation(
                                noun_phrase, python_pos_parameter.annotation.__args__[idx], description=docstring.input_description_by_noun_phrases([noun_phrase])
                            )
                            for idx, noun_phrase in enumerate(english_pos)
                        ]

                        pcm.append(ParameterConceptFactory.from_parameter(python_pos_parameter, concepts=concepts, description=docstring.param_description_by_name(pos)))
                    else:
                        pos_noun_phrase = NounPhrase(head=pos, modifiers=[])
                        concept = ConceptFactory.from_noun_phrase_and_annotation(pos_noun_phrase, python_pos_parameter.annotation)
                        for noun_phrases in [[pos_noun_phrase], english_pos]:
                            if noun_phrases:
                                concept.description = docstring.input_description_by_noun_phrases(noun_phrases)
                                if concept.description:
                                    break

                        pcm.append(ParameterConceptFactory.from_parameter(python_pos_parameter, concepts=[concept], description=docstring.param_description_by_name(pos)))

        # add mapping for any remaining input parameter
        for idx, p in enumerate(python_signature.parameters.items()):
            _, parameter = p

            if parameter.name == "self":
                continue

            if parameter.annotation == FilterExpression or (
                hasattr(parameter.annotation, "__origin__")
                and parameter.annotation.__origin__ == Union
                and len(parameter.annotation.__args__) == 2
                and parameter.annotation.__args__[0] == FilterExpression
                and parameter.annotation.__args__[1] == NoneType
            ):
                filter_argument_position = idx
                filter_capable = True
                continue

            if parameter.annotation == int or (
                hasattr(parameter.annotation, "__origin__")
                and parameter.annotation.__origin__ == Union
                and len(parameter.annotation.__args__) == 2
                and parameter.annotation.__args__[0] == int
                and parameter.annotation.__args__[1] == NoneType
            ):
                if parameter.name == "offset":
                    offset_argument_position = idx
                    if limit_argument_position is not None:
                        page_capable = True
                    continue

                if parameter.name == "limit":
                    limit_argument_position = idx
                    if offset_argument_position is not None:
                        page_capable = True
                    continue

            if parameter.name not in [param.python_name for param in pcm]:
                parameter_concept = ParameterConceptFactory.from_parameter(parameter, description=docstring.param_description_by_name(parameter.name))
                for concept in parameter_concept.concepts:
                    for noun_phrases in [
                        find_noun_phrase_path(english_signature.object, concept.noun_phrases),
                        find_noun_phrase_path(english_signature.target, concept.noun_phrases),
                        concept.noun_phrases,
                    ]:
                        if noun_phrases:
                            concept.description = docstring.input_description_by_noun_phrases(noun_phrases)
                            if not concept.description:
                                concept.description = parameter_concept.description

                            if concept.description:
                                break
                pcm.append(parameter_concept)

        # add type for outputs
        outputs: List[ConceptDescriptor] = []
        return_annotation = python_signature.return_annotation
        if english_signature and english_signature.outputs:
            if len(english_signature.outputs) > 1 and len(english_signature.outputs) != len(return_annotation.__args__):
                raise SignatureError("the number of elements in the return tuple do not match the number of outputs in the english signature")

            for idx, output in enumerate(english_signature.outputs):
                sub_annotation = return_annotation.__args__[idx] if len(english_signature.outputs) > 1 else return_annotation
                outputs.append(
                    ConceptFactory.from_noun_phrases_and_annotation(
                        output,
                        sub_annotation,
                        description=docstring.output_description_by_noun_phrases(output),
                    )
                )
        elif return_annotation and return_annotation != inspect.Signature.empty:
            answer_noun_phrase = NounPhrase(head="answer", modifiers=[])
            outputs.append(
                ConceptFactory.from_noun_phrase_and_annotation(
                    answer_noun_phrase,
                    return_annotation,
                    description=(docstring.output_description_by_noun_phrases([answer_noun_phrase])),
                )
            )

        if len(outputs) == 1 and outputs[0].description is None and docstring.returns:
            outputs[0].description = docstring.returns

        return BookProcedureDescriptor(
            id=identifier,
            english_signature=english_signature,
            python_signature=python_signature,
            parameter_concept_map=pcm,
            outputs=outputs,
            filter_capable=filter_capable,
            filter_argument_position=filter_argument_position,
            page_capable=page_capable,
            offset_argument_position=offset_argument_position,
            limit_argument_position=limit_argument_position,
            connection_required=False,
            override_connection_required=override_connection_required,
            short_description=docstring.short_description.strip() if docstring.short_description else None,
            long_description=docstring.long_description.strip() if docstring.long_description else None,
            examples=[Example.from_docstring(docstring_example) for docstring_example in docstring.examples],
        )
