# Installation:
# - For systems without CUDA: make install
# - For systems with CUDA: make install-cuda

.PHONY: install
install:
	@echo "🚀 Creating virtual environment"
	@uv sync

.PHONY: install-cuda
install-cuda:
	@echo "🚀 Creating virtual environment with Cuda"
	@uv sync
	@uv pip install ".[cuda]"

.PHONY: check
check:
	@echo "🚀 Running Ruff for linting..."
	uv run ruff check .
	@echo "🚀 Running MyPy for type checking..."
	uv run mypy --strict .

.PHONY: run
run: check
	uv run app
	
.PHONY: clean
clean: 
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@rm -rf src/project_template.egg-info
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
