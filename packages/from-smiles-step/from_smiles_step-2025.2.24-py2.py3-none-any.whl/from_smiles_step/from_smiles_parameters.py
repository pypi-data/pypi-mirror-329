# -*- coding: utf-8 -*-
"""Control parameters for generating a structure from SMILES"""

import logging
import seamm

logger = logging.getLogger(__name__)


class FromSMILESParameters(seamm.Parameters):
    """The control parameters for creating a structure from SMILES"""

    parameters = {
        "notation": {
            "default": "perceive",
            "kind": "enum",
            "default_units": "",
            "enumeration": ("perceive", "SMILES", "InChI", "InChIKey", "name"),
            "format_string": "s",
            "description": "Input notation:",
            "help_text": "The line notation used.",
        },
        "smiles string": {
            "default": "",
            "kind": "string",
            "default_units": "",
            "enumeration": tuple(),
            "format_string": "s",
            "description": "Input:",
            "help_text": "The input string for the structure.",
        },
        "smiles flavor": {
            "default": "rdkit",
            "kind": "string",
            "default_units": "",
            "enumeration": ("rdkit", "openbabel", "openeye"),
            "format_string": "s",
            "description": "SMILES flavor:",
            "help_text": "The flavor of SMILES to use.",
        },
    }

    def __init__(self, defaults={}, data=None):
        """Initialize the instance, by default from the default
        parameters given in the class"""

        super().__init__(
            defaults={
                **FromSMILESParameters.parameters,
                **seamm.standard_parameters.structure_handling_parameters,
                **defaults,
            },
            data=data,
        )

        # Do any local editing of defaults
        tmp = self["structure handling"]
        tmp.description = "Structure handling:"

        tmp = self["system name"]
        tmp.default = "use Canonical SMILES string"

        tmp = self["configuration name"]
        tmp._data["enumeration"] = ["initial", *tmp.enumeration]
        tmp.default = "initial"
