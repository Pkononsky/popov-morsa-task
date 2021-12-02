import sys
import argparse
import psutil

BYTES_IN_GIG = float(1024 * 1024 * 1024) # 1 gig in bytes
MAX_SIZE = 0
# 1 gig * 1024 mega * 1024 kilo * 1024 byte


def write_tye_morsa_file(file_name):
    bytes_in_file = 1
    read_size = 1024 * 1024 * 1024

    while True:
        readed = 0
        need_to_read_size = bytes_in_file
        while readed != need_to_read_size:
            with open(file_name, mode='r+', encoding='utf-8') as f:
                f.seek(readed)
                line = f.read(read_size)
                f.seek(0, 2)
                readed += len(line)
                for symbol in line:
                    f.write('1' if symbol == '0' else '0')
                    bytes_in_file += 1
                    if bytes_in_file >= MAX_SIZE:
                        return

        print(f'{bytes_in_file} of {MAX_SIZE} completed')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fileName', help='Определить назначение записи файл с указанным именем')
    parser.add_argument('--ram', help='Определить назначение записи оперативную память', nargs='?')
    parser.add_argument('--size', help='Определить выходной размер файла в Гигабайтах Значение будет уменьшено до 99,99%%. Используется вместе с fileName')

    try:
        args = vars(parser.parse_args())

        if args['fileName']:
            global BYTES_IN_GIG, MAX_SIZE
            MAX_SIZE = int(BYTES_IN_GIG * float(args['size']) * 0.9999)

            file_name = args['fileName']
            file = open(file_name, mode='w+', encoding='utf-8')
            file.write('0')
            file.close()

            write_tye_morsa_file(file_name)
            print(f'Done!')
        elif '--ram' in sys.argv:
            target_mem = int(psutil.virtual_memory().total * 0.1)
            morsa_str = ['0']

            while True:
                new_morsa_str = ['1' if symbol == '0' else '0' for symbol in morsa_str]
                morsa_str.extend(new_morsa_str)
                print(f'current free memory:{psutil.virtual_memory().free}\ttarget free memory: {target_mem}\tcurrent morsa len: {len(morsa_str)}')
                if psutil.virtual_memory().free <= target_mem:
                    print(f'Done!')
                    break
    except:
        parser.print_help()


if __name__ == '__main__':
    main()

