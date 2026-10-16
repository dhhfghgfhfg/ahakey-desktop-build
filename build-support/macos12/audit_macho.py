import json
import pathlib
import plistlib
import struct
import sys


def versions(data):
    magic = struct.unpack_from('>I', data)[0]
    if magic in (0xcafebabe, 0xcafebabf):
        count = struct.unpack_from('>I', data, 4)[0]
        result = []
        for i in range(count):
            if magic == 0xcafebabe:
                _, _, offset, size, _ = struct.unpack_from('>iiIII', data, 8 + 20 * i)
            else:
                _, _, offset, size, _, _ = struct.unpack_from('>iiQQII', data, 8 + 32 * i)
            result.extend(versions(data[offset:offset + size]))
        return result
    assert magic in (0xcffaedfe, 0xcefaedfe), hex(magic)
    cpu = struct.unpack_from('<I', data, 4)[0]
    count = struct.unpack_from('<I', data, 16)[0]
    offset = 32 if magic == 0xcffaedfe else 28
    minimum = None
    for _ in range(count):
        command, size = struct.unpack_from('<II', data, offset)
        if command in (0x32, 0x24):
            value = struct.unpack_from('<I', data, offset + (12 if command == 0x32 else 8))[0]
            minimum = (value >> 16, (value >> 8) & 255, value & 255)
        offset += size
    assert minimum is not None
    return [{'cpu':cpu, 'minimum':minimum}]


def main():
    app = pathlib.Path(sys.argv[1])
    info = plistlib.loads((app / 'Contents/Info.plist').read_bytes())
    assert info['CFBundleShortVersionString'] == '0.2.3'
    assert info['LSMinimumSystemVersion'] == '12.0'
    report = {'version':'0.2.3', 'target_system':'macOS 12.7.6 Intel', 'executables':[]}
    for relative in ('Contents/MacOS/AhaKeyConfig', 'Contents/MacOS/ahakeyconfig-agent', 'Contents/Resources/FirmwareFlasher/tools/x86_64/wchisp'):
        targets = versions((app / relative).read_bytes())
        intel = [target for target in targets if target['cpu'] == 0x1000007]
        assert intel and all(tuple(target['minimum']) <= (12, 7, 6) for target in intel), (relative, targets)
        if relative.startswith('Contents/MacOS/'):
            assert len(targets) == 1 and len(intel) == 1
        report['executables'].append({'path':relative, 'targets':targets})
    text = json.dumps(report, indent=2) + '\n'
    pathlib.Path(sys.argv[2]).write_text(text)
    print(text)


if __name__ == '__main__':
    main()
