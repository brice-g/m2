import argparse
import json
import hashlib
from datetime import datetime
from pathlib import Path
import pandas as pd
from loguru import logger

# Import des fonctions de nettoyage
from .clean import (
    drop_duplicates,
    normalise_text,
    handle_missing,
    flag_length_outliers,
    drop_invalid_rows
)
from .anonymize import anonymize_data

def compute_hash(file_path):
    """Calcule le hash SHA256 d'un fichier."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def run_pipeline(input_path: str, output_path: str):
    start_time = datetime.now()
    input_p = Path(input_path)
    output_p = Path(output_path)
    
    # Création du dossier de sortie si inexistant
    output_p.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Démarrage du pipeline. Fichier source : {input_path}")

    # 1. Chargement
    df = pd.read_json(input_path, lines=True)
    initial_stats = {
        "count": len(df),
        "hash_raw": compute_hash(input_path)
    }

    # 2. Enchaînement des étapes
    df = handle_missing(df)
    df = normalise_text(df)
    df = drop_invalid_rows(df)
    df = drop_duplicates(df)
    df = flag_length_outliers(df)
    
    # 3. Anonymisation (Regex + NER)
    df = anonymize_data(df)

    # 4. Sauvegarde du fichier nettoyé
    df.to_json(output_path, orient='records', lines=True, force_ascii=False)
    logger.success(f"Fichier nettoyé sauvegardé : {output_path}")

    # 5. Génération des métadonnées
    meta_path = output_p.with_suffix('.meta.json')
    metadata = {
        "pipeline_execution_date": start_time.isoformat(),
        "input_file": str(input_p.name),
        "output_file": str(output_p.name),
        "parameters": {
            "min_length_threshold": 10,
            "ner_model": "fr_core_news_lg"
        },
        "stats": {
            "rows_before": initial_stats["count"],
            "rows_after": len(df),
            "rows_removed": initial_stats["count"] - len(df),
            "outliers_detected": int(df['is_length_outlier'].sum())
        },
        "hashes": {
            "input_sha256": initial_stats["hash_raw"],
            "output_sha256": compute_hash(output_path)
        }
    }

    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)
    
    logger.success(f"Métadonnées générées : {meta_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline de nettoyage FastIA")
    parser.add_argument("--input", type=str, required=True, help="Chemin vers le dataset JSONL brut")
    parser.add_argument("--output", type=str, required=True, help="Chemin vers le dataset JSONL nettoyé")
    
    args = parser.parse_args()
    
    try:
        run_pipeline(args.input, args.output)
    except Exception as e:
        logger.exception(f"Échec du pipeline : {e}")