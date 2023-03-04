import argparse
import os, shutil, random, sys


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
            if attempts > MAX_ATTEMPTS:
                exit_string = str.format('The maximum number of attempts({}) for creating a kit has been reached.', MAX_ATTEMPTS)
                sys.exit(exit_string)

            source = random_source() # Randomly choose a new source dir each iteration

            # Pick random file
            files = [os.path.join(path, filename)
                for path, dirs, files in os.walk(source)
                for filename in files]
            random_file = random.choice(files)

            # Only grab audio files
            if (os.path.isfile(random_file) and 
                random_file.lower().endswith(('.wav', '.mp3', '.aiff'))):

                shutil.copy(random_file, output_folder)

                copied_string = os.path.basename(random_file) + ' copied to ' + kit_folder
                cumulative_size += os.path.getsize(random_file)
                cumulative_size_string = '{:.2f} {}'.format(cumulative_size/1024.0/1024.0, 'MiB copied')

                # Columnated console output
                print(f'{copied_string:<50}{"":<10}{cumulative_size_string:<}'  )

                samples_added += 1

            else:
                attempts +=1


        current_kit_label = current_kit_label + 1


if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()
    print(args)
    generate_kits(args)



