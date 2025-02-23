#!/bin/zsh
# SAIS Prism Standardized Build & Release Script
# Complies with modular architecture (client/models/training/deployment/utils) 
# and dependency management requirements

rm -rf dist/* build/* *.egg-info artifacts/*

# Install core build toolchain (layered requirements)
python -m pip install setuptools wheel twine==6.0.1 

# Enforce code quality gates (mandatory black + flake8 checks)
black --check . 
black .
flake8 .

# Build distribution packages
python setup.py sdist bdist_wheel

# Validate package integrity
twine check dist/*

# Deploy to PyPI (requires pre-configured credentials)
# Security: Uses API token authentication (never hardcode credentials)
twine upload dist/*
