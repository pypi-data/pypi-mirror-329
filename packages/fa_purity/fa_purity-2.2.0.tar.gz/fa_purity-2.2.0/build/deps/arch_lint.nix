{ nixpkgs, pynix, python_pkgs }:
let
  make_bundle = commit: sha256:
    let
      raw_src = builtins.fetchTarball {
        inherit sha256;
        url =
          "https://gitlab.com/dmurciaatfluid/arch_lint/-/archive/${commit}/arch_lint-${commit}.tar";
      };
      src = import "${raw_src}/build/filter.nix" nixpkgs.nix-filter raw_src;
      bundle = import "${raw_src}/build" {
        inherit nixpkgs pynix src;
        scripts = { run-lint = [ ]; };
      };
      extented_python_pkgs = python_pkgs // {
        inherit (bundle.deps.python_pkgs) grimp;
      };
    in bundle.buildBundle {
      pkgDeps = bundle.requirements extented_python_pkgs;
    };
in {
  "v4.0.2" = make_bundle "c2306821288b424a2c25c795904b2bdfc3be2b6d"
    "083sjd5zslfxyg8zb9f0rzcg15wsj9k1wb9b2pgs0y9f41l4kfiy";
}
