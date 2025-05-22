import polars as pl
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
import time
import torch

df = pl.read_parquet("compare-20250513.parquet")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M").to(device)
tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")


def translate(text, model, tokenizer, source_lang="en", target_lang="zh") -> str:
    tokenizer.src_lang = source_lang
    encoded_text = tokenizer(text, return_tensors="pt").to(device)
    generated_tokens = model.generate(
        **encoded_text,
        forced_bos_token_id=tokenizer.get_lang_id(target_lang)
    )
    return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]


translated_rows = []
total_time = 0
total_rows = len(df)

print(f"start {total_rows} rows...")
start_total = time.time()

for i, row in enumerate(df.iter_rows(named=True)):
    start_time = time.time()
    result = translate(row["before"], model, tokenizer, "en", "zh")
    end_time = time.time()

    translation_time = end_time - start_time
    total_time += translation_time

    new_row = dict(row)
    new_row["m2m100"] = result
    new_row["translation_time"] = translation_time
    translated_rows.append(new_row)

    if (i + 1) % 10 == 0 or i == total_rows - 1:
        avg_time = total_time / (i + 1)
        print(f" {i+1}/{total_rows} rows ({(i+1)/total_rows*100:.1f}%), avg: {avg_time:.2f}s")

end_total = time.time()
total_elapsed = end_total - start_total

print(f"\nfinished!")
print(f"total time: {total_elapsed:.2f}s")
print(f"avg time: {total_time/total_rows:.2f}s")

new_df = pl.DataFrame(translated_rows)
print(new_df)
new_df.write_parquet("m2m100.parquet")
