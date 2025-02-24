""" Copyright 2024-2025 LEDR Technologies Inc.
This file is part of the Orchestra library, which helps developer use our Orchestra technology which is based on AvesTerra, owned and developped by Georgetown University, under license agreement with LEDR Technologies Inc.
The Orchestra library is a free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
The Orchestra library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.
You should have received a copy of the GNU Lesser General Public License along with the Orchestra library. If not, see <https://www.gnu.org/licenses/>.
If you have any questions, feedback or issues about the Orchestra library, you can contact us at support@ledr.io.
"""

import json
from typing import Dict, List
import avesterra.avial as av
from avesterra.taxonomy import AvAttribute
from tabulate import tabulate


class AvialModel:
    """
    Data structure to hold an Avial model.
    more info on the Avial model can be found in the wiki:
    https://gitlab.com/ledr/core/dev-platform/developer-resources/-/wikis/The-Orchestra-Platform/Orchestra-model

    You can either build a model from scratch or load it from a JSON dictionary,
    which you can get by retrieving an existing entity and parsing the JSON string.
    You can turn the model back into a JSON dictionary to store it back in the
    entity.

    Do note that retrieve + modify + store paradigm is not thread safe and can
    lead to data loss if multiple threads (perhaps multiple clients) concurrently
    modify the same entity.
    When doing a lot of editing or when multiple clients are involved, it is
    recommended to use a DAO Object instead, which will only overwrite fields
    than were updated, therefore reducing the risk of data loss.

    Every aspect of the avial model can either be accessed through it's unique
    key or by index.
    Unique key are:
    - Properties: the key
    - Facts: the attribute
    - Facets: the name
    - Factors: the key
    - Features: the key
    - Fields: the name
    - Frames: the key

    If you try to access the NULL key, the first occurence of the NULL key will
    be returned.
    If you try to access a key that does not exist, a new object will be created

    This model makes it possible to create multiple objects with the same unique
    key by using the `append` method recklessly, which is not legal in Avial.
    You are responsible for ensuring it does not happen.
    Though it is possible to have multiple objects with the NULL key, the
    avial STORE operation does NOT support it. Therefore, this data structure
    only helps you to parse such models, not to create them.
    If you need to create such a model with multiple objects with the NULL key,
    you will need to use the specific avial methods insert/remove which support
    such operations by index.

    Note that index are 0-based, unlike the usual 1-based indexing in Avial.

    Example:
    ```
    auth = AvAuthorization("c08d118a-0ebf-4889-b5de-bbabbf841403")
    entity = av.AvEntity(0, 0, 177185)

    # Step 1 - Retrieve the entity
    val = av.retrieve_entity(entity, auth)

    # Step 2 - Parse the JSON string into an avial model
    model = AvialModel.from_interchange(val)

    # Step 3 - Read and modify it
    my_value = model.facts[AvAttribute.NAME].facets["first"].value = AvValue.encode_text("New first name")
    my_value = model.facts[AvAttribute.NAME].facets["first"].factors[0].value = AvValue.encode_text("I'm the first factor")
    my_value = model.facts[AvAttribute.NAME].facets["first"].factors["another"].value = AvValue.encode_text("I'm another factor")

    # Step 4 - Store the updated model back to the entity
    obj.store_entity(
        entity,
        AvMode.REPLACE,
        model.to_interchange(),
        auth,
    )
    ```
    """

    def __init__(self):
        self.name: str = ""
        self.key: str = ""
        self.data: int = 0
        self.properties = PropertyList()
        self.facts = FactList()

    def __eq__(self, other):
        return (
            self.name == other.name
            and self.key == other.key
            and self.data == other.data
            and self.properties == other.properties
            and self.facts == other.facts
        )

    def pretty_str(self, indent: int = 0):
        indent_str = " " * indent
        name_str = f"{indent_str}Name: {self.name}\n"
        key_str = f"{indent_str}Key: {self.key}\n"
        if self.data:
            data_str = f"{indent_str}Data: {self.data}\n"
        else:
            data_str = ""
        if self.properties:
            properties_str = f"{indent_str}Properties ({len(self.properties)}):\n{self.properties.pretty_str(indent+4)}\n"
        else:
            properties_str = ""
        if self.facts:
            facts_str = f"{indent_str}Facts ({len(self.facts)}):\n{self.facts.pretty_str(indent+4)}\n"
        else:
            facts_str = ""

        return f"{name_str}{key_str}{data_str}{properties_str}{facts_str}"

    @staticmethod
    def from_interchange(value: av.AvValue):
        """
        Safer way to create an AvialModel from an Interchange value retrieved
        from the object adapter.
        Compensates for a bug in the Object adapter causing to sometimes return
        invalid JSON string
        """
        s = value.decode_interchange()

        # This is guaranteed to be the right match because unescaped double
        # quotes cannot be found in the Name or Key fields
        attribute_index = s.find('"Attributes":')
        # This is guaranteed to be the right match because unescaped double
        # quotes cannot be found in values of the Facts field
        # Note that we search from the end because this guarantee does not
        # hold for the content of the Attributes field, whose value may
        # contain unescaped double quotes
        fact_index = s.rfind('"Facts":')

        if attribute_index != -1 and fact_index != -1:
            s = s[:attribute_index] + s[fact_index:]

        return AvialModel.from_json_dict(json.loads(s))

    @staticmethod
    def retrieve(entity: av.AvEntity, timeout: av.AvTimeout, auth: av.AvAuthorization):
        """
        Convenience method to retrieve an entity and get the result as an AvialModel
        """
        return AvialModel.from_interchange(av.retrieve_entity(entity, timeout, auth))

    def to_interchange(self) -> av.AvValue:
        return av.AvValue.encode_interchange(json.dumps(self.to_json_dict()))

    @staticmethod
    def from_json_dict(d: Dict):
        model = AvialModel()

        model.name = d.get("Name", "")
        model.key = d.get("Key", "")
        model.data = d.get("Data", 0)

        model.properties = PropertyList.from_json_list(d.get("Properties", []))
        model.facts = FactList.from_json_list(d.get("Facts", []))

        return model

    def to_json_dict(self):
        d = {}
        if self.name:
            d["Name"] = self.name
        if self.key:
            d["Key"] = self.key
        if self.data:
            d["Data"] = self.data
        if self.properties:
            d["Properties"] = self.properties.to_json_list()
        if self.facts:
            d["Facts"] = self.facts.to_json_list()
        return d


