import re
from functools import partial
from itertools import product
from typing import List, Optional

from lmlib.schemas.model import (Decklength, FabricationYard, GrillageType,
                                 Monopile)
from lmlib.schemas.operational_specification import (GrillageCompatibility,
                                                     ParameterSpecification)


def separate_connectors(text, connectors=["of", "to"]):
    for conn in connectors:
        # find words ending with the connector and not already separated
        pattern = re.compile(rf"(\w+){conn}_(\w+)")
        text = pattern.sub(rf"\1_{conn}_\2", text)
    return text


def join_single_chars(input_str):
    return re.sub(r"_([a-zA-Z])_([a-zA-Z])(?=(_|$))", r"_\1\2", input_str)


def replace_double_underscore(input_string):
    return re.sub(r"__", "_", input_string)


def camel_case_to_snake_case(input: str, lower=True):
    if "_" in input and input.islower():  # O(n)
        return input  # O(1)
    result = re.sub(r"(?<!^)(?=[A-Z])", "_", input)  # O(n)
    target = result.lower() if lower else result  # O(n)
    target_with_joined_single_chars = join_single_chars(target)  # O(n)
    target_with_separate_connectors = separate_connectors(
        target_with_joined_single_chars
    )  # O(k * n) ; k = num of connectors
    return replace_double_underscore(target_with_separate_connectors)  # O(n)


class Operand:
    def __init__(self, adt_service, target_type, target_property, source_id, relation):

        # if target_property not in target_type.model_fields:
        #     raise ValueError(f"Property '{target_property}' is not defined in target type '{target_type.__name__}'")

        query = "SELECT target "
        query += "FROM digitaltwins source JOIN target RELATED "
        query += f"source.{relation} "
        query += f"where source.$dtId='{source_id}' "
        print(f"Operand : query - {query}")
        result = adt_service.query_digital_twins(query)
        print(f"Operand : query result - {result}")

        self.nodes = []
        for elem in result:

            input = {}
            for key in elem["target"].keys():

                if key == "$dtId":
                    input["id"] = elem["target"][key]
                    continue
                prop = camel_case_to_snake_case(key)
                if prop in target_type.model_json_schema()["properties"].keys():
                    input[prop] = elem["target"][key]
            print(f"Query results after cleaning - {input}")
            self.nodes.append(target_type(**input))

    def get(self):
        return self.nodes


class LengthConfigurations:

    @staticmethod
    def is_compatible(elem, scale_factor, property_lop, property_rop):
        length_lop, length_rop = elem
        # print(f"{length_lop}, {length_rop}, {property_lop}, {property_rop}, {scale_factor}")
        # print(f"{float(length_rop.model_dump()[property_rop])}, {float(length_lop.model_dump()[property_lop])}")
        return (
            float(length_rop.model_dump()[property_rop])
            - float(length_lop.model_dump()[property_lop]) * scale_factor
            > 0
        )

    def __init__(
        self,
        adt_service,
        twin_id,
        l_type,
        l_property,
        r_type,
        r_property,
        is_active: Optional[bool] = None,
    ):
        self.configurations = []
        if is_active is None:
            is_active = ParameterSpecification.model_fields["is_active"].default
        if not is_active:
            self.configurations = []
            return

        query = f"select * from digitaltwins where is_of_model('{ParameterSpecification.model_id}')"
        constraint_nodes = adt_service.query_digital_twins(query)
        # print([elem for elem in constraint_nodes])
        length_spec = [
            ParameterSpecification(
                value=elem["value"], value_unit_of_measure=elem["valueUnitOfMeasure"]
            )
            for elem in constraint_nodes
            if elem["$dtId"] == twin_id
        ]

        if length_spec:
            configuration: ParameterSpecification = length_spec[0]
            assert configuration.value_unit_of_measure == "percentage"
            compatibility_checker = partial(
                self.is_compatible,
                scale_factor=1 + float(configuration.value) * 0.01,
                property_lop=camel_case_to_snake_case(l_property),
                property_rop=camel_case_to_snake_case(r_property),
            )

            lop = Operand(adt_service, l_type, l_property, twin_id, "of")
            lnodes: List[Monopile] = lop.get()
            rop = Operand(adt_service, r_type, r_property, twin_id, "with")
            rnodes: List[Decklength] = rop.get()

            self.configurations = list(
                filter(compatibility_checker, product(lnodes, rnodes))
            )

    def get(self):
        return self.configurations


