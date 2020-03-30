# Extract translatable messages into .pot files
make gettext

# Generate .po files. Generated .po files will be placed:
sphinx-intl update -p _build/gettext -l ko

# Now, translate with .po files
