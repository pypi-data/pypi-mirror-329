.. image:: https://img.shields.io/github/issues-pr-raw/molssi-seamm/from_smiles_step
   :target: https://github.com/molssi-seamm/from_smiles_step/pulls
   :alt: GitHub pull requests

.. image:: https://github.com/molssi-seamm/from_smiles_step/workflows/CI/badge.svg
   :target: https://github.com/molssi-seamm/from_smiles_step/actions
   :alt: Build Status

.. image:: https://codecov.io/gh/molssi-seamm/from_smiles_step/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/molssi-seamm/from_smiles_step
   :alt: Code Coverage

.. image:: https://img.shields.io/lgtm/grade/python/g/molssi-seamm/from_smiles_step.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/molssi-seamm/from_smiles_step/context:python
   :alt: Code Quality

.. image:: https://github.com/molssi-seamm/from_smiles_step/workflows/Documentation/badge.svg
   :target: https://molssi-seamm.github.io/from_smiles_step/index.html
   :alt: Documentation Status

.. image:: https://pyup.io/repos/github/molssi-seamm/from_smiles_step/shield.svg
   :target: https://pyup.io/repos/github/molssi-seamm/from_smiles_step/
   :alt: Updates for Dependencies

.. image:: https://img.shields.io/pypi/v/from_smiles_step.svg
   :target: https://pypi.python.org/pypi/from_smiles_step
   :alt: PyPi VERSION

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.5159800.svg
   :target: https://doi.org/10.5281/zenodo.5159800
   :alt: DOI

=========================
SEAMM From SMILES plug-in
=========================

A SEAMM plug-in for creating structures from a SMILES string.

This plug-in accepts SMILES_ (Simplified Molecular-Input Line Entry
System) string representing a structure, and creates the structure if
the current system/conformation in SEAMM. It uses the implementation
in `Open Babel`_ which has an extension for handling radicals_.

* Free software: BSD license
* Documentation: https://from-smiles-step.readthedocs.io.

.. _SMILES: https://en.wikipedia.org/wiki/Simplified_molecular-input_line-entry_system
.. _`Open Babel`: http://openbabel.org/wiki/Main_Page
.. _radicals: http://openbabel.org/wiki/Radicals_and_SMILES_extensions

Features
--------

* Accepts with a SMILES string directly or from a variable.
* The generated structure can optionally be optimized using one of
  several forcefields.

Acknowledgements
----------------

This package was created with Cookiecutter_ and the `molssi-seamm/cookiecutter-seamm-plugin`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`molssi-seamm/cookiecutter-seamm-plugin`: https://github.com/molssi-seamm/cookiecutter-seamm-plugin

Developed by the Molecular Sciences Software Institute (MolSSI_),
which receives funding from the `National Science Foundation`_ under
award OAC-1547580 and CHE-2136142.

.. _MolSSI: https://www.molssi.org
.. _`National Science Foundation`: https://www.nsf.gov
