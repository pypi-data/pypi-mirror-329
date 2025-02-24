import re
from dmtgen.common.package import Package
from dmtgen.common.blueprint import Blueprint
from dmtgen.common.blueprint_attribute import BlueprintAttribute


def to_fortran_typename(name: str) -> str:
    return f'{name}_t'

def package_to_module_name(package: Package) -> str:
    return package.get_path().replace('/', '__')

def blueprint_to_module_name(blueprint: Blueprint) -> str:
    package_module = package_to_module_name(blueprint.parent)
    return f'{package_module}__{blueprint.name}'

def attribute_to_module_name(attr: BlueprintAttribute) -> str:
    components = attr.type.split('/')
    return '__'.join(components)
