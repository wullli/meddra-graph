#!/bin/bash

# Script to run all CI checks locally
set -e

echo "🔍 Running CI checks locally..."

echo "🎨 Code style check with black..."
black --check --diff src/

echo "📝 Type checking with mypy..."
mypy src/meddra_graph --ignore-missing-imports --strict-optional

echo "🔍 Linting with pylint..."
pylint src/meddra_graph --disable=missing-docstring,too-few-public-methods,invalid-name,redefined-outer-name

echo "🧪 Running tests with pytest and coverage..."
pytest --cov=src/meddra_graph --cov-report=xml --cov-report=term src/meddra_graph/tests/

echo "✅ All CI checks passed!"
