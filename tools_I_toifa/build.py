#!/usr/bin/env python3
"""Savol matnlari (q/NNN.txt) -> shablon.xlsx asosidagi NNN.xlsx. Tekshiruv + seed'li shuffle."""
import re, sys, os, glob, random, zipfile, json
from xml.sax.saxutils import escape

W = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = '/projects/sandbox/Epid-vrach-oliy-test/shablon.xlsx'
QDIR = os.path.join(W, 'q')
OUT = os.path.join(W, 'out')
L = 'ABCDE'
BAD_START = ("faqat", "hech", "umuman", "barcha")


def parse(path):
    topic = None; qs = []; cur = None; diffs = []; unv = []
    for raw in open(path, encoding='utf8'):
        line = raw.rstrip('\n')
        if not line.strip():
            continue
        if line.startswith('=== '):
            topic = line[4:].strip(); continue
        if line.startswith('#D'):
            diffs.append(line[2:].strip()); continue
        if line.startswith('#U'):
            unv.append(line[2:].strip()); continue
        t, body = line[0], line[2:].strip()
        if t == '?':
            cur = {'q': body, 'ok': None, 'bad': [], 'note': '', 'src': ''}; qs.append(cur)
        elif t == '+': cur['ok'] = body
        elif t == '-': cur['bad'].append(body)
        elif t == '!': cur['note'] = body
        elif t == '@': cur['src'] = body
        else: raise ValueError(f'{path}: noma\'lum qator: {line[:60]}')
    return topic, qs, diffs, unv


def first_word(s):
    m = re.match(r"\W*([\w'’ʻʼ`-]+)", s.lower())
    return m.group(1) if m else ''


def flags_for(q, ok, wrongs):
    f = []
    if len(wrongs) != 4: f.append('4 ta noto\'g\'ri emas')
    lens = [len(w) for w in wrongs]
    if lens and len(ok) > 1.10 * max(lens): f.append(f'uzun {len(ok)}/{max(lens)}={len(ok)/max(lens):.2f}')
    bad = sum(1 for w in wrongs if first_word(w) in BAD_START)
    if bad > 1: f.append(f'Faqat/Hech x{bad}')
    from collections import Counter
    c = Counter(first_word(w) for w in wrongs)
    for w, n in c.items():
        if n >= 3 and first_word(ok) != w and not re.match(r'^[\d\W]', w): f.append(f'bir xil boshlanish "{w}" x{n}')
    if len(set(x.strip().lower() for x in wrongs + [ok])) < 5: f.append('takroriy variant')
    if not q.get('note') or not q.get('src'): f.append('izoh/manba yo\'q')
    return f


def letter_plan(n, rng, gcount):
    base, r = divmod(n, 5)
    cnt = {l: base for l in L}
    order = sorted(L, key=lambda l: (gcount[l] + 0, rng.random()))
    for l in order[:r]: cnt[l] += 1
    for _ in range(2000):
        seq = [l for l in L for _ in range(cnt[l])]
        rng.shuffle(seq)
        if all(not (seq[i] == seq[i+1] == seq[i+2]) for i in range(len(seq) - 2)):
            return seq
    raise RuntimeError('ketma-ket 3 ta harfsiz tartib topilmadi')


def comment(q):
    ok = q['ok'].rstrip()
    ok_dot = ok if ok.endswith('.') else ok + '.'
    note = q['note'].strip()
    if not note.endswith('.'): note += '.'
    src = q['src'].strip().rstrip('.')
    return f"To'g'ri javob: {ok_dot} {note} Manba: {src}."


def build_xlsx(name, rows):
    zin = zipfile.ZipFile(TEMPLATE)
    strings = ['Question', 'A', 'B', 'C', 'D', 'Correct', "Comment (Faqat to'g'ri javob uchun)", 'E']  # shablon indekslari
    idx = {s: i for i, s in enumerate(strings)}
    # yangi satrlar uchun alohida (takrorlanmaydigan) indekslar
    xml_rows = []
    new = []
    def sid(s):
        new.append(s); return len(strings) - 1 + len(new)
    for r, row in enumerate(rows, start=2):
        cells = ''.join(f'<c r="{c}{r}" s="1" t="s"><v>{sid(v)}</v></c>' for c, v in zip('ABCDEFGH', row))
        xml_rows.append(f'<row r="{r}" spans="1:8">{cells}</row>')
    sheet = zin.read('xl/worksheets/sheet1.xml').decode('utf8')
    sheet = sheet.replace('</row></sheetData>', '</row>' + ''.join(xml_rows) + '</sheetData>')
    sheet = sheet.replace('<dimension ref="A1:H1"/>', f'<dimension ref="A1:H{len(rows)+1}"/>')
    sst = zin.read('xl/sharedStrings.xml').decode('utf8')
    tot = 8 + len(new)
    sst = re.sub(r'count="8" uniqueCount="8"', f'count="{tot}" uniqueCount="{tot}"', sst)
    add = ''.join(f'<si><t xml:space="preserve">{escape(s)}</t></si>' for s in new)
    sst = sst.replace('</sst>', add + '</sst>')
    path = os.path.join(OUT, name + '.xlsx')
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as zo:
        for it in zin.infolist():
            data = zin.read(it.filename)
            if it.filename == 'xl/worksheets/sheet1.xml': data = sheet.encode('utf8')
            elif it.filename == 'xl/sharedStrings.xml': data = sst.encode('utf8')
            zo.writestr(it, data)


def main(check_only=False):
    os.makedirs(OUT, exist_ok=True)
    gcount = {l: 0 for l in L}
    allflags = {}; stats = {'files': 0, 'q': 0, 'long': 0}
    reports = {'diff': {}, 'unv': {}}
    for p in sorted(glob.glob(os.path.join(QDIR, '*.txt'))):
        name = os.path.basename(p)[:-4]
        topic, qs, diffs, unv = parse(p)
        reports['diff'][name] = diffs; reports['unv'][name] = unv
        rng = random.Random(int(name))
        fl = []
        if len(qs) < 10: fl.append((0, f'savollar soni {len(qs)} < 10'))
        plan = letter_plan(len(qs), rng, gcount)
        rows = []
        for i, q in enumerate(qs, 1):
            for f in flags_for(q, q['ok'] or '', q['bad']): fl.append((i, f))
            if not q['ok'] or len(q['bad']) != 4: continue
            if len(q['ok']) > 1.10 * max(len(w) for w in q['bad']): stats['long'] += 1
            wr = q['bad'][:]; rng.shuffle(wr)
            pos = L.index(plan[i-1])
            opts = wr[:pos] + [q['ok']] + wr[pos:]
            rows.append([q['q']] + opts + [plan[i-1], comment(q)])
            gcount[plan[i-1]] += 1
        stats['files'] += 1; stats['q'] += len(rows)
        if fl: allflags[name] = fl
        if not check_only and not [f for f in fl if f[0] == 0]:
            build_xlsx(name, rows)
    json.dump(reports, open(os.path.join(W, 'reports.json'), 'w'), ensure_ascii=False, indent=1)
    for n, fl in allflags.items():
        for i, f in fl: print(f'{n} #{i}: {f}')
    print('STATS', stats, 'LETTERS', gcount, 'flagged files', len(allflags), 'flags', sum(len(v) for v in allflags.values()))


if __name__ == '__main__':
    main(check_only='--check' in sys.argv)
