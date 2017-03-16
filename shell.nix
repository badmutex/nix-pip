{ pkgs ? import ./pip2nix/data/nixpkgs.nix
, venvdir ? ".venv"
, name ? "cloudmesh_core"
}:

with pkgs;

let

  inherit (lib)
    getAttr
    hasAttr
    hasPrefix
    fileContents
    filter
    splitString
    stringLength
    ;

  callPythonPackage = path: attrs: with pythonPackages;
    callPackage path ({ inherit buildPythonPackage fetchPypi; } // attrs) ;

  myPythonPackages = pythonPackages // (with pythonPackages; {
    python-novaclient = novaclient;
    python-keystoneclient = keystoneclient;
    pygraphviz = pygraphviz.override (super: {doCheck = false;});
  });

  readRequirements = file:
    let
      cleaner = line: !(hasPrefix "#" line) && (stringLength line > 0);
      lines = splitString "\n" (fileContents file);
    in filter cleaner lines;

  findPackages = set: packageNames:
    let
      findPkg = name:
        if hasAttr name set
        then getAttr name set
        else throw "Cannot find '${name}'";
    in map findPkg packageNames;

  findPythonPackages = path: findPackages myPythonPackages (readRequirements path);

  requirements      = findPythonPackages ./requirements.open;
  test_requirements = findPythonPackages ./test_requirements.open;

  python = pythonFull.withPackages (_: requirements ++ test_requirements);

  buildInputs = [
    cacert
    libffi
    openssl
    pkgconfig
    sqlite
    zlib
  ];

in

pythonPackages.buildPythonPackage {
  name = "${name}";
  buildInputs = [ python ] ++ buildInputs;
}
