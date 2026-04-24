#!/usr/bin/env python3
import json
import sys
import os

def modify_item_model(data):
    if 'parent' in data:
        parent = data['parent']
        if parent == 'item/generated':
            data['parent'] = 'builtin/generated'
        elif parent == 'item/handheld':
            data['parent'] = 'builtin/handheld'
        elif parent == 'item/template_spawn_egg':
            data['parent'] = 'builtin/spawn_egg'
        elif parent.startswith('jujutsucraft:'):
            data['parent'] = 'builtin/generated'
    if 'textures' in data:
        for key, value in data['textures'].items():
            if isinstance(value, str):
                if value.startswith('jujutsucraft:item/'):
                    data['textures'][key] = value.replace('jujutsucraft:item/', 'minecraft:items/')
                elif value.startswith('jujutsucraft:block/'):
                    data['textures'][key] = value.replace('jujutsucraft:block/', 'minecraft:blocks/')
    return data

def modify_block_model(data):
    if 'render_type' in data:
        del data['render_type']
    if 'textures' in data:
        for key, value in data['textures'].items():
            if isinstance(value, str) and value.startswith('jujutsucraft:block/'):
                data['textures'][key] = value.replace('jujutsucraft:block/', 'minecraft:blocks/')
    return data

def modify_blockstate(data):
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
        data = modify_item_model(data)
    elif type_ == 'block':
        data = modify_block_model(data)
    elif type_ == 'blockstate':
        data = modify_blockstate(data)
    elif type_ == 'lang':
        content = json_to_lang(data)
        with open(output_file, 'w') as f:
            f.write(content)
        sys.exit(0)
    
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)