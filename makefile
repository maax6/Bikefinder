# Makefile pour le scraper moto

.PHONY: install run export clean venv

# 1. Crée un environnement virtuel et installe les dépendances
install: venv
	@echo "📦 Installation des dépendances..."
	.venv/bin/pip install -r requirements.txt

# 2. Crée le venv s'il n'existe pas
venv:
	@if [ ! -d ".venv" ]; then \
		echo "🧪 Création de l'environnement virtuel..."; \
		python3 -m venv .venv; \
		.venv/bin/python -m ensurepip --upgrade; \
	fi

# 3. Lance le script principal avec le venv
run:
	@echo "🏃 Lancement du scraper..."
	.venv/bin/python scrapeUrlByYear.py

# 4. Export CSV (à compléter plus tard)
export:
	@echo "📤 Export non implémenté. Ajoute un module export_csv.py ;)"

# 5. Nettoie l’environnement (efface le venv)
clean:
	@echo "🧹 Suppression du venv..."
	rm -rf .venv
