"""Verify the extracted release payload, filters, dependencies and signatures."""
import argparse
import hashlib
import json
from pathlib import Path
import plistlib
import struct
import subprocess
import tempfile


def run(*args):
    return subprocess.check_output(list(map(str, args)), text=True, stderr=subprocess.STDOUT)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    args = parser.parse_args()
    results = []
    for scheme, architecture, prefix in [('rootless', 'iphoneos-arm64', 'var/jb'), ('rootful', 'iphoneos-arm', '')]:
        package = args.folder / f'Spotify-9.1.90-Vitrine-Pixie-v1.2-{scheme}.deb'
        assert run('dpkg-deb', '-f', package, 'Architecture').strip() == architecture
        assert run('dpkg-deb', '-f', package, 'Version').strip() == '9.1.90-1.2'
        with tempfile.TemporaryDirectory(prefix='pixie-deb-check-') as temporary:
            extracted = Path(temporary)
            run('dpkg-deb', '-R', package, extracted)
            assert sorted(p.name for p in (extracted/'DEBIAN').iterdir()) == ['control']
            libraries = extracted/prefix/'Library/MobileSubstrate/DynamicLibraries'
            assert sorted(p.name for p in libraries.iterdir()) == [
                'SpotifyAudioProbe.dylib', 'SpotifyAudioProbe.plist', 'spotifyglass.dylib', 'spotifyglass.plist']
            for name in ['SpotifyAudioProbe', 'spotifyglass']:
                assert plistlib.loads((libraries/(name+'.plist')).read_bytes()) == {'Filter': {'Executables': ['Spotify']}}
                library = libraries/(name+'.dylib')
                assert struct.unpack_from('<II', library.read_bytes()) == (0xfeedfacf, 0x100000c)
                run('codesign', '--verify', '--strict', library)
                run('xcrun', 'dyld_info', '-validate_only', library)
                dependencies = run('otool', '-L', library)
                assert '@rpath/CydiaSubstrate.framework/CydiaSubstrate' in dependencies
                assert '/Users/' not in dependencies
                commands = run('otool', '-l', library)
                framework_path = '/'+('/'.join([prefix, 'Library/Frameworks']).lstrip('/'))
                assert 'path '+framework_path+' (offset' in commands
                if name == 'spotifyglass':
                    assert dependencies.count('@loader_path/SpotifyAudioProbe.dylib') == 1
                else:
                    binary = library.read_bytes()
                    for marker in [b'Pixie Download Manager', b'Reset log', b'log_reset', b'9.1.90-v1.2',
                                   b'https://github.com/Glongq/Vitrine-Pixie', b'https://t.me/glongqforks',
                                   b'SAPTraceNativeBoundary', b'vitrine_page_hook_installed']:
                        assert marker in binary, marker
                    for marker in [b'Start WAV recording', b'Export WAV']:
                        assert marker not in binary, marker
            results.append({'file': package.name, 'sha256': hashlib.sha256(package.read_bytes()).hexdigest(),
                            'extracted_filters_signatures_dependencies_and_latest_ui': 'passed'})
    report = {'release': '9.1.90-Vitrine-Pixie-v1.2', 'packages': results,
              'scope': 'Extracted package verification; runtime tests are recorded separately.',
              'jailbroken_device_tested': False}
    (args.folder/'verification.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
