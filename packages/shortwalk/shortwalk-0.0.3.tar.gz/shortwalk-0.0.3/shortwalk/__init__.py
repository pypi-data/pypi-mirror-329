import os
import glob
import fnmatch

def walk(top, maxdepth=0, skip=None, topdown=True, onerror=None, followlinks=False):
    return _walk(os.fspath(top), maxdepth, skip, topdown, onerror, followlinks)

def make_skip_pred(skip):
    def pred(name):
        for pattern in skip:
            if fnmatch.fnmatch(name, pattern):
                return True
            if name == pattern:
                return True
        return False
    return pred

def _walk(top, maxdepth, skip, topdown, onerror, followlinks):
    dirs = []
    nondirs = []
    walk_dirs = []
    if skip is None:
        skip = []
    skip_pred = make_skip_pred(skip)
    try:
        scandir_it = os.scandir(top)
    except OSError as error:
        if onerror is not None:
            onerror(error)
        return

    with scandir_it:
        while True:
            try:
                try:
                    entry = next(scandir_it)
                except StopIteration:
                    break
            except OSError as error:
                if onerror is not None:
                    onerror(error)
                return

            try:
                is_dir = entry.is_dir()
            except OSError:
                is_dir = False

            if is_dir:
                if not skip_pred(entry.name):
                    dirs.append(entry.name)
            else:
                if not skip_pred(entry.name):
                    nondirs.append(entry.name)

            if not topdown and is_dir:
                if followlinks:
                    walk_into = True
                else:
                    try:
                        is_symlink = entry.is_symlink()
                    except OSError:
                        is_symlink = False
                    walk_into = not is_symlink

                if skip_pred(entry.name):
                    walk_into = False

                if walk_into:
                    walk_dirs.append(entry.path)

    maxdepth -= 1
    if topdown:
        yield top, dirs, nondirs
        if maxdepth == 0:
            return
        islink, join = os.path.islink, os.path.join
        for dirname in dirs:
            new_path = join(top, dirname)
            if followlinks or not islink(new_path):
                yield from _walk(new_path, maxdepth, skip, topdown, onerror, followlinks)
    else:
        if maxdepth == 0:
            walk_dirs = []
        for new_path in walk_dirs:
            yield from _walk(new_path, maxdepth, skip, topdown, onerror, followlinks)
        yield top, dirs, nondirs

def main():
    import argparse
    parser = argparse.ArgumentParser(prog='shortwalk')
    parser.add_argument("--maxdepth", "-d", type=int, default=0)
    parser.add_argument("--skip", "-s", nargs='*')
    parser.add_argument("--topdown", "-t", type=int, default=1)
    args = parser.parse_args()
    #print(args); exit(0)
    for root, dirs, files in walk(os.getcwd(), maxdepth = args.maxdepth, skip = args.skip, topdown=args.topdown):
        for name in dirs:
            print(os.path.join(root, name))
        for name in files:
            print(os.path.join(root, name))

if __name__ == "__main__":
    main()