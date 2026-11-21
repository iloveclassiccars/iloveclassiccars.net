#!/usr/bin/env python3
"""오픈 전 테스트 글 일괄 삭제 도구.
사용: python3 tools/purge_test_posts.py            -> 미리 세기만 함(아무것도 안 지움)
      python3 tools/purge_test_posts.py --apply    -> board/index.html 안의 테스트 글(test:1)을 지움
지우기 전 board/index.html.bak-날짜 로 자동 백업합니다."""
import json, re, sys, shutil, datetime
P = 'board/index.html'
s = open(P, encoding='utf-8').read()
i = s.find('var D=') + len('var D=')
D, end = json.JSONDecoder().raw_decode(s, i)
tot = keep = 0
rep = []
for k, b in D.items():
    items = b.get('items', [])
    real = [x for x in items if not x.get('test')]
    rep.append((k, len(items), len(items) - len(real), len(real)))
    tot += len(items); keep += len(real)
    if '--apply' in sys.argv:
        b['items'] = real
print('게시판      전체   테스트   남는 글')
for r in rep: print(f'{r[0]:<10}{r[1]:>6}{r[2]:>8}{r[3]:>9}')
print(f'합계      {tot:>6}{tot-keep:>8}{keep:>9}')
if '--apply' in sys.argv:
    bak = P + '.bak-' + datetime.datetime.now().strftime('%Y%m%d-%H%M')
    shutil.copy(P, bak)
    s = s[:i] + json.dumps(D, ensure_ascii=False) + s[end:]
    open(P, 'w', encoding='utf-8').write(s)
    print('지웠습니다. 백업:', bak)
else:
    print('미리 세기만 했습니다. 실제로 지우려면 --apply')