class Property:
    def __init__(
        self,
        name: str = "",
        key: str = "",
        value: av.AvValue = av.NULL_VALUE,
        annotations: Dict[AvAttribute, av.AvValue] | None = None,
    ):
        self.name = name
        self.key = key
        self.value = value
        self.annotations = annotations if annotations is not None else {}

    def __eq__(self, other):
        return (
            self.name == other.name
            and self.key == other.key
            and self.value == other.value
            and self.annotations == other.annotations
        )

    def pretty_str(self, indent: int = 0):
        indent_str = " " * indent
        return indent_str + str(self)

    def __str__(self):
        ann = (
            "[" + ", ".join(f"{k.name}: {v}" for k, v in self.annotations.items()) + "]"
        )
        return f"{self.name}\t[{self.key}]: {self.value} | {ann}"

    @staticmethod
    def from_json_list(li: List):
        p = Property()

        p.name = li[0]
        p.key = li[1]
        p.value = av.AvValue.from_json(li[2])
        if len(li) > 3:
            for k, v in li[3].items():
                attribute_name = k.removesuffix("_ATTRIBUTE")
                p.annotations[AvAttribute[attribute_name]] = av.AvValue.from_json(v)

        return p

    def to_json_list(self):
        li = []
        li.append(self.name)
        li.append(self.key)
        li.append(self.value.obj())
        if self.annotations:
            d = {}
            for k, v in self.annotations.items():
                d[k.name + "_ATTRIBUTE"] = v.obj()
            li.append(d)
        return li


