{
  description = "AGS dev flake";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils }:
  flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs {
        inherit system;
        config = {
          allowUnfree = true;
        };
      };
    in
      {
        devShell = pkgs.mkShell {
          buildInputs =  with pkgs; [
            # (boost.override { 
            #   enableShared = true;
            #   enableStatic = true;
            # })
            # clang-tools
            # bear
            # binutils
            # cmake
            # gnumake




            (python3.withPackages (py-pkgs: [
              py-pkgs.numpy
              py-pkgs.pandas

              py-pkgs.python-lsp-server
              py-pkgs.python-lsp-black
              py-pkgs.python-lsp-ruff
            ]))

          ];
        };
    });
}



