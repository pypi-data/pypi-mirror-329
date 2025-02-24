"""Console script for fouriercrop."""

from typing import Annotated, Optional

import numpy as np
import typer

from fouriercrop import FourierCrop, __version__, load_mrc, save_mrc

app = typer.Typer()


def version_callback(value: bool) -> None:
    """Callback function for the --version option."""
    if value:
        typer.echo(f"fouriercrop, version {__version__}")
        raise typer.Exit()


@app.command()
def main(
    input_path: Optional[str] = None,
    output_path: Optional[str] = None,
    bin_factor: int = 2,
    pad_mode: int = 0,
    norm_flag: bool = False,
    version: Annotated[
        Optional[bool],
        typer.Option("--version", callback=version_callback, is_eager=True),
    ] = None,
) -> None:
    """Console script for fouriercrop."""
    if input_path:
        x, v = load_mrc(input_path, as_tensor=True, get_voxel_size=True)
        x = x.unsqueeze(0).unsqueeze(0)  # type: ignore[union-attr]
        print(f"input shape: {x.shape}")

        fc_func = FourierCrop(pad_mode=pad_mode)
        x = fc_func(x, bin_factor=bin_factor, norm_flag=norm_flag)
        print(f"output shape: {x.shape}")

        if output_path:
            save_mrc(output_path, x.squeeze().numpy(), voxel_size=np.min(v))
            print(f"Save: {output_path}")
    else:
        print("fouriercrop.cli.main")


if __name__ == "__main__":
    app()  # pragma: no cover
