#!/bin/bash

# Script to run all CI checks locally
set -e

echo "🔍 Running CI checks locally..."

echo "📝 Type checking with mypy..."
mypy src/meddra_loader --ignore-missing-imports --strict-optional

echo "🔍 Linting with pylint..."
pylint src/meddra_loader --disable=missing-docstring,too-few-public-methods,invalid-name,redefined-outer-name

echo "🎨 Code style check with black..."
black --check --diff src/

echo "🧪 Running tests with pytest and coverage..."
pytest src/meddra_loader/tests/ --cov=src/meddra_loader --cov-report=xml --cov-report=term

echo "✅ All CI checks passed!"
