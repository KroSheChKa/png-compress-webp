import argparse
from pathlib import Path
from PIL import Image

def convert_to_webp(
    input_path: Path,
    output_dir: Path,
    lossless: bool,
    quality: int,
    optimize_palette: bool
):
    img = Image.open(input_path)
    
    if optimize_palette and lossless and input_path.suffix.lower() == '.png':
        img = img.convert('P', palette=Image.ADAPTIVE)

    output_path = output_dir / f"{input_path.stem}.webp"
    img.save(
        output_path,
        format='WEBP',
        lossless=lossless,
        quality=quality,
        method=6 # уровень компрессии WebP (0–6, 6 — максимальный)
    )
    print(f"Saved: {output_path.relative_to(Path.cwd())}")

def main():
    parser = argparse.ArgumentParser(
        description="Batch-convert images to WebP with optional lossless optimization"
    )

    parser.add_argument(
        "src_dir",
        type=Path,
        nargs="?",
        default=Path(__file__).parent / "input",
        help="Папка с исходными изображениями (по умолчанию ./input)"
    )

    parser.add_argument(
        "-o", "--out_dir",
        type=Path,
        default=None,
        help="Куда класть WebP (по умолчанию ../output рядом с src_dir)"
    )
    parser.add_argument(
        "--lossy",
        action="store_true",
        help="Использовать lossy-сжатие (иначе — lossless)"
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=90,
        help="Качество для lossy (0–100), по умолчанию 80"
    )
    args = parser.parse_args()

    src = args.src_dir
    out = args.out_dir or (src.parent / "output")
    out.mkdir(parents=True, exist_ok=True)

    lossless = not args.lossy
    lossless = 0
    quality = args.quality
    quality = 98
    optimize_palette = lossless

    exts = {'.png', '.jpg', '.jpeg', '.bmp', '.gif'}
    for img_path in src.iterdir():
        if img_path.suffix.lower() in exts and img_path.is_file():
            convert_to_webp(
                img_path, out,
                lossless=lossless,
                quality=quality,
                optimize_palette=optimize_palette
            )

if __name__ == "__main__":
    main()
