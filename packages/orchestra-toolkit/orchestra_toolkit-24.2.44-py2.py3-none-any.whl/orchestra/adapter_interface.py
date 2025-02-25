""" Copyright 2024-2025 LEDR Technologies Inc.
This file is part of the Orchestra library, which helps developer use our Orchestra technology which is based on AvesTerra, owned and developped by Georgetown University, under license agreement with LEDR Technologies Inc.
The Orchestra library is a free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
The Orchestra library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.
You should have received a copy of the GNU Lesser General Public License along with the Orchestra library. If not, see <https://www.gnu.org/licenses/>.
If you have any questions, feedback or issues about the Orchestra library, you can contact us at support@ledr.io.
"""

from dataclasses import dataclass, field
import avesterra as av


@dataclass
class Method:
    name: str
    description: str
    base: av.AvLocutorOpt
    args: list[av.AvAspect]
    value_in: av.AvValue = field(default_factory=lambda: av.NULL_VALUE)
    value_out: av.AvValue = field(default_factory=lambda: av.NULL_VALUE)


@dataclass
class Interface:
    name: str
    version: str
    description: str
    methods: list[Method]

    @staticmethod
    def from_avialmodel(model: av.AvialModel) -> "Interface":
        name = model.facts[av.AvAttribute.NAME].value.decode()
        if not isinstance(name, str):
            name = ""
        version = model.facts[av.AvAttribute.VERSION].value.decode()
        if not isinstance(version, str):
            version = ""
        description = model.facts[av.AvAttribute.DESCRIPTION].value.decode()
        if not isinstance(description, str):
            description = ""
        methods = []
        for facet in model.facts[av.AvAttribute.METHOD].facets:
            mname = facet.name
            mdescription = facet.value.decode()
            if not isinstance(mdescription, str):
                mdescription = ""
            mbase = facet.factors["base"].value.decode_locutor()
            margs = []
            for arg in facet.factors["args"].value.decode_array():
                margs.append(arg.decode_locutor().aspect)
            mvalue_in = facet.factors["value_in"].value
            mvalue_out = facet.factors["value_out"].value

            methods.append(
                Method(
                    name=mname,
                    description=mdescription,
                    base=mbase,
                    args=margs,
                    value_in=mvalue_in,
                    value_out=mvalue_out,
                )
            )

        return Interface(name, version, description, methods)

    def to_avialmodel(self) -> av.AvialModel:
        model = av.AvialModel()
        model.facts[av.AvAttribute.NAME].value = av.AvValue.encode_text(self.name)
        model.facts[av.AvAttribute.VERSION].value = av.AvValue.encode_string(
            self.version
        )
        model.facts[av.AvAttribute.DESCRIPTION].value = av.AvValue.encode_text(
            self.description
        )
        for method in self.methods:
            facet = model.facts[av.AvAttribute.METHOD].facets[method.name]
            facet.value = av.AvValue.encode_text(method.description)
            facet.factors["base"].value = av.AvValue.encode_locutor(method.base)
            facet.factors["args"].value = av.AvValue.encode_array(
                [
                    av.AvValue.encode_locutor(av.AvLocutor(aspect=arg))
                    for arg in method.args
                ]
            )
            facet.factors["value_in"].value = method.value_in
            facet.factors["value_out"].value = method.value_out
        return model
