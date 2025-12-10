import argparse
import asyncio
import pandas as pd
from googletrans import Translator


async def translate_column(series, translator, src="en", dest="es", batch_size=50):
    """
    Translate a pandas Series using batching + dedup (async version).
    """
    # Work on a copy to avoid SettingWithCopyWarning
    series = series.copy()

    mask = series.notna()
    non_na = series[mask]

    unique_texts = non_na.unique().tolist()
    translations = {}

    print(f"  Unique strings to translate: {len(unique_texts)}")

    for i in range(0, len(unique_texts), batch_size):
        chunk = unique_texts[i : i + batch_size]
        try:
            res = await translator.translate(chunk, src=src, dest=dest)

            # googletrans returns a single object if len(chunk) == 1
            if not isinstance(res, list):
                res = [res]

            for orig, r in zip(chunk, res):
                translations[orig] = r.text
        except Exception as e:
            print(f"  Batch {i // batch_size} failed: {e}")
            # Fallback: keep originals
            for orig in chunk:
                translations[orig] = orig

    translated_non_na = non_na.map(translations)
    series[mask] = translated_non_na
    return series


async def main_async(input_file, output_file):
    df = pd.read_csv(input_file)
    translator = Translator()

    caption_cols = ["caption_0", "caption_1", "caption_2", "caption_3"]

    for col in caption_cols:
        if col in df.columns:
            print(f"Translating column: {col}")
            df[col] = await translate_column(df[col], translator)
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
    asyncio.run(main_async(args.input_csv, args.output_csv))
