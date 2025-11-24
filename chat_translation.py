import pandas as pd
from googletrans import Translator
import argparse

def translate_column(series, translator, src='en', dest='es', batch_size=50):
    """Translate a pandas Series using batching + dedup."""
    # Keep NaNs as-is
    mask = series.notna()
    non_na = series[mask]

    # Work on unique values only
    unique_texts = non_na.unique().tolist()
    translations = {}

    print(f"  Unique strings to translate: {len(unique_texts)}")

    for i in range(0, len(unique_texts), batch_size):
        chunk = unique_texts[i : i + batch_size]
        try:
            # googletrans supports list input for batching
            res = translator.translate(chunk, src=src, dest=dest)

            # When len(chunk) == 1, googletrans returns a single object
            if not isinstance(res, list):
                res = [res]

            for orig, r in zip(chunk, res):
                translations[orig] = r.text
        except Exception as e:
            print(f"  Batch {i//batch_size} failed: {e}")
            # Fallback: keep originals for this chunk
            for orig in chunk:
                translations[orig] = orig

    # Map back to the original Series
    translated_non_na = non_na.map(translations)
    series.loc[mask] = translated_non_na
    return series


def main(input_file, output_file):
    # Load CSV
    df = pd.read_csv(input_file)

    translator = Translator()

    caption_cols = ["caption_0", "caption_1", "caption_2", "caption_3"]

    for col in caption_cols:
        if col in df.columns:
            print(f"Translating column: {col}")
            df[col] = translate_column(df[col], translator)
        else:
            print(f"Warning: column '{col}' not found in input CSV")

    df.to_csv(output_file, index=False)
    print(f"Saved translated CSV to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Translate caption columns from English to Spanish."
    )
    parser.add_argument("input_csv", help="Path to input CSV")
    parser.add_argument("output_csv", help="Path to save translated CSV")

    args = parser.parse_args()
    main(args.input_csv, args.output_csv)
