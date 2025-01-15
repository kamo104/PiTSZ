#/usr/bin/env bash

echo -n {50..500..50} | tr ' ' '\n' | xargs -I '{}' python algo3/pajton.py --program verifier instances3/in_"$1"_'{}'.txt wynikowe3/out_'{}'
