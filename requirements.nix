{ pkgs
, buildPythonPackage
, fetchurl
, extras ? []
, ...
}:

with pkgs;
with pythonPackages;

rec {

  click = buildPythonPackage {
      name = "click-6.7";
      src = fetchurl {
        url = "https://pypi.python.org/packages/95/d9/c3336b6b5711c3ab9d1d3a80f1a3e2afeb9d8c02a7166462f6cc96570897/click-6.7.tar.gz";
        sha256 = "f15516df478d5a56180fbf80e68f206010e6d160fc39fa508b65e035fd75130b";
      };
      format = "setuptools";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  coloredlogs = buildPythonPackage {
      name = "coloredlogs-6.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/d7/a8/4aa2891bd3324d57edabf4cb031db33b06570f3bb3f33ebbdd034ee6f23f/coloredlogs-6.0-py2.py3-none-any.whl";
        sha256 = "b97cd81e39f359b4d6310881633dadc4dc77ea9b2f035941fe8c6d4be1a7d5c4";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [ humanfriendly ];
      doCheck = false;
    }
    ;
  decorator = buildPythonPackage {
      name = "decorator-4.0.11";
      src = fetchurl {
        url = "https://pypi.python.org/packages/cc/ac/5a16f1fc0506ff72fcc8fd4e858e3a1c231f224ab79bb7c4c9b2094cc570/decorator-4.0.11.tar.gz";
        sha256 = "953d6bf082b100f43229cf547f4f97f97e970f5ad645ee7601d55ff87afdfe76";
      };
      format = "setuptools";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  humanfriendly = buildPythonPackage {
      name = "humanfriendly-2.4";
      src = fetchurl {
        url = "https://pypi.python.org/packages/ce/f0/3f6022be8ed23b86d84d749672b487438496d802309e3e771c83b80540e0/humanfriendly-2.4-py2.py3-none-any.whl";
        sha256 = "af81b05b794dff4df2657f144fe384f80ca5f422ddef8026e2040c7b0924e609";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [ monotonic ];
      doCheck = false;
    }
    ;
  monotonic = buildPythonPackage {
      name = "monotonic-1.3";
      src = fetchurl {
        url = "https://pypi.python.org/packages/96/b3/3e9fa0bdf132a971571cbf0e3f0c8b38834f4f7af8ca9523794f4f5895e0/monotonic-1.3.tar.gz";
        sha256 = "2b469e2d7dd403f7f7f79227fe5ad551ee1e76f8bb300ae935209884b93c7c1b";
      };
      format = "setuptools";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  munch = buildPythonPackage {
      name = "munch-2.1.1";
      src = fetchurl {
        url = "https://pypi.python.org/packages/84/dc/d897cb427f15029e04745a3de611d8ed3d97e9a0ef894547a0ba261f2807/munch-2.1.1.tar.gz";
        sha256 = "648b650d1eb0173bd83c29f2eea2568b7591c1e05c87971387d170c71c6397e8";
      };
      format = "setuptools";
      buildInputs = [  ];
      propagatedBuildInputs = [ six ];
      doCheck = false;
    }
    ;
  networkx = buildPythonPackage {
      name = "networkx-1.11";
      src = fetchurl {
        url = "https://pypi.python.org/packages/d3/2c/e473e54afc9fae58dfa97066ef6709a7e35a1dd1c28c5a3842989322be00/networkx-1.11-py2.py3-none-any.whl";
        sha256 = "1b229b54fe9ccb009cee4de02a88552191497a542a7d5d34adab216b9f15c1ff";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [ decorator ];
      doCheck = false;
    }
    ;
  pygraphviz = buildPythonPackage {
      name = "pygraphviz-1.3.1";
      src = fetchurl {
        url = "https://pypi.python.org/packages/98/bb/a32e33f7665b921c926209305dde66fe41003a4ad934b10efb7c1211a419/pygraphviz-1.3.1.tar.gz";
        sha256 = "7c294cbc9d88946be671cc0d8602aac176d8c56695c0a7d871eadea75a958408";
      };
      format = "setuptools";
      buildInputs = [ graphviz pkgconfig ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  pyyaml = buildPythonPackage {
      name = "pyyaml-3.12";
      src = fetchurl {
        url = "https://pypi.python.org/packages/4a/85/db5a2df477072b2902b0eb892feb37d88ac635d36245a72a6a69b23b383a/PyYAML-3.12.tar.gz";
        sha256 = "592766c6303207a20efc445587778322d7f73b161bd994f227adaa341ba212ab";
      };
      format = "setuptools";
      buildInputs = [ libyaml ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  requests = buildPythonPackage {
      name = "requests-2.13.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/7e/ac/a80ed043485a3764053f59ca92f809cc8a18344692817152b0e8bd3ca891/requests-2.13.0-py2.py3-none-any.whl";
        sha256 = "1a720e8862a41aa22e339373b526f508ef0c8988baf48b84d3fc891a8e237efb";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  traits = buildPythonPackage {
      name = "traits-4.6.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/56/47/03f50e82e1ff1e8a602c5f2cf12f08675f79a7169629fe4ce521e59d265f/traits-4.6.0.tar.bz2";
        sha256 = "c71c3165526e5375f74358968fd70a258a65d6c8768210ee4e4f88347a4ab853";
      };
      format = "setuptools";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  

}