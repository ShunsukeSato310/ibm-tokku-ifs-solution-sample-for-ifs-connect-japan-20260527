"""
調達担当者ロビー XML マージスクリプト
datasources/*.xml + elements/*.xml → lobby_procurement.xml

ET.parseを使わず rawテキストのまま結合することで
&apos; / &lt; / &amp; などのエスケープを保持する

使い方: python3 merge.py
"""
import glob, os, uuid, re

BASE = os.path.dirname(os.path.abspath(__file__))

def load_dir_raw(subdir):
    """各XMLファイルをテキストとして読み込み、ルートタグの内容だけ返す"""
    files = sorted(glob.glob(os.path.join(BASE, subdir, "*.xml")))
    items = []
    for f in files:
        with open(f, encoding="utf-8") as fh:
            text = fh.read().strip()
        # <?xml ...?> 宣言を除去
        text = re.sub(r'<\?xml[^?]*\?>', '', text).strip()
        items.append((os.path.basename(f), text))
    return items

datasources = load_dir_raw("datasources")
elements    = load_dir_raw("elements")

page_id = str(uuid.uuid4())

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8" standalone=\'yes\'?>')
lines.append('<Page>')
lines.append('  <Author>IBM Tokku Team</Author>')
lines.append('  <Keywords>調達,購買,発注残,procurement</Keywords>')
lines.append('  <DescriptiveText>調達担当者向けロビー。発注残KPI・遅延アラート・発注残一覧・クイックリンクを集約。</DescriptiveText>')
lines.append('  <LastModified>2026-05-26-00.00.00</LastModified>')
lines.append('  <Locked>false</Locked>')
lines.append('  <Component>PURCH</Component>')
lines.append('  <AurenaLobby>true</AurenaLobby>')
lines.append(f'  <PageId>{page_id}</PageId>')
lines.append('  <PageTitle>調達担当者ロビー</PageTitle>')
lines.append('  <Layout><Groups><Group><Elements>')

for fname, text in elements:
    lines.append(f'    <!-- {fname} -->')
    for line in text.splitlines():
        lines.append('    ' + line)

lines.append('  </Elements></Group></Groups></Layout>')
lines.append('  <DataSources>')

for fname, text in datasources:
    lines.append(f'    <!-- {fname} -->')
    for line in text.splitlines():
        lines.append('    ' + line)

lines.append('  </DataSources>')
lines.append('  <Parameters/>')
lines.append('  <Translations/>')
lines.append('</Page>')

out_path = os.path.join(BASE, "lobby_procurement.xml")
with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Generated : {out_path}")
print(f"PageId    : {page_id}")
print(f"Elements  : {len(elements)} files")
print(f"DataSources: {len(datasources)} files")
