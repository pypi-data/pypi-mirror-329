from typing import List, Optional

from docstring_parser import Docstring as BaseDocstring
from docstring_parser import DocstringMeta as BaseDocstringMeta
from docstring_parser import DocstringParam as BaseDocstringParam

from kognitos.bdk.klang import KlangParser

from ..api.noun_phrase import NounPhrase
from .example import DocstringExample


class DocstringConcept:
    _meta: Optional[BaseDocstringMeta]

    def __init__(self, meta: Optional[BaseDocstringMeta]):
        self._meta = meta

    @property
    def name(self) -> Optional[str]:
        if self._meta:
            return self._meta.args[1]

        return None

    @property
    def description(self) -> Optional[str]:
        if self._meta:
            return self._meta.description

        return None

    @property
    def noun_phrases(self) -> Optional[List[NounPhrase]]:
        try:
            if self._meta:
                noun_phrases, _ = KlangParser.parse_determiner_noun_phrases(self._meta.args[1])
                return [NounPhrase.from_tuple(np) for np in noun_phrases] if noun_phrases else None
        except SyntaxError:
            pass

        return None


class DocstringAttribute:
    _meta: Optional[BaseDocstringMeta]

    def __init__(self, meta: Optional[BaseDocstringMeta]):
        self._meta = meta

    @property
    def name(self) -> Optional[str]:
        if self._meta:
            return self._meta.args[1]

        return None

    @property
    def description(self) -> Optional[str]:
        if self._meta:
            return self._meta.description

        return None


class DocstringParam:
    _docstring: Optional[BaseDocstringParam]
    _meta: Optional[BaseDocstringMeta]

    def __init__(self, docstring: Optional[BaseDocstringParam], meta: Optional[BaseDocstringMeta]):
        self._docstring = docstring
        self._meta = meta

    @property
    def name(self) -> Optional[str]:
        if self._docstring:
            return self._docstring.arg_name

        if self._meta:
            return self._meta.args[1]

        return None

    @property
    def description(self) -> Optional[str]:
        if self._docstring:
            return self._docstring.description

        return None

    @property
    def label(self) -> Optional[str]:
        if self._meta:
            return self._meta.description

        return None


class Docstring:
    docstring: BaseDocstring

    def __init__(self, docstring: BaseDocstring):
        self.docstring = docstring

    @property
    def author(self) -> Optional[str]:
        for meta in self.docstring.meta:
            if "author" in meta.args:
                return meta.description
        return None

    @property
    def short_description(self) -> Optional[str]:
        return self.docstring.short_description

    @property
    def long_description(self) -> Optional[str]:
        return self.docstring.long_description

    @property
    def returns(self) -> Optional[str]:
        return self.docstring.returns.description if self.docstring.returns else None

    @property
    def input_concepts(self) -> List[DocstringConcept]:
        inputs = []

        for meta in self.docstring.meta:
            if len(meta.args) > 1:
                if meta.args[0] == "inputs":
                    inputs.append(DocstringConcept(meta))

        return inputs

    @property
    def examples(self) -> List[DocstringExample]:
        return [DocstringExample(example) for example in self.docstring.examples]

    @property
    def output_concepts(self) -> List[DocstringConcept]:
        outputs = []

        for meta in self.docstring.meta:
            if len(meta.args) > 1:
                if meta.args[0] == "outputs":
                    outputs.append(DocstringConcept(meta))

        return outputs

    @property
    def attributes(self) -> List[DocstringAttribute]:
        attributes = []

        for meta in self.docstring.meta:
            if len(meta.args) > 1:
                if meta.args[0] == "attribute":
                    attributes.append(DocstringAttribute(meta))

        return attributes

    @property
    def params(self) -> List[DocstringParam]:
        def convert_param(param: BaseDocstringParam):
            param_meta = None
            for meta in self.docstring.meta:
                if len(meta.args) > 1:
                    if meta.args[0] == "label" and meta.args[1] == param.arg_name:
                        param_meta = meta
                        break

            return DocstringParam(param, param_meta)

        params = list(map(convert_param, self.docstring.params))

        for meta in self.docstring.meta:
            if len(meta.args) > 1:
                if meta.args[0] == "label":
                    already = [param for param in params if param.name == meta.args[1]]
                    if not already:
                        params.append(DocstringParam(None, meta))

        return params

    def param_by_name(self, param: str) -> Optional[DocstringParam]:
        for doc_param in self.params:
            if doc_param.name == param:
                return doc_param

        return None

    def param_description_by_name(self, param: str) -> Optional[str]:
        for doc_param in self.params:
            if doc_param.name == param:
                return doc_param.description

        return None

    def input_concept_by_noun_phrases(self, noun_phrases: List[NounPhrase]) -> Optional[DocstringConcept]:
        for doc_concept in self.input_concepts:
            if doc_concept.noun_phrases == noun_phrases:
                return doc_concept

        return None

    def input_description_by_noun_phrases(self, noun_phrases: List[NounPhrase]) -> Optional[str]:
        for doc_concept in self.input_concepts:
            if doc_concept.noun_phrases == noun_phrases:
                return doc_concept.description

        return None

    def output_concept_by_noun_phrases(self, noun_phrases: List[NounPhrase]) -> Optional[DocstringConcept]:
        for doc_concept in self.output_concepts:
            if doc_concept.noun_phrases == noun_phrases:
                return doc_concept

        return None

    def output_description_by_noun_phrases(self, noun_phrases: List[NounPhrase]) -> Optional[str]:
        for doc_concept in self.output_concepts:
            if doc_concept.noun_phrases == noun_phrases:
                return doc_concept.description

        return None
