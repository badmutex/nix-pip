{ pkgs ? import <nixpkgs> {}
, python ? pkgs.pythonFull
, pythonPackages ? pkgs.pythonPackages
, requirements_nix ? ./requirements.nix
, ignoreCollisions ? true
, ...
}@args:

# Accept packages definitions and return a set of derivation sets.
#
# This assumes that nix-pip has been run to generate
# ./requirements.nix containing the derivations of all the python
# requirements.
#
# Example, in shell.nix or default.nix add something like:
#
# nixpip = callPackage ./nixpip.nix {
#   inherit pkgs;
#   runtime = ./requirements.txt;
#   testing = ["pytest"];
#   docs = ["sphinx"];
#   };
#   
# This returns a set with "python" and "requirements" as names,
# mapping to sets with the corresponding "runtime", "testing", and
# "docs" requirement sets and python interpreters.
#
# For instances:
#
# - nixpip.requirements.runtime
# - nixpip.python.testing
#
# Additionally, there is a "all" for each "requirements" or "python"
# child with the entire set of requirements:
#
# - nixpip.python.all
# - nixpip.requirements.all



let

  inherit (pkgs)
    fetchurl
    ;

  inherit (pkgs.lib)
    attrValues
    getAttr
    hasAttr
    hasPrefix
    elem
    fileContents
    filter
    filterAttrs
    flatten
    id
    isList
    mapAttrs
    mapAttrs'
    nameValuePair
    replaceStrings
    splitString
    stringLength
    ;

  args' =
    let reserved_names = ["pkgs" "python" "pythonPackages" "requirements_nix" "ignoreCollisions"];
    in filterAttrs (n: _: !elem n reserved_names) args;

  callPythonPackage = path: attrs: with pythonPackages;
    callPackage path ({ inherit buildPythonPackage fetchPypi; } // attrs) ;

  packages = import requirements_nix {
    inherit pkgs fetchurl;
    inherit (pythonPackages) buildPythonPackage;
  };

  allPythonPackages = pythonPackages // packages;

  readRequirements = file:
    let
      cleaner = line: !(hasPrefix "#" line) && (stringLength line > 0);
      lines = splitString "\n" (fileContents file);

      fixDots = replaceStrings ["."] ["-"];
      # dotted names are valid python pkg names, but are not what we
      # want in a Nix pkg set. `nix-pip` applies this transformation
      # when generating the package set, which is needed when reading
      # in the python requirements from a file or other input.

    in map fixDots (filter cleaner lines);

  findPackages = set: packageNames:
    let
      findPkg = name:
        if hasAttr name set
        then getAttr name set
        else throw "Cannot find '${name}'";
    in map findPkg packageNames;


  reqs =
  # Map the components of the requested requirements to their python package names
    let

      find_drvs = given:
      # find the drvs for the given requirements
        let
          doPath = path:  findPackages allPythonPackages (readRequirements path);
          doList = names: findPackages allPythonPackages names;
        in if isList given
           then doList
           else doPath;

    in mapAttrs find_drvs args';

  mkPython = reqs: python.buildEnv.override {
    extraLibs = reqs;
    ignoreCollisions = ignoreCollisions;
  };

  mkAll = fn: set: { all = fn (flatten (attrValues set)); };

in { python = (mapAttrs (_: reqs: mkPython reqs) reqs) // mkAll mkPython reqs;
     requirements = reqs // mkAll id reqs;
   }
