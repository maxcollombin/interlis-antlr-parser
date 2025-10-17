#!/bin/sh
set -eu

echo "Configuration de l'environnement interlis-antlr-parser..."

# Vérifier et ajouter le submodule grammar si absent
if [ ! -d "grammar" ]; then
    echo "Ajout du submodule grammar..."
    git submodule add https://github.com/maxcollombin/interlis-antlr4.git grammar || true
fi

# Initialisation et mise à jour des submodules
echo "Initialisation et mise à jour des submodules..."
git submodule update --init --recursive

# Vérifier que le submodule a été correctement récupéré
if [ ! -d "grammar" ] || [ ! -f "grammar/InterlisLexer.g4" ] || [ ! -f "grammar/InterlisParser.g4" ]; then
    echo "Erreur: Submodule grammar non initialisé ou fichiers .g4 manquants"
    exit 1
fi

# Création de l'environnement virtuel
if [ ! -d "interlis-antlr4" ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv interlis-antlr4
fi

echo "Activation de l'environnement virtuel..."
. interlis-antlr4/bin/activate

if [ -z "${VIRTUAL_ENV:-}" ]; then
    echo "Erreur: L'environnement virtuel n'a pas été activé correctement"
    exit 1
fi
echo "Environnement virtuel actif: $VIRTUAL_ENV"

echo "Installation des dépendances Python..."
pip install -q antlr4-python3-runtime antlr4-tools

# Génération du code à partir des grammaires du submodule
echo "Génération des fichiers ANTLR..."
outdir="interlis_antlr_parser/grammar/generated"
mkdir -p "$outdir"
rm -rf "$outdir"/*

# Création d'un répertoire temporaire pour la copie des fichiers de grammaire
temp_dir=$(mktemp -d)
echo "Répertoire temporaire: $temp_dir"

# Copie des fichiers de grammaire dans le répertoire temporaire
cp grammar/InterlisLexer.g4 "$temp_dir/"
cp grammar/InterlisParser.g4 "$temp_dir/"


# Génération des runtime ANTLR
cd "$temp_dir"
echo "Génération du lexer..."
antlr4 -Dlanguage=Python3 InterlisLexer.g4
echo "Génération du parser..."
antlr4 -Dlanguage=Python3 InterlisParser.g4

# Retourner dans le répertoire principal
cd - > /dev/null

# Copier les fichiers générés
echo "  Copie des fichiers générés..."
cp "$temp_dir"/*.py "$outdir/"
cp "$temp_dir"/*.tokens "$outdir/"
cp "$temp_dir"/*.interp "$outdir/"

# Nettoyage du répertoire temporaire
rm -rf "$temp_dir"

# Création de __init__.py
cat > "$outdir/__init__.py" << 'EOF'
from .InterlisLexer import InterlisLexer
from .InterlisParser import InterlisParser
from .InterlisListener import InterlisListener
__all__ = ["InterlisLexer", "InterlisParser", "InterlisListener"]
EOF

rm -rf interlis_antlr_parser.egg-info

echo "Désinstallation d'antlr4-tools (plus nécessaire)..."
pip uninstall -y antlr4-tools

echo " Setup terminé avec succès!"
echo " Environnement virtuel: interlis-antlr4"
echo " Pour l'activer: source interlis-antlr4/bin/activate"
echo "Suppression du submodule grammar..."
git submodule deinit -f grammar
git rm -f grammar
rm -rf .git/modules/grammar
rm -rf grammar
echo ""
echo " Test rapide de l'installation..."
python -c "import interlis_antlr_parser; print(' Import réussi!')" || echo " Problème d'import"
