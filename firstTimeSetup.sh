#!/bin/bash
set -xeuf -o pipefail

rm -rf venv

python3.6 -m venv venv

source venv/bin/activate
source environment

pip install --upgrade pip