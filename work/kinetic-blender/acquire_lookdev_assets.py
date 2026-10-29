"""Fetch only selected Poly Haven CC0 assets, with source metadata and checksums."""
import hashlib
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent / 'assets'
ROOT.mkdir(exist_ok=True)
HEADERS = {'User-Agent': 'KineticStudio-Lookdev/1.0 (reference-driven local Blender art production)'}

CHANNEL_ALIASES = {
    'diff': ['diff', 'diffuse'],
    'rough': ['rough', 'roughness'],
    'nor_gl': ['nor_gl'],
}


def fetch(url):
    if not url.startswith(('https://api.polyhaven.com/', 'https://polyhaven.com/', 'https://cdn.polyhaven.com/', 'https://dl.polyhaven.org/')):
        raise ValueError('Unexpected asset origin')
    return urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=90).read()


def js(url):
    return json.loads(fetch(url))


def get_texture_extension(options):
    if 'jpg' in options:
        return 'jpg'
    if 'png' in options:
        return 'png'
    return 'exr'


def build_texture_tasks(name, files):
    tasks = []
    for channel in ['diff', 'rough', 'nor_gl']:
        aliases = CHANNEL_ALIASES[channel]
        key = next(k for k in files if k.lower() in aliases)
        options = files[key]['2k']
        ext = get_texture_extension(options)
        entry = options[ext]
        tasks.append((f"{name}_{channel}_2k.{ext}", entry))
    return tasks


def build_asset_tasks(name, kind, files):
    if kind == 'model':
        entry = files['blend']['1k']['blend']
        return [(f"{name}_1k.blend", entry)] + list(entry.get('include', {}).items())
    elif kind == 'hdri':
        entry = files['hdri']['2k']['hdr']
        return [(f"{name}_2k.hdr", entry)]
    else:
        return build_texture_tasks(name, files)


def save_asset_file(task, asset_root, root_dir=ROOT):
    relative, entry = task
    dest = (asset_root / relative).resolve()
    assert dest.is_relative_to(asset_root.resolve())
    dest.parent.mkdir(parents=True, exist_ok=True)

    data = dest.read_bytes() if dest.exists() else fetch(entry['url'])
    assert hashlib.md5(data).hexdigest() == entry['md5'], f"{relative} checksum mismatch"

    if not dest.exists():
        dest.write_bytes(data)

    return {
        'path': str(dest.relative_to(root_dir)),
        'source': entry['url'],
        'bytes': len(data),
        'sha256': hashlib.sha256(data).hexdigest(),
    }


def process_asset(name, kind, root_dir=ROOT):
    asset_root = root_dir / name
    asset_root.mkdir(exist_ok=True)

    info = js(f"https://api.polyhaven.com/info/{name}")
    files = js(f"https://api.polyhaven.com/files/{name}")

    (asset_root / 'info.json').write_text(json.dumps(info, indent=2), encoding='utf-8')
    (asset_root / 'files.json').write_text(json.dumps(files, indent=2), encoding='utf-8')

    tasks = build_asset_tasks(name, kind, files)

    def save_task(task):
        return save_asset_file(task, asset_root, root_dir=root_dir)

    with ThreadPoolExecutor(max_workers=5) as pool:
        downloads = list(pool.map(save_task, tasks))

    return {
        'kind': kind,
        'source': f"https://polyhaven.com/a/{name}",
        'authors': info.get('authors', {}),
        'files': downloads,
    }


def download_previews(names, root_dir=ROOT):
    for name in names:
        url = f"https://cdn.polyhaven.com/asset_img/thumbs/{name}.png?height=512"
        (root_dir / f"{name}_preview.png").write_bytes(fetch(url))
        print('PREVIEW', name)


def main():
    import sys
    if '--preview' in sys.argv:
        names = ['sofa_02', 'sofa_03', 'modern_arm_chair_01', 'mid_century_lounge_chair', 'potted_plant_02', 'potted_plant_04']
        download_previews(names)
    else:
        license_text = fetch('https://polyhaven.com/license').decode('utf-8')
        assert 'CC0' in license_text
        selected = {
            'potted_plant_02': 'model',
            'potted_plant_04': 'model',
            'mid_century_lounge_chair': 'model',
            'qwantani_dusk_2_puresky': 'hdri',
            'brown_leather': 'texture',
            'wood_cabinet_worn_long': 'texture',
        }
        manifest = {
            'provider': 'Poly Haven',
            'license': 'CC0',
            'license_url': 'https://polyhaven.com/license',
            'assets': {},
        }
        for name, kind in selected.items():
            asset_data = process_asset(name, kind)
            manifest['assets'][name] = asset_data
            downloads = asset_data['files']
            (ROOT / 'asset-provenance.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
            print('ASSET_VERIFIED', name, len(downloads), sum(d['bytes'] for d in downloads), flush=True)


if __name__ == '__main__':
    main()
