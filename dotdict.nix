{ buildPythonPackage
, fetchPypi
, ...
}:

buildPythonPackage rec {
  pname = "dotdict";
  version = "0.1";
  name = "${pname}-${version}";
  src = fetchPypi {
    inherit pname version;
    sha256 = "0nxpar3b0p099j6wlxaklabwaw3bcxsx7l4zyyqcqiic3r61vira";
  };
}
