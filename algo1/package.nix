{pkgs}:
pkgs.stdenv.mkDerivation rec {
  pname = "alg1";
  version = "0.1.0";

  src = pkgs.fetchFromGithub {
    owner = "kamo104";
    repo = "PiTSZ";
    rev = "eecbfedac48f827e96ad5e151de8f41f6cd3af66";
    sha256 = "0rs9bxxrw4wscf4a8yl776a8g880m5gcm75q06yx2cn3lw2b7v22";
  };

  buildInputs = with pkgs; [
    boost
    cmake
  ];

  configurePhase = ''
    cmake . -B build -DCMAKE_RELEASE_TYPE=Release
  '';

  buildPhase = ''
    cd build &&  make -j$(nproc)
  '';

  installPhase = ''
    mkdir -p $out/bin
    mv build/{verifer,generator,solution} $out/bin/
    # mv build/generator $out/bin/
    # mv build/solution $out/bin/
  '';
}