class PropertyList:
    def __init__(self):
        self.properties: List[Property] = []

    def __bool__(self):
        return bool(self.properties)

    def __len__(self):
        return len(self.properties)

    def __eq__(self, other):
        return self.properties == other.properties

    def __str__(self):
        return "[" + ", ".join(str(p) for p in self.properties) + "]"

    def pretty_str(self, indent: int = 0):
        return "\n".join([p.pretty_str(indent) for p in self.properties])

    def __getitem__(self, item: int | str):
        return self._get_property(item)

    def _get_property(self, item: int | str) -> Property:
        if isinstance(item, int):
            return self.properties[item]
        elif isinstance(item, str):
            for p in self.properties:
                if p.key == item:
                    return p
            newp = Property()
            newp.key = item
            self.properties.append(newp)
            return newp
        else:
            raise TypeError(f"Invalid type for item: {type(item)}")

    def append(self, item: Property):
        self.properties.append(item)

    @staticmethod
    def from_json_list(li: List):
        model = PropertyList()

        for p in li:
            model.properties.append(Property.from_json_list(p))

        return model

    def to_json_list(self):
        return [p.to_json_list() for p in self.properties]


class Fact:
    def __init__(
        self,
        attribute: AvAttribute,
        value: av.AvValue = av.NULL_VALUE,
    ):
        self.attribute = attribute
        self.value = value
        self.facets = FacetList()
        self.features = FeatureList()
        self.fields = FieldList()
        self.frames = FrameList(self.fields)

    def __eq__(self, other):
        return (
            self.attribute == other.attribute
            and self.value == other.value
            and self.facets == other.facets
            and self.features == other.features
            and self.fields == other.fields
            and self.frames == other.frames
        )

    def pretty_str(self, indent: int = 0):
        indent_str = " " * indent
        attribute_str = f"{indent_str}Attribute: {self.attribute.name:<15} "
        value_str = f"{self.value.tag().name}: {self.value.decode()}\n"
        if self.facets:
            facet_str = f"{indent_str}Facets ({len(self.facets)}):\n{self.facets.pretty_str(indent+4)}\n"
        else:
            facet_str = ""
        if self.features:
            feature_str = f"{indent_str}Features ({len(self.features)}):\n{self.features.pretty_str(indent+4)}\n"
        else:
            feature_str = ""
        if self.fields:
            field_str = f"{indent_str}Fields ({len(self.fields)}):\n{self.fields.pretty_str(indent+4)}\n"
        else:
            field_str = ""
        if self.frames:
            frame_str = f"{indent_str}Frames ({len(self.frames)}):\n{self.frames.pretty_str(indent+4)}\n"
        else:
            frame_str = ""
        return (
            f"{attribute_str}{value_str}{facet_str}{feature_str}{field_str}{frame_str}"
        )

    @staticmethod
    def from_json_list(li: List):
        f = Fact(AvAttribute.NULL)

        attribute_name = li[0].removesuffix("_ATTRIBUTE")
        f.attribute = AvAttribute[attribute_name]
        f.value = av.AvValue.from_json(li[1])
        f.facets = FacetList.from_json_list(li[2])
        f.features = FeatureList.from_json_list(li[3])
        f.fields = FieldList.from_json_list(li[4])
        f.frames = FrameList.from_json_list(li[5], f.fields)
        f.frames.fields = f.fields

        return f

    def to_json_list(self):
        li = []
        li.append(self.attribute.name + "_ATTRIBUTE")
        li.append(self.value.obj())
        li.append(self.facets.to_json_list())
        li.append(self.features.to_json_list())
        li.append(self.fields.to_json_list())
        li.append(self.frames.to_json_list())
        return li


