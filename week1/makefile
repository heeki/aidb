.PHONY: backend.venv backend.install backend.run frontend.install frontend.run dev

# Backend
backend.venv:
	cd backend && uv venv .venv

backend.install: backend.venv
	cd backend && uv pip install -r requirements.txt

backend.run:
	backend/.venv/bin/uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Frontend
frontend.install:
	. $(HOME)/.nvm/nvm.sh && cd frontend && npm install

frontend.run:
	. $(HOME)/.nvm/nvm.sh && cd frontend && npm run dev

# Run both backend and frontend concurrently
dev:
	$(MAKE) backend.run & $(MAKE) frontend.run & wait
