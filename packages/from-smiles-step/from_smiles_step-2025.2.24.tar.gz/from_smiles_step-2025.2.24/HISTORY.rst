=======
History
=======
2024.2.24 -- Added isomeric SMILES to structure names and ability to discard structures
    * Added ability to ignore or discard a structure from e.g. optimization
    * Added isomeric SMILES to the possible names for systems and configurations
      
2024.10.31 -- Bugfix: Issue recognizing chemical names
    * Fixed an issue where the chemical name was handled as SMILES, causing the code to
      crash. 
      
2023.11.10 -- Bugfix: New configurations created incorrectly
    * New configurations made from other systems could remove the atoms in those
      systems.
      
2023.11.9.1 -- Removed using structure names when perceiving type
    * Using structure names is too dangerous to use by perceiving if text is a name of
      SMILES and there is no easy test for valid SMILES. So change to only using names
      if the user specifies names.
      
2023.11.9 -- Improved structure handling, added from names
    * Switched to standard structure handling, which adds more options
    * Added getting structures from Pubchem using the chemical name.
      
2023.7.18 -- Added support for InChI and InChIKeys

2021.2.10 (10 February 2021)
----------------------------

* Updated the README file to give a better description.
* Updated the short description in setup.py to work with the new installer.
* Added keywords for better searchability.

2020.2.4 (4 February 2021)
--------------------------

* Internal Changes

  - Corrected an issue in CI.

2021.2.3 (3 February 2021)
--------------------------

* Internal Changes

  - Upgraded to be compatible with the improved version of the
    MolSystem classes for describing the molecular system.

2020.12.4 (4 December 2020)
---------------------------

* Internal Changes

  - Moved the continuous integration (CI) to GitHub Actions from
    TravisCI.
  - Moved documentation from ReadTheDocs to GitHub Pages and
    integrated with the rest of the SEAMM documentation.

2020.11.2 (2 November 2020)
---------------------------

* Moved to the new command-line argument handling.

2020.9.24.1 (24 September 2020)
-------------------------------

* Fixed small bug with the title of the system when generated from SMILES.

2020.9.24 (24 September 2020)
-----------------------------

* Updated to work with the new MolSystem classes describing the
  molecular system.

0.9 (15 April 2020)
-------------------

* Internal changes for compatibility.

0.7.0 (17 December 2019)
------------------------

* Internal changes cleaning the code.
  
0.1.0 (20 January 2018)
-----------------------

* First release on PyPI.