class FactList:
    def __init__(self):
        self.facts: List[Fact] = []

    def __bool__(self):
        return bool(self.facts)

    def __len__(self):
        return len(self.facts)

    def __eq__(self, other):
        return self.facts == other.facts

    def __str__(self):
        return "[" + ", ".join(str(p) for p in self.facts) + "]"

    def pretty_str(self, indent: int = 0):
        return "".join([f.pretty_str(indent) for f in self.facts])

    def __getitem__(self, item: int | AvAttribute):
        if isinstance(item, AvAttribute):
            for f in self.facts:
                if f.attribute == item:
                    return f
            newf = Fact(item)
            self.facts.append(newf)
            return newf
        elif isinstance(item, int):
            return self.facts[item]
        else:
            raise TypeError(f"Invalid type for item: {type(item)}")

    def append(self, item: Fact):
        self.facts.append(item)

    @staticmethod
    def from_json_list(li: List):
        model = FactList()

        for f in li:
            model.facts.append(Fact.from_json_list(f))

        return model

    def to_json_list(self):
        return [f.to_json_list() for f in self.facts]


class Facet:
    def __init__(self, name: str, value: av.AvValue = av.NULL_VALUE):
        self.name = name
        self.value = value
        self.factors = FactorList()

    def __eq__(self, other):
        return (
            self.name == other.name
            and self.value == other.value
            and self.factors == other.factors
        )

    def pretty_str(self, indent: int = 0):
        indent_str = " " * indent
        if self.factors:
            factor_str = f"{indent_str}Factors ({len(self.factors)}):\n{self.factors.pretty_str(indent+4)}\n"
        else:
            factor_str = ""
        return f"{indent_str}Name: {self.name}\n{indent_str}Value: {self.value}\n{factor_str}"

    @staticmethod
    def from_json_list(li: List):
        f = Facet("")

        f.name = li[0]
        f.value = av.AvValue.from_json(li[1])
        f.factors = FactorList.from_json_list(li[2])

        return f

    def to_json_list(self):
        li = []
        li.append(self.name)
        li.append(self.value.obj())
        li.append(FactorList.to_json_list(self.factors))
        return li


class FacetList:
    def __init__(self):
        self.facets: List[Facet] = []

    def __bool__(self):
        return bool(self.facets)

    def __len__(self):
        return len(self.facets)

    def __eq__(self, other):
        return self.facets == other.facets

    def __str__(self):
        return "[" + ", ".join(str(p) for p in self.facets) + "]"

    def pretty_str(self, indent: int = 0):
        return "\n".join([f.pretty_str(indent) for f in self.facets])

    def __getitem__(
        self,
        item: int | str,
    ):
        if isinstance(item, int):
            return self.facets[item]
        elif isinstance(item, str):
            for f in self.facets:
                if f.name == item:
                    return f
            newf = Facet(item)
            self.facets.append(newf)
            return newf
        else:
            raise TypeError(f"Invalid type for item: {type(item)}")

    def append(self, item: Facet):
        self.facets.append(item)

    @staticmethod
    def from_json_list(li: List):
        model = FacetList()

        for f in li:
            model.facets.append(Facet.from_json_list(f))

        return model

    def to_json_list(self):
        return [f.to_json_list() for f in self.facets]


class Factor:
    def __init__(self, key: str, value: av.AvValue = av.NULL_VALUE):
        self.key = key
        self.value = value

    def __eq__(self, other):
        return self.key == other.key and self.value == other.value

    def pretty_str(self, indent: int = 0):
        indent_str = " " * indent
        return f"{indent_str}{self.key}: {self.value}"

    @staticmethod
    def from_json_list(li: List):
        f = Factor("")

        f.key = li[0]
        f.value = av.AvValue.from_json(li[1])

        return f

    def to_json_list(self):
        li = []
        li.append(self.key)
        li.append(self.value.obj())
        return li


