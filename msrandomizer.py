import argparse
import os, shutil, random, re, sys


KIT_COUNT = 25
KIT_SIZE = 6
MAX_ATTEMPTS = 25
MAX_TRANSFER_LIMIT_IN_BYTES = 1024*1024*1024 * .98 # 98% of 1 GiB



def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Create seqeuntially named directories - each containing six random audio files(.wav, .mp3, .aiff) collated from the provided source directories')

    parser.add_argument('sources', nargs='+')
    parser.add_argument('dest', nargs=1)
    parser.add_argument('--kits', '-k', 
                        nargs='?', 
                        type=int, 
                        default=KIT_COUNT, 
                        help='The number of output folders(\'kits\') to create. Default: ' + str(KIT_COUNT))
    return parser


def remove_leading_non_alphanumeric_characters(input_string):
    return re.sub(r'^[^a-zA-Z0-9]*', '', input_string)



def generate_kits(args) -> None:
    random_source = lambda: random.choice(args.sources)
    dest = args.dest[0]
    kit_count = args.kits

    current_kit_label = 0
    cumulative_size = 0


    for kit in range(kit_count):

        if cumulative_size > MAX_TRANSFER_LIMIT_IN_BYTES:
            exit_string = str.format('Max transfer size({} GiB) reached', cumulative_size/1024.0/1024.0/1024.0)
            sys.exit(exit_string)
        
        attempts = 0
        samples_added = 0
        kit_folder = f'{current_kit_label:x}'
        output_folder = os.path.join(dest, kit_folder)

        if os.path.isdir(output_folder):
            shutil.rmtree(output_folder)
    

        os.mkdir(output_folder)

        while samples_added < KIT_SIZE:

            source = random_source() # Randomly choose a new source dir each iteration

            # Build list of files
            audio_files = []
            for path, subdirs, files in os.walk(source):
                for file in files:


                    # Only grab audio files
                    if file.lower().endswith(('.wav', '.mp3', '.aiff')):
                        audio_files.append(os.path.join(path, file))

            random_file_path = random.choice(audio_files)
            random_file = os.path.basename(random_file_path)

            root, ext =  os.path.splitext(random_file)

            

            renamed_output_file = remove_leading_non_alphanumeric_characters(root)

            # Add 1-6 suffix to accomodate how the Model:Samples loads kits
            renamed_output_file = f"{renamed_output_file}-{samples_added+1}{ext}"
            
            renamed_output_file_path = os.path.join(output_folder, renamed_output_file)
            shutil.copy(random_file_path, os.path.join(output_folder, renamed_output_file))

            cumulative_size += os.path.getsize(random_file_path)
            cumulative_size_string = '{:.2f} {}'.format(cumulative_size/1024.0/1024.0, 'MiB copied')

            # Columnated console output
            renamed_output_file = f'\'{renamed_output_file}\'' # You can't put backslashes inside of f-string braces, so I inserted them here
            print(f'{random_file_path:<100} copied to \'{kit_folder}\' {"":<10}as {renamed_output_file:<30}  {cumulative_size_string:>30}'  )

            samples_added += 1


        print('\n')
        current_kit_label = current_kit_label + 1


if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()
    print(args)
    generate_kits(args)

