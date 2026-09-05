def dupes(tracks, tags, func, matchcase=False, threshold=1, prevdupe=None):
    if matchcase:
        strings = [
            [(i, t.get(field, "")) for i, t in enumerate(tracks)] for field in tags
        ]
    else:
        strings = [
            [(i, t.get(field, "").lower()) for i, t in enumerate(tracks)]
            for field in tags
        ]
    if prevdupe:
        ret = prevdupe
        start = 0
    else:
        start = 1
        ret = finddupes(strings[0], func, threshold)

    for s in strings[start:]:
        l = []
        dups = finddupes(s, func, threshold)
        if len(dups) > len(ret):
            for z in dups:
                x = [z.intersection(r) for r in ret if z.intersection(r)]
                if x:
                    l.append(x[0])
        else:
            for z in ret:
                x = [z.intersection(r) for r in dups if z.intersection(r)]
                if x:
                    l.append(x[0])
        ret = l
    return ret


def delete(l, dellist):
    while dellist:
        del l[dellist[0]]
        dellist = [z - 1 for z in dellist][1:]


def finddupes(strings, func, threshold=1):
    dupes = []
    while strings:
        index, mainstring = strings[0]
        dupeset = {index}
        li = strings[1:]
        todelete = []
        for z, s in enumerate(li):
            if func(s[1], mainstring) >= threshold:
                dupeset.add(s[0])
                todelete.append(z + 1)
        delete(strings, todelete)
        strings = strings[1:]
        if len(dupeset) > 1:
            dupes.append(dupeset)
    return dupes


def dupesinlib(library, algs, maintag=None, artists=None):
    alg = algs[0]

    if not maintag:
        maintag = alg.tags[0]
    if not artists:
        artists = sorted(library.distinct_values(maintag))
    yield artists
    for a in artists:
        tracks = library.get_tracks(maintag, a)
        st = [z.stringtags() for z in library.get_tracks(maintag, a)]
        ret = dupes(st, alg.tags, alg.func, alg.matchcase, alg.threshold)
        for alg in algs:
            ret = dupes(st, alg.tags, alg.func, alg.matchcase, alg.threshold, ret)
        yield [[tracks[i] for i in z] for z in ret]


if __name__ == "__main__":
    from ..libraries import quodlibetlib as quodlibet

    lib = quodlibet.QuodLibet(".quodlibet/songs")

    # 'algo' is not defined here; this __main__ block is demo code
    # for the dupe-finder API and only runs with custom user code.
    # The original references 'algo' but never defines it; the
    # actual 'algos' list is meant to use a class with .tags/.threshold
    # etc. that lives elsewhere.
    for z in dupesinlib(lib, []):
        if z:
            print(z)
