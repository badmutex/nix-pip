Changelog
=========

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


