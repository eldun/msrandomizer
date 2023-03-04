import os
import shutil
import random
import argparse

MAX_SIZE = 1024 ** 3  # 1 GiB in bytes


def main():
    parser = argparse.ArgumentParser(description='Copy random audio files to folders.')    
    parser.add_argument('sources', nargs='+', help='the source folder(s) to select audio files from')
    parser.add_argument('destination', help='the destination folder to create sub-folders in')
    parser.add_argument('num_folders', type=int, help='the number of folders to create')
    args = parser.parse_args()

    # create destination folder if it doesn't exist
    os.makedirs(args.destination, exist_ok=True)

    cumulative_size = 0
    for i in range(args.num_folders):
        folder_name = hex(i)[2:].zfill(2)  # convert to hex and zero-pad to 2 digits
        folder_path = os.path.join(args.destination, folder_name)
        os.mkdir(folder_path)

        files = []
        for source in args.sources:
            for root, _, filenames in os.walk(source):
                for filename in filenames:
                    if filename.endswith('.mp3') or filename.endswith('.wav'):
                        files.append(os.path.join(root, filename))

        if len(files) < 6:
            print(f"Not enough audio files found for folder {folder_name}.")
            shutil.rmtree(folder_path)
            break

        folder_size = 0
        selected_files = random.sample(files, 6)
        for file_path in selected_files:
            file_size = os.path.getsize(file_path)
            if cumulative_size + folder_size + file_size > MAX_SIZE:
                print(f"Folder {folder_name} exceeds 1 GiB. Deleting folder.")
                shutil.rmtree(folder_path)
                return

            relative_path = os.path.relpath(file_path, args.sources[0])[-40:]
            dest_path = os.path.join(folder_path, os.path.basename(file_path))
            shutil.copy2(file_path, dest_path)
            folder_size += file_size
            cumulative_size += file_size

            print(f"{relative_path:40} {folder_name} {cumulative_size / (1024 ** 2):10.2f} MiB copied so far.")

if __name__ == '__main__':
    main()
