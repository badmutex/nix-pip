{ pkgs ? import ./nixpip/data/nixpkgs.nix
}:

with pkgs;

let

  inherit (lib)
    getAttr
    hasAttr
    hasPrefix
    fileContents
    filter
    replaceStrings
    splitString
    stringLength
    ;


  version = builtins.readFile ./nixpip/VERSION;

  callPythonPackage = path: attrs: with pythonPackages;
    callPackage path ({ inherit buildPythonPackage fetchPypi; } // attrs) ;

  packages = import ./requirements.nix {
    inherit pkgs fetchurl;
    inherit (pythonPackages) buildPythonPackage;
  };

  myPythonPackages = pythonPackages // packages;

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

  findPythonPackages = path: findPackages myPythonPackages (readRequirements path);

  requirements      = findPythonPackages ./requirements.open;
  test_requirements = findPythonPackages ./test_requirements.open;

  python = pythonFull.buildEnv.override {
    extraLibs = requirements ++ test_requirements;
    ignoreCollisions = true;
  };


  buildInputs = [
    cacert
    libffi
    openssl
    pkgconfig
    sqlite
    zlib
  ];

in

pythonPackages.buildPythonApplication {
  inherit version;
  name = "nixpip-${version}";
  propagatedBuildInputs = buildInputs ++ builtins.attrValues packages;
  src = ./.;
}
