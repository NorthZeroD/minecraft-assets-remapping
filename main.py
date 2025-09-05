import os
from remapping_symlink import *
from remapping_copy import *
from versions import *

def main():

    minecraft_dir_path = input('Enter the path to your Minecraft folder\ne.g. C:/Users/YourName/AppData/Roaming/.minecraft\nEnter with empty to set as \'.minecraft\'\n') or '.minecraft'
    if not os.path.isdir(minecraft_dir_path):
        print('The provided path is not a valid directory.')
        return
    assets_dir_path = os.path.join(minecraft_dir_path, 'assets')
    if not os.path.isdir(assets_dir_path):
        print('The assets folder does not exist in the provided Minecraft directory.')
        return
    objects_dir_path = os.path.join(assets_dir_path, 'objects')
    if not os.path.isdir(objects_dir_path):
        print('The objects folder does not exist in the assets directory.')
        return
    indexes_dir_path = os.path.join(assets_dir_path, 'indexes')
    if not os.path.isdir(indexes_dir_path):
        print('The indexes folder does not exist in the assets directory.')
        return

    index_files = [f for f in os.listdir(indexes_dir_path) if os.path.isfile(os.path.join(indexes_dir_path, f))]

    if not index_files:
        print(f'No index files found in {indexes_dir_path}. Please download Minecraft versions in your launcher first.')
        return

    order_map = {k: i for i, k in enumerate(VERSIONS.keys())}
    index_files.sort(key=lambda f: order_map.get(f[:-5], float("inf")))
    print('Select an index file:')
    for f in index_files:
        print(f'{f} - {VERSIONS[f[:-5]] if f[:-5] in VERSIONS else 'Unknown version'}')
    selected_file = input('Enter the filename (e.g. 27.json): ')
    if selected_file not in index_files:
        print('The selected file does not exist in the indexes directory.')
        return

    output_dir = input(f'Enter the output directory (default: ./output/{selected_file[:-5]}/assets): ') or f'./output/{selected_file[:-5]}/assets'
    if os.path.exists(output_dir):
        print('The output directory already exists. Please choose a different directory or remove the existing one.')
        return

    output_mode = input('Select output mode:\nc - copy files\ns - create symlinks\nEnter with empty to set as default [c]: ').lower() or 'c'
    if output_mode == 'c':
        remapping_copy(os.path.join(indexes_dir_path, selected_file),
                       objects_dir_path,
                       output_dir)
    elif output_mode == 's':
        remapping_symlink(os.path.join(indexes_dir_path, selected_file),
                  objects_dir_path,
                  output_dir)
    else:
        print('Invalid mode selected. Please enter "c" for copy or "s" for symlink.')
        return
    
    print('Remapping completed. Output directory:', output_dir)
    
if __name__ == '__main__':
    main()
