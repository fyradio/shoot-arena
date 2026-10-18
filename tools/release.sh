#!/bin/bash
# 用法: bash release.sh "更新說明" [patch|minor]
# 流程: 語法檢查 → 版本號+1 → SW 版本+1 → build → git commit/push
# 發佈 Artifact 仍要由 Claude 用 Artifact 工具做（file_path=/home/claude/spin.html, url=遊戲 artifact 網址）
set -e
SRC=/home/claude/spin.html; REPO=/home/claude/shoot-arena; MSG="${1:?need message}"; LV="${2:-patch}"
node -e "const s=require('fs').readFileSync('$SRC','utf8');const m=[...s.matchAll(/<script>([\s\S]*?)<\/script>/g)];if(!m.length)throw 'no script';m.forEach(x=>new Function(x[1]));console.log('syntax ok')"
NEW=$(python3 - "$SRC" "$LV" <<'PY'
import re,sys
p,lv=sys.argv[1:3];s=open(p).read()
m=re.search(r'class="ver">v(\d+)\.(\d+)\.(\d+)',s);a,b,c=map(int,m.groups())
a,b,c=(a,b+1,0) if lv=='minor' else (a,b,c+1)
v=f'v{a}.{b}.{c}';s=s[:m.start()]+f'class="ver">{v}'+s[m.end():];open(p,'w').write(s);print(v)
PY
)
python3 - "$REPO/tools/build.py" <<'PY'
import re,sys
p=sys.argv[1];s=open(p).read();s=re.sub(r"(shoot-legend-v'\+')(\d+)",lambda m:m.group(1)+str(int(m.group(2))+1),s,1);open(p,'w').write(s)
PY
python3 $REPO/tools/build.py
cd $REPO && git add -A && git commit -qm "$NEW: $MSG

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_011F3i8arvgisAS8eNXdGWUM" && git push -q
echo "released $NEW  (接著請用 Artifact 工具發佈 $SRC)"