class GrillageConfigurations:

    # @staticmethod
    # def is_compatible(elem, property_lop, property_rop):
    #   length_lop, length_rop = elem
    #   #print(f"{length_lop}, {length_rop}, {property_lop}, {property_rop}, {scale_factor}")
    #   #print(f"{float(length_rop.model_dump()[property_rop])}, {float(length_lop.model_dump()[property_lop])}")
    #   return length_rop.model_dump()[property_rop] == length_lop.model_dump()[property_lop]

    def __init__(
        self,
        adt_service,
        twin_id,
        l_type,
        l_property,
        r_type,
        r_property,
        is_active: Optional[bool] = None,
    ):
        self.configurations = []
        if is_active is None:
            is_active = GrillageCompatibility.model_fields["is_active"].default
        if not is_active:
            self.configurations = []
            return

        query = f"select * from digitaltwins where is_of_model('{GrillageCompatibility.model_id}')"
        constraint_nodes = adt_service.query_digital_twins(query)
        # print([elem for elem in constraint_nodes])
        grillage_spec = [
            GrillageCompatibility(
                value="", value_unit_of_measure="", grillage_type=elem["grillageType"]
            )
            for elem in constraint_nodes
            if elem["$dtId"] == twin_id
        ]

        if grillage_spec:
            configuration: GrillageCompatibility = grillage_spec[0]
            # compatibility_checker  = partial(self.is_compatible,
            #                                   property_lop = camel_case_to_snake_case(l_property),
            #                                   property_rop =  camel_case_to_snake_case(r_property))

            lop = Operand(adt_service, l_type, l_property, twin_id, "ofFabricationYard")
            lnodes: List[FabricationYard] = lop.get()
            rop = Operand(adt_service, r_type, r_property, twin_id, "with")
            rnodes: List[GrillageType] = rop.get()

            valid_vessels = list(
                filter(
                    lambda x: x.grillage_type.value
                    == configuration.grillage_type.value,
                    rnodes,
                )
            )

            # valid_vessels = [
            #     vessel
            #     for vessel in rnodes
            #     if vessel.grillage_type.value == configuration.grillage_type.value
            # ]

            if lnodes:
                fab_yard = lnodes[0].id
                mlop = Operand(adt_service, Monopile, "", fab_yard, "fabricates")
                monopiles = mlop.get()

                self.configurations = list(product(monopiles, valid_vessels))

    def get(self):
        return self.configurations




class PreAllocatedConfigurations:

   

    def __init__(
        self,
        adt_service,
        twin_id,
        l_type,
        l_property,
        r_type,
        r_property,
        is_active: Optional[bool] = None,
    ):
        self.configurations = []
        if is_active is None:
            is_active = ParameterSpecification.model_fields["is_active"].default
        if not is_active:
            self.configurations = []
            return
        print("###############################PreAllocConfigActive##############################")
        query = f"select * from digitaltwins where is_of_model('{ParameterSpecification.model_id}')"
        constraint_nodes = adt_service.query_digital_twins(query)
       
        preallocation_spec = [
            elem["$dtId"]
            for elem in constraint_nodes
            if elem["$dtId"] == twin_id
        ]
        print(f"preallocation_spec: {preallocation_spec}")
        if preallocation_spec:
                
                query = "SELECT target "
                query += "FROM digitaltwins source JOIN target RELATED "
                query += f"source.contains "
                query += f"where source.$dtId='{preallocation_spec[0]}' "
                print(f"Operand : query - {query}")
                result = adt_service.query_digital_twins(query)
                print(f"Operand : query result - {result}")

                for elem in result:
                    print(f"#####Elem: {elem}")
                    lop = Operand(adt_service, l_type, l_property, elem["target"]["$dtId"], "of")
                    lnodes: List[Monopile] = lop.get()
                    rop = Operand(adt_service, r_type, r_property, elem["target"]["$dtId"], "with")
                    rnodes: List[Decklength] = rop.get()
                    if lnodes and rnodes:
                        self.configurations.extend(list(product(lnodes,rnodes))) 

    def get(self):
        return self.configurations
