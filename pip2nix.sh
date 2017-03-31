#!/usr/bin/env nix-shell
#!nix-shell -i bash shell.nix

pip2nix \
    -r requirements.open \
    -i pygraphviz graphviz,pkgconfig \
    -s munch six
