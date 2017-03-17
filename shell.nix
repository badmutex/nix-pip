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


  monotonic = pythonPackages.buildPythonPackage {
    name = "monotonic";
    version = "1.3";
    src = fetchurl {
      url = "https://pypi.python.org/packages/1e/4c/f58022573cd15125bc03114913906bcb6d9bc1a4b8a170a88e0525b6cd51/monotonic-1.3-py2.py3-none-any.whl";
      sha256 = "a8c7690953546c6bc8a4f05d347718db50de1225b29f4b9f346c0c6f19bdc286";
    };
    format = "wheel";
  };

  humanfriendly = pythonPackages.buildPythonPackage {
    name = "humanfriendly";
    version = "2.4";
    src = fetchurl {
      url = "https://pypi.python.org/packages/ce/f0/3f6022be8ed23b86d84d749672b487438496d802309e3e771c83b80540e0/humanfriendly-2.4-py2.py3-none-any.whl";
      sha256 = "af81b05b794dff4df2657f144fe384f80ca5f422ddef8026e2040c7b0924e609";
    };
    format = "wheel";
    propagatedBuildInputs = [ monotonic ];
  };

  coloredlogs = pythonPackages.buildPythonPackage {
    name = "coloredlogs";
    version = "6.0";
    src = fetchurl {
      url = "https://pypi.python.org/packages/d7/a8/4aa2891bd3324d57edabf4cb031db33b06570f3bb3f33ebbdd034ee6f23f/coloredlogs-6.0-py2.py3-none-any.whl";
      sha256 = "b97cd81e39f359b4d6310881633dadc4dc77ea9b2f035941fe8c6d4be1a7d5c4";
    };
    format = "wheel";
    propagatedBuildInputs = [ humanfriendly ];
  };


  callPythonPackage = path: attrs: with pythonPackages;
    callPackage path ({ inherit buildPythonPackage fetchPypi; } // attrs) ;

  myPythonPackages = pythonPackages // (with pythonPackages; {
    inherit coloredlogs;
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
