{pkgs ? import ./nixpkgs.nix
, buildInputNames ? ""
}:

let

  inherit (pkgs.lib)
    getAttr
    optional
    hasAttr
    hasPrefix
    fileContents
    filter
    splitString
    stringLength

    traceShowVal
    ;

  python = pkgs.python.withPackages (ps: with ps; [virtualenv pip]);
  buildInputs = optional (stringLength buildInputNames > 0) (
    map (name: getAttr name pkgs) (splitString " " buildInputNames)
  );
in

pkgs.stdenv.mkDerivation {
  name = "python-bare";
  buildInputs = [python pkgs.dateutils pkgs.cacert] ++ buildInputs;
  shellHook = ''
    export SOURCE_DATE_EPOCH=$(date +%s)
    export SSL_CERT_FILE=${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt
  '';
}
