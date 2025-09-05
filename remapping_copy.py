import json
import os
import shutil

def remapping_copy(index_file_path, objects_dir_path, output_dir_path):
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)
        
    with open(index_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
        with open(os.path.join(output_dir_path[:-7], 'output.log'), 'w', encoding='utf-8') as log:
            
            for k, v in data['objects'].items():
                hash = v['hash']
                subdir = hash[:2]
                source = os.path.join(objects_dir_path, subdir, hash)
                target = os.path.join(output_dir_path, k)
                target_dir = os.path.dirname(target)

                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                    log.write(f"Created directory: {target_dir}\n")
                if os.path.exists(source):
                    if not os.path.exists(target):
                        shutil.copy2(source, target)
                        print(f"Copied file: {target} <- {source}")
                        log.write(f"Copied file: {target} <- {source}\n")
                    else:
                        print(f"File already exists: {target}")
                        log.write(f"File already exists: {target}\n")
                else:
                    print(f"Source file does not exist: {source}")
                    log.write(f"Source file does not exist: {source}\n")

if __name__ == "__main__":
    remapping_copy('.minecraft/assets/indexes/27.json',
                   '.minecraft/assets/objects',
                   './assets')
