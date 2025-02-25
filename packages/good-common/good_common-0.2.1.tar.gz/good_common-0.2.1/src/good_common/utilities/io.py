import zipfile
from pathlib import Path
from contextlib import asynccontextmanager
import httpx
from typing import AsyncGenerator
import tempfile
import tqdm


async def decompress_tempfile(tempfile: Path) -> Path:
    """
    Takes a Path object to a compressed file and returns a Path object to the
    decompressed archive folder.
    """
    with zipfile.ZipFile(tempfile, "r") as archive:
        archive.extractall(tempfile.parent / tempfile.stem)
    return tempfile.parent / tempfile.stem


class FileDoesNotExist(Exception):
    pass


@asynccontextmanager
async def download_url_to_tempfile(
    url: str, directory: Path, display_progress: bool = True
) -> AsyncGenerator[Path, None]:
    download_file = None
    async with httpx.AsyncClient(
        timeout=30,
    ) as client:
        try:
            with tempfile.NamedTemporaryFile(
                dir=directory, delete=False, suffix=".zip"
            ) as download_file:
                filepath = Path(download_file.name)
                async with client.stream("GET", url) as response:
                    if response.status_code != 200:
                        raise FileDoesNotExist(f"File not found at {url}")
                    total = int(response.headers.get("Content-Length", 0))
                    with tqdm.tqdm(
                        total=total,
                        unit_scale=True,
                        unit_divisor=1024,
                        unit="B",
                        disable=not display_progress,
                    ) as progress:
                        num_bytes_downloaded = response.num_bytes_downloaded
                        async for chunk in response.aiter_bytes():
                            download_file.write(chunk)
                            progress.update(
                                response.num_bytes_downloaded - num_bytes_downloaded
                            )
                            num_bytes_downloaded = response.num_bytes_downloaded
            yield filepath
        finally:
            if filepath.exists():
                filepath.unlink()
