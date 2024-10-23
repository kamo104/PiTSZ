{
  description = "AGS dev flake";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    # firefox.url = "github:nix-community/flake-firefox-nightly";
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

            # llvmPackages_17
            boost
            clang-tools
            bear
            binutils
            cmake
            gnumake

          ];
        };
    });
}



