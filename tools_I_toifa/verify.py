import zipfile,re,glob,html,collections,xml.dom.minidom as md
L='ABCDE'
tot=collections.Counter(); n=0; over10=0; over0=0; maxr=0; seqbad=0; fsc=0
for f in sorted(glob.glob('out/*.xlsx')):
    z=zipfile.ZipFile(f)
    for nm in z.namelist():
        if nm.endswith('.xml') or nm.endswith('.rels'): md.parseString(z.read(nm))
    sst=[html.unescape(re.sub('<[^>]+>','',s)) for s in re.findall(r'<si>(.*?)</si>',z.read('xl/sharedStrings.xml').decode(),re.S)]
    sh=z.read('xl/worksheets/sheet1.xml').decode()
    assert 'dataValidation' in sh
    rows=re.findall(r'<row r="(\d+)".*?>(.*?)</row>',sh,re.S)
    seq=[]
    for r,body in rows[1:]:
        cells=re.findall(r'<c r="([A-H])\d+"[^>]*><v>(\d+)</v>',body)
        v=[sst[int(i)] for _,i in cells]; assert len(v)==8
        q,opts,c,cm=v[0],v[1:6],v[6],v[7]
        assert c in L and len(set(opts))==5
        ok=opts[L.index(c)]; 
        assert cm.startswith("To'g'ri javob: "+ok.rstrip('.')) and ' Manba: ' in cm, (f,r)
        w=max(len(o) for i,o in enumerate(opts) if i!=L.index(c))
        rat=len(ok)/w; maxr=max(maxr,rat); over10+=rat>1.10; over0+=rat>1.0
        tot[c]+=1; n+=1; seq.append(c)
    assert len(seq)>=10, f
    if any(seq[i]==seq[i+1]==seq[i+2] for i in range(len(seq)-2)): seqbad+=1
print(n,dict(tot),'>10%:',over10,'>0%:',over0,'maxratio',round(maxr,3),'3-in-row files',seqbad)
