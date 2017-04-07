Changelog
=========

v0.3.1 (2017-04-07)
-------------------

Fix
~~~

- Fix invocation without a config file present. [Badi' Abdul-Wahid]

- Correct incorrectly import yaml module. [Badi' Abdul-Wahid]

- Correctly get nested Nix attribute name from pkgs. [Badi' Abdul-Wahid]

  Specifying ``buildInputs`` like ``gcc.cc`` or
  ``pythonPackages.cython`` due to the use of ``lib.getAttr``. This
  switches to ``lib.getAttrFromPath``

v0.3.0 (2017-04-06)
-------------------

Changes
~~~~~~~

- Rename entrypoint from ``pip2nix`` to ``nix-pip`` [Badi' Abdul-Wahid]

- Update example in readme. [Badi' Abdul-Wahid]

v0.2.0 (2017-04-06)
-------------------

New
~~~

- Learn to load configurations from a yaml file. [Badi' Abdul-Wahid]

  The settings file should have three sections:
  - ``requirements``
  - ``setup_requires``
  - ``build_inputs``

  If these are not set a default empty configuration is used.

  **requirements**

  - inputs: a list of pip requirements files to read
    eg::

      - requirements.txt
      - requirements-test.txt

  - output: the output file to generate
    default: ``requirements.nix``

  - packages: list of extra python package requirements
    eg::

      - requests
      - vcversioner==2.16.0.0

  **setup_requires** and **build_inputs**

  These sections are a mapping from package name to any requirements needed
  to install and build (respectively) the package.

  For instance::

    setup_requires:
      munch:
        - six

    build_inputs:
      pygraphviz:
        - graphviz
        - pkgconfig
      pyyaml:
        - libyaml

  The ``build_inputs`` entries map a python package name to the Nix
  derivation names relative the top level of the Nix packge set.

- Learn to reuse frozen packages accross independant invokations. [Badi'
  Abdul-Wahid]

Changes
~~~~~~~

- Remove obsolete requirement from readme. [Badi' Abdul-Wahid]

- Update readme. [Badi' Abdul-Wahid]

- Sort ``inputs`` and ``propagatedBuildInputs`` lexicographically.
  [Badi' Abdul-Wahid]

Fix
~~~

- Change name of repository to nix-pip in readme. [Badi' Abdul-Wahid]

- Fix type error on sorted buildInputs. [Badi' Abdul-Wahid]

v0.1.2 (2017-04-03)
-------------------

New
~~~

- Add installation instructions to readme. [Badi' Abdul-Wahid]

- Learn to get version with ``-V`` or ``--version`` [Badi' Abdul-Wahid]

- Add changelog. [Badi' Abdul-Wahid]

Changes
~~~~~~~

- Install using ``nix-env -f . -i`` [Badi' Abdul-Wahid]

Fix
~~~

- Correctly handle hyphenated PyPI package names. [Badi' Abdul-Wahid]

  Due to bad regex hyphenated PyPI package names were truncated at the
  hyphen. Eg "apache-libcloud" became just "apache"

- Remove unsupported usage from readme. [Badi' Abdul-Wahid]

v0.1.1 (2017-03-31)
-------------------

New
~~~

- Eat our dogfood. [Badi' Abdul-Wahid]

  This change generates requirements.nix for this package

Fix
~~~

- Pass buildInputs to intermediate builds. [Badi' Abdul-Wahid]

- Show output when nix-shell fails. [Badi' Abdul-Wahid]

v0.1.0 (2017-03-29)
-------------------

New
~~~

- Release version 0.1.0. [Badi' Abdul-Wahid]

- Readme: add Features section. [Badi' Abdul-Wahid]

- Support caching the dependency graph. [Badi' Abdul-Wahid]

- Learn --setup-requires. [Badi' Abdul-Wahid]

- Use colored logging output. [Badi' Abdul-Wahid]

Changes
~~~~~~~

- Readme: describe usage. [Badi' Abdul-Wahid]

Fix
~~~

- Normalize pkg names to lowercase. [Badi' Abdul-Wahid]

  Sometimes (eg flask, eve) detected package names are capitalized (eg
  Flask, Eve), which causes confusion when lookup up packages from the
  provided requirements.txt.

- Readme: update procedure. [Badi' Abdul-Wahid]

- Readme: fix links for requirements. [Badi' Abdul-Wahid]

- Dev expose system-provided python derivations if needed. [Badi' Abdul-
  Wahid]


