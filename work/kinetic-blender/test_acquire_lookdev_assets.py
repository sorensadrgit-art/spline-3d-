import hashlib
import json
from unittest.mock import patch
import pytest

from acquire_lookdev_assets import (
    get_texture_extension,
    build_texture_tasks,
    build_asset_tasks,
    save_asset_file,
    process_asset,
    fetch,
)


def test_fetch_invalid_url():
    with pytest.raises(ValueError, match="Unexpected asset origin"):
        fetch("https://example.com/malicious")


def test_get_texture_extension():
    assert get_texture_extension({'jpg': {}, 'png': {}}) == 'jpg'
    assert get_texture_extension({'png': {}, 'exr': {}}) == 'png'
    assert get_texture_extension({'exr': {}}) == 'exr'


def test_build_texture_tasks():
    files = {
        'DIFFUSE': {'2k': {'jpg': {'url': 'http://diff.jpg'}}},
        'ROUGHNESS': {'2k': {'png': {'url': 'http://rough.png'}}},
        'nor_gl': {'2k': {'exr': {'url': 'http://nor.exr'}}},
    }
    tasks = build_texture_tasks('wood', files)
    assert len(tasks) == 3
    assert tasks[0] == ('wood_diff_2k.jpg', {'url': 'http://diff.jpg'})
    assert tasks[1] == ('wood_rough_2k.png', {'url': 'http://rough.png'})
    assert tasks[2] == ('wood_nor_gl_2k.exr', {'url': 'http://nor.exr'})


def test_build_asset_tasks_model_and_hdri():
    files_model = {
        'blend': {
            '1k': {
                'blend': {
                    'url': 'http://model.blend',
                    'include': {'textures/tex1.png': {'url': 'http://tex1.png'}},
                }
            }
        }
    }
    model_tasks = build_asset_tasks('chair', 'model', files_model)
    assert len(model_tasks) == 2
    assert model_tasks[0] == ('chair_1k.blend', files_model['blend']['1k']['blend'])
    assert model_tasks[1] == ('textures/tex1.png', {'url': 'http://tex1.png'})

    files_hdri = {'hdri': {'2k': {'hdr': {'url': 'http://sky.hdr'}}}}
    hdri_tasks = build_asset_tasks('sky', 'hdri', files_hdri)
    assert len(hdri_tasks) == 1
    assert hdri_tasks[0] == ('sky_2k.hdr', {'url': 'http://sky.hdr'})


def test_save_asset_file(tmp_path):
    asset_root = tmp_path / 'test_asset'
    asset_root.mkdir()
    content = b"fake binary data"
    md5 = hashlib.md5(content).hexdigest()
    sha256 = hashlib.sha256(content).hexdigest()

    entry = {'url': 'https://api.polyhaven.com/fake', 'md5': md5}
    task = ('sub/file.png', entry)

    with patch('acquire_lookdev_assets.fetch', return_value=content):
        res = save_asset_file(task, asset_root, root_dir=tmp_path)

    dest_file = asset_root / 'sub/file.png'
    assert dest_file.exists()
    assert dest_file.read_bytes() == content
    assert res['bytes'] == len(content)
    assert res['sha256'] == sha256
    assert res['path'] == 'test_asset/sub/file.png'

    # Test when file already exists locally
    with patch('acquire_lookdev_assets.fetch') as mock_fetch:
        res2 = save_asset_file(task, asset_root, root_dir=tmp_path)
        mock_fetch.assert_not_called()
    assert res2['sha256'] == sha256


def test_process_asset(tmp_path):
    info_data = {'authors': {'artist': 'Soren'}}
    files_data = {'hdri': {'2k': {'hdr': {'url': 'https://api.polyhaven.com/sky.hdr', 'md5': hashlib.md5(b"skydata").hexdigest()}}}}

    def fake_js(url):
        if '/info/' in url:
            return info_data
        if '/files/' in url:
            return files_data
        return {}

    with patch('acquire_lookdev_assets.js', side_effect=fake_js), \
         patch('acquire_lookdev_assets.fetch', return_value=b"skydata"):
        res = process_asset('sky_asset', 'hdri', root_dir=tmp_path)

    assert res['kind'] == 'hdri'
    assert res['authors'] == {'artist': 'Soren'}
    assert len(res['files']) == 1
    assert (tmp_path / 'sky_asset/info.json').exists()
    assert (tmp_path / 'sky_asset/files.json').exists()