class FactorList:
    def __init__(self):
        self.factors: List[Factor] = []

    def __bool__(self):
        return bool(self.factors)

    def __len__(self):
        return len(self.factors)

    def __eq__(self, other):
        return self.factors == other.factors

    def __str__(self):
        return "[" + ", ".join(str(p) for p in self.factors) + "]"

    def pretty_str(self, indent: int = 0):
        return "\n".join([f.pretty_str(indent) for f in self.factors])

    def __getitem__(self, item: int | str):
        if isinstance(item, int):
            return self.factors[item]
        elif isinstance(item, str):
            for f in self.factors:
                if f.key == item:
                    return f
            newf = Factor("")
            newf.key = item
            self.factors.append(newf)
            return newf
        else:
            raise TypeError(f"Invalid type for item: {type(item)}")

    def append(self, item: Factor):
        self.factors.append(item)

    @staticmethod
    def from_json_list(li: List):
        model = FactorList()

        for f in li:
            model.factors.append(Factor.from_json_list(f))

        return model

    def to_json_list(self):
        return [f.to_json_list() for f in self.factors]


class Feature:
    def __init__(self, name: str, key: str, value: av.AvValue = av.NULL_VALUE):
        self.name = name
        self.key = key
        self.value = value

    def __eq__(self, other):
        return (
            self.name == other.name
            and self.key == other.key
            and self.value == other.value
        )

    def pretty_str(self, indent: int = 0):
        indent_str = " " * indent
        return f"{indent_str}{self.name}\t[{self.key}]: {self.value}"

    @staticmethod
    def from_json_list(li: List):
        f = Feature("", "")

        f.name = li[0]
        f.key = li[1]
        f.value = av.AvValue.from_json(li[2])

        return f

    def to_json_list(self):
        li = []
        li.append(self.name)
        li.append(self.key)
        li.append(self.value.obj())
        return li


class FeatureList:
    def __init__(self):
        self.features: List[Feature] = []

    def __bool__(self):
        return bool(self.features)

    def __len__(self):
        return len(self.features)

    def __eq__(self, other):
        return self.features == other.features

    def __str__(self):
        return "[" + ", ".join(str(p) for p in self.features) + "]"

    def pretty_str(self, indent: int = 0):
        return "\n".join([f.pretty_str(indent) for f in self.features])

    def __getitem__(self, item: int | str):
        if isinstance(item, int):
            return self.features[item]
        elif isinstance(item, str):
            for f in self.features:
                if f.key == item:
                    return f
            newf = Feature("", item)
            self.features.append(newf)
            return newf
        else:
            raise TypeError(f"Invalid type for item: {type(item)}")

    def append(self, item: Feature):
        self.features.append(item)

    @staticmethod
    def from_json_list(li: List):
        model = FeatureList()

        for f in li:
            model.features.append(Feature.from_json_list(f))

        return model

    def to_json_list(self):
        return [f.to_json_list() for f in self.features]


class Field:
    def __init__(self, name: str, value: av.AvValue = av.NULL_VALUE):
        self.name = name
        self.value = value

    def __eq__(self, other):
        return self.name == other.name and self.value == other.value

    def pretty_str(self, indent: int = 0):
        indent_str = " " * indent
        return f"{indent_str}{self.name}: {self.value}"

    @staticmethod
    def from_json_list(li: List):
        f = Field("")

        f.name = li[0]
        f.value = av.AvValue.from_json(li[1])

        return f

    def to_json_list(self):
        li = []
        li.append(self.name)
        li.append(self.value.obj())
        return li


