{ nixpkgs, pynix, }:
let
  inherit (pynix) lib;

  layer_1 = python_pkgs:
    python_pkgs // {
      arch-lint = let
        result = import ./arch_lint.nix { inherit nixpkgs pynix python_pkgs; };
      in result."v4.0.2".pkg;
      types-simplejson = import ./simplejson/stubs.nix lib;
    };
  python_pkgs = pynix.utils.compose [ layer_1 ] pynix.lib.pythonPackages;
in { inherit lib python_pkgs; }
