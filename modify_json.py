#!/usr/bin/env python3
import json
import sys
import os

code_items = []
code_blocks = []

def classify_item(name):
    if '_spawn_egg' in name:
        return 'spawn_egg'
    elif any(x in name for x in ['chestplate', 'helmet', 'leggings', 'boots']):
        return 'armor'
    elif any(x in name for x in ['sword', 'axe', 'pickaxe', 'shovel', 'hoe']):
        return 'handheld'
    else:
        return 'generated'

def modify_item_model(data, name):
    type_ = classify_item(name)
    if type_ == 'spawn_egg':
        data['parent'] = 'builtin/spawn_egg'
        if 'textures' in data:
            del data['textures']
    elif type_ == 'armor':
        data['parent'] = 'builtin/generated'
        if 'textures' in data:
            tex = data['textures'].get('layer0', '')
            if tex.startswith('jujutsucraft:item/'):
                tex = tex.replace('jujutsucraft:item/', 'minecraft:items/')
            data['textures'] = {
                'layer0': tex,
                'layer1': tex  # assume same for overlay
            }
    elif type_ == 'handheld':
        data['parent'] = 'builtin/handheld'
    else:
        data['parent'] = 'builtin/generated'
    
    if 'textures' in data:
        for key, value in data['textures'].items():
            if isinstance(value, str):
                if value.startswith('jujutsucraft:item/'):
                    data['textures'][key] = value.replace('jujutsucraft:item/', 'minecraft:items/')
                elif value.startswith('jujutsucraft:block/'):
                    data['textures'][key] = value.replace('jujutsucraft:block/', 'minecraft:blocks/')
    
    # Generate code
    global code_items
    item_name = name.replace('.json', '')
    if type_ == 'armor':
        slot = 0
        if 'helmet' in item_name:
            slot = 0
        elif 'chestplate' in item_name:
            slot = 1
        elif 'leggings' in item_name:
            slot = 2
        elif 'boots' in item_name:
            slot = 3
        code_items.append(f"registerItem({len(code_items)+434}, \"{item_name}\", (new ItemArmor(ItemArmor.ArmorMaterial.LEATHER, 0, {slot})).setUnlocalizedName(\"{item_name}\").setCreativeTab(CreativeTabs.tabCombat));")
        code_items.append(f"this.registerItem(Items.{item_name}, \"{item_name}\");")
    else:
        code_items.append(f"registerItem({len(code_items)+434}, \"{item_name}\", (new Item()).setUnlocalizedName(\"{item_name}\").setCreativeTab(CreativeTabs.tabMisc));")
        code_items.append(f"this.registerItem(Items.{item_name}, \"{item_name}\");")
    code_items.append(f"public static Item {item_name};")
    code_items.append(f"{item_name} = getRegisteredItem(\"{item_name}\");")
    
    return data

def modify_block_model(data, name):
    if 'render_type' in data:
        del data['render_type']
    if 'textures' in data:
        for key, value in data['textures'].items():
            if isinstance(value, str) and value.startswith('jujutsucraft:block/'):
                data['textures'][key] = value.replace('jujutsucraft:block/', 'minecraft:blocks/')
    
    # Generate code
    global code_blocks
    block_name = name.replace('.json', '')
    code_blocks.append(f"registerBlock({len(code_blocks)+256}, \"{block_name}\", (new Block(Material.rock)).setHardness(1.0F).setUnlocalizedName(\"{block_name}\").setCreativeTab(CreativeTabs.tabBlock));")
    code_blocks.append(f"public static Block {block_name};")
    code_blocks.append(f"{block_name} = getRegisteredBlock(\"{block_name}\");")
    
    return data

def modify_blockstate(data, name):
    if 'variants' in data:
        for variant, props in data['variants'].items():
            if 'model' in props and props['model'].startswith('jujutsucraft:block/'):
                props['model'] = props['model'].replace('jujutsucraft:block/', 'minecraft:block/')
    return data

def json_to_lang(data):
    lines = []
    for key, value in data.items():
        lines.append(f"{key}={value}")
    return '\n'.join(lines)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python modify_json.py <type> <input_file> <output_file>")
        sys.exit(1)
    type_ = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    if type_ == 'item':
        name = os.path.basename(input_file)
        data = modify_item_model(data, name)
    elif type_ == 'block':
        name = os.path.basename(input_file)
        data = modify_block_model(data, name)
    elif type_ == 'blockstate':
        data = modify_blockstate(data)
    elif type_ == 'lang':
        content = json_to_lang(data)
        with open(output_file, 'w') as f:
            f.write(content)
        sys.exit(0)
    
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    # Write code to file
    with open('generated_code.txt', 'w') as f:
        f.write("// Items\n")
        for line in code_items:
            f.write(line + '\n')
        f.write("// Blocks\n")
        for line in code_blocks:
            f.write(line + '\n')