class FieldList:
    def __init__(self):
        self.fields: List[Field] = []

    def __bool__(self):
        return bool(self.fields)

    def __len__(self):
        return len(self.fields)

    def __eq__(self, other):
        return self.fields == other.fields

    def __str__(self):
        return "[" + ", ".join(str(p) for p in self.fields) + "]"

    def pretty_str(self, indent: int = 0):
        return "\n".join([f.pretty_str(indent) for f in self.fields])

    def __getitem__(self, item: int | str):
        if isinstance(item, int):
            return self.fields[item]
        elif isinstance(item, str):
            idx = self.index_of(item)
            if idx != -1:
                return self.fields[idx]
            newf = Field(item)
            self.fields.append(newf)
            return newf
        else:
            raise TypeError(f"Invalid type for item: {type(item)}")

    def append(self, item: Field):
        self.fields.append(item)

    def index_of(self, name: str):
        for i, f in enumerate(self.fields):
            if f.name == name:
                return i
        return -1

    @staticmethod
    def from_json_list(li: List):
        model = FieldList()

        for f in li:
            model.fields.append(Field.from_json_list(f))

        return model

    def to_json_list(self):
        return [f.to_json_list() for f in self.fields]


class Frame:
    def __init__(self, key: str, values: List[av.AvValue] | None = None):
        self.key = key
        self.values: List[av.AvValue] = values if values is not None else []
        self.fields: FieldList | None = None

    def __eq__(self, other):
        return self.key == other.key and self.values == other.values

    def __len__(self):
        return len(self.values)

    def __getitem__(self, item: int | str):
        assert self.fields is not None
        if isinstance(item, int):
            return self.values[item]
        elif isinstance(item, str):
            idx = self.fields.index_of(item)
            if idx != -1:
                return self.values[idx]
            raise ValueError(f"Field '{item}' not found")
        else:
            raise TypeError(f"Invalid type for item: {type(item)}")

    def __setitem__(self, item: int | str, value: av.AvValue):
        assert self.fields is not None
        if isinstance(item, int):
            self.values[item] = value
        elif isinstance(item, str):
            idx = self.fields.index_of(item)
            if idx != -1:
                self.values[idx] = value
                return
            raise ValueError(
                f"Field '{item}' not found, available fields: {', '.join(f.name for f in self.fields)}"
            )
        else:
            raise TypeError(f"Invalid type for item: {type(item)}")

    @staticmethod
    def from_json_list(li: List):
        f = Frame("")

        f.key = li[0]
        f.values = [av.AvValue.from_json(f) for f in li[1]]

        return f

    def to_json_list(self):
        li = []
        li.append(self.key)
        li.append([f.obj() for f in self.values])
        return li


class FrameList:
    def __init__(self, fields: FieldList | None = None):
        self.frames: List[Frame] = []
        self.fields = fields

    def __bool__(self):
        return bool(self.frames)

    def __len__(self):
        return len(self.frames)

    def __eq__(self, other):
        return self.frames == other.frames

    def __str__(self):
        return "[" + ", ".join(str(p) for p in self.frames) + "]"

    def pretty_str(self, indent: int = 0):
        assert self.fields is not None
        indent_str = " " * indent
        headers = [f.name for f in self.fields]
        rows = []
        for f in self.frames:
            rows.append([f.key] + [f"{v.tag().name}: {v.decode()}" for v in f.values])

        res = tabulate(rows, headers=headers)
        res = indent_str + res.replace("\n", "\n" + indent_str)

        return res

    def __getitem__(self, item: int | str):
        assert self.fields is not None
        if isinstance(item, int):
            return self.frames[item]
        elif isinstance(item, str):
            for f in self.frames:
                if f.key == item:
                    return f
            newf = Frame(item)
            newf.fields = self.fields
            for f in self.fields:
                newf.values.append(f.value)

            self.frames.append(newf)
            return newf
        else:
            raise TypeError(f"Invalid type for item: {type(item)}")

    @staticmethod
    def from_json_list(li: List, fields: FieldList):
        model = FrameList()
        model.fields = fields

        for f in li:
            frame = Frame.from_json_list(f)
            frame.fields = model.fields
            model.frames.append(frame)

        return model

    def to_json_list(self):
        return [f.to_json_list() for f in self.frames]
