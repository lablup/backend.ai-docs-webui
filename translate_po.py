# -- To translate every PO file under LC_MESSAGES directory:
# find /path/to/LC_MESSAGES -name "*.po" -type f | xargs -I {} sh -c 'python translate_po.py "{}" "{}"'

import argparse
import polib
from openai import OpenAI

import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


target_language = "Thailand language"
llm_model = "gpt-4o-mini"


def translate_text(text, target_language):
    response = client.chat.completions.create(
        model=llm_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a translator of Lablup's Backend.AI Web UI manual. "
                    "Note that the manual text or sentence is written as restructuredText format. "
                    f"Translate the following text to {target_language}. "
                    "Translate the text as-is without attaching any additional information"
                ),
            },
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content.strip()


def translate_po_file(input_file, output_file):
    po = polib.pofile(input_file)

    for entry in po:
        if entry.msgstr == "" or "fuzzy" in entry.flags:
            print(f"---\nTranslating: {entry.msgid}")
            entry.msgstr = translate_text(entry.msgid, target_language)
            print(f"Translated: {entry.msgstr}")

    po.save(output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PO translator")
    parser.add_argument("input_file", help="Input PO file path")
    parser.add_argument("output_file", help="Output PO file path")

    args = parser.parse_args()

    translate_po_file(args.input_file, args.output_file)
