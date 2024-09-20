# -- To translate every PO file under LC_MESSAGES directory:
# find /path/to/LC_MESSAGES -name "*.po" -type f | xargs -I {} sh -c 'python translate_po.py "{}" "{}"'

import argparse
import polib
from openai import OpenAI

import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


target_language = "Japanese"
# llm_model = "gpt-4o-mini"
llm_model = "gpt-4o-2024-08-06"
prompt_template = (
    "You are tasked with translating Lablup's Backend.AI Web UI manual. "
    "The text is formatted in reStructuredText. Please translate the following "
    f"text into {target_language} exactly as written, without adding any extra "
    "information. Follow these rules:\n\n"
    "- If the text contains a URL, simply translate it without accessing or modifying the link.\n"
    "- For inline code wrapped in double backticks (``):\n"
    "  + Ensure there is a space before the opening backticks and after the closing backticks.\n"
    "  + Do not add space immediately after the opening backticks or immediately before the closing backticks.\n"
    "  + Example: ' ``code`` ' is correct, but ' `` code `` ' is not.\n"
    "- For links that start with ` and end with `_:\n"
    "  + Add a space before the opening backtick and after the closing `_.\n"
    "  + Do not add space immediately after the opening backtick or immediately before the closing `_.\n"
    "  + Example: ' `link`_ ' is correct, but ' ` link `_ ' is not.\n"
    "- For references in the format :ref:`reference-name<reference-id>`:\n"
    "  + Add a space before :ref: and after the closing backtick.\n"
    "  + Do not add space immediately after :ref: or immediately before the closing backtick.\n"
    "  + Example: ' :ref:`reference-name<reference-id>` ' is correct, but ' :ref: `reference-name<reference-id> ` ' is not.\n"
)


def translate_text(text, target_language):
    response = client.chat.completions.create(
        model=llm_model,
        messages=[
            {
                "role": "system",
                "content": prompt_template,
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
