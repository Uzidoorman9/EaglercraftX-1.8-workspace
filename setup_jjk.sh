#!/bin/bash

# Copy all textures
cp -r jjkassets/assets/jujutsucraft/textures/* desktopRuntime/resources/assets/minecraft/textures/

# Copy and modify item models
for file in jjkassets/assets/jujutsucraft/models/item/*.json; do
    base=$(basename "$file")
    python3 modify_json.py item "$file" "desktopRuntime/resources/assets/minecraft/models/item/$base"
done

# Copy and modify block models
for file in jjkassets/assets/jujutsucraft/models/block/*.json; do
    base=$(basename "$file")
    python3 modify_json.py block "$file" "desktopRuntime/resources/assets/minecraft/models/block/$base"
done

# Copy and modify blockstates
for file in jjkassets/assets/jujutsucraft/blockstates/*.json; do
    base=$(basename "$file")
    python3 modify_json.py blockstate "$file" "desktopRuntime/resources/assets/minecraft/blockstates/$base"
done

# Convert and append lang
python3 modify_json.py lang jjkassets/assets/jujutsucraft/lang/en_us.json temp_lang.txt
cat temp_lang.txt >> desktopRuntime/resources/assets/minecraft/lang/en_US.lang
rm temp_lang.txt

echo "Setup complete."