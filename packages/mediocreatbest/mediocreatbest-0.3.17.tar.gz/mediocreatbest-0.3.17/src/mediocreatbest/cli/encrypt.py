"""

"""

from __future__ import annotations
from .._auto import auto


def main(
    *,
    input_path: auto.pathlib.Path,
    output_path: auto.pathlib.Path,
    password_name: str,
):
    password = auto.os.environ[password_name]
    
    auto.self.lib.encrypt(
        dec_path = input_path,
        enc_path = output_path,
        password = password,
    )


def cli(args = None):
    parser = auto.argparse.ArgumentParser()

    parser.add_argument(
        '--input-path',
        '-i',
        type = auto.pathlib.Path,
        required = True,
    )

    parser.add_argument(
        '--output-path',
        '-o',
        type = auto.pathlib.Path,
        required = True,
    )

    parser.add_argument(
        '--password-name',
        '-p',
        type = str,
        required = True,
    )
    
    args = vars(parser.parse_args(args))
    
    main(**args)

if __name__ == '__main__':
    cli()
