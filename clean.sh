#!/bin/sh

# Script de nettoyage complet pour interlis-antlr-parser
# Supprime tous les fichiers intermédiaires et temporaires

echo " Nettoyage du projet interlis-antlr-parser..."

# Désactivation de l'environnement virtuel si actif
if [ -n "$VIRTUAL_ENV" ]; then
    echo " Désactivation de l'environnement virtuel..."
    deactivate || echo " (déjà désactivé ou non interactif)"
fi

# Fonction de suppression sécurisée
safe_remove() {
    if [ -e "$1" ]; then
        echo "    Suppression: $1"
        rm -rf "$1"
    else
        echo "    Déjà supprimé: $1"
    fi
}

# Suppression des fichiers de grammaire ANTLR générés (dans le dossier generated)
echo ""
echo " Suppression des fichiers de grammaire ANTLR générés dans interlis_transcoder/grammar/generated/..."
safe_remove "interlis_transcoder/grammar/generated/.antlr"
safe_remove "interlis_transcoder/grammar/generated/__pycache__"
safe_remove "interlis_transcoder/grammar/generated/InterlisLexer.py"
safe_remove "interlis_transcoder/grammar/generated/InterlisParser.py"
safe_remove "interlis_transcoder/grammar/generated/InterlisParserListener.py"
safe_remove "interlis_transcoder/grammar/generated/InterlisParser.tokens"
safe_remove "interlis_transcoder/grammar/generated/InterlisLexer.tokens"
safe_remove "interlis_transcoder/grammar/generated/InterlisLexer.interp"
safe_remove "interlis_transcoder/grammar/generated/InterlisParser.interp"
safe_remove "interlis_transcoder/grammar/generated/__init__.py"

# Suppression des caches Python
echo ""
echo " Suppresson des caches Python..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true

# Suppression de l'environnement virtuel    
echo ""
echo " Suppression de l'environnement virtuel..."
safe_remove "interlis-antlr4"

# Suppression des fichiers de build et distribution
echo ""
echo " Suppression des fichiers de build..."
safe_remove "*.egg-info"
safe_remove "interlis_antlr_parser.egg-info"

echo "Nettoyage terminé."