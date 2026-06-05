# Startup Data Collector

Ce projet collecte des donnees sur les startups et les investisseurs a partir d'une URL.

## Installation

```bash
pip install -r requirements.txt
```

Copier `.env.example` vers `.env`, puis ajouter la cle OpenRouter :

```env
OPENROUTER_API_KEY=your_key
```

## Utilisation

```bash
python main.py
```

Le programme va :

1. demander une URL ;
2. recuperer le contenu de la page ;
3. sauvegarder le contenu brut dans `raw_data/` ;
4. nettoyer et decouper le texte ;
5. detecter le type d'entite ;
6. extraire les donnees avec le LLM ;
7. sauvegarder le resultat dans `extracted_json/`.
