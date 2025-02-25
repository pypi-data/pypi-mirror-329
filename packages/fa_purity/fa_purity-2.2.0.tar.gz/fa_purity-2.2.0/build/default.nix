{ nixpkgs, pynix, src, scripts, }:
let
  deps = import ./deps { inherit nixpkgs pynix; };
  requirements = python_pkgs: {
    runtime_deps = with python_pkgs; [
      deprecated
      more-itertools
      simplejson
      types-deprecated
      types-simplejson
    ];
    build_deps = with python_pkgs; [ flit-core ];
    test_deps = with python_pkgs; [ arch-lint mypy pytest pylint ruff ];
  };
  buildBundle = { pkgDeps }: pynix.stdBundle { inherit pkgDeps src; };
  bundle = buildBundle { pkgDeps = requirements deps.python_pkgs; };
  devShell = (pynix.vscodeSettingsShell {
    pythonEnv = bundle.env.dev;
    extraPackages = [ scripts.run-lint ];
  }).shell;
in bundle // { inherit deps buildBundle requirements devShell; }
