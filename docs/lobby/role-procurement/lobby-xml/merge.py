"""
調達担当者ロビー XML マージスクリプト
datasources/*.xml + elements/*.xml → lobby_procurement.xml

- rawテキスト結合でエスケープ（&apos;等）を保持
- 非UUID ID を本物のUUIDに置換（IFS Cloud は UUID必須）

使い方: python3 merge.py
"""
import glob, os, uuid, re

BASE = os.path.dirname(os.path.abspath(__file__))

def load_dir_raw(subdir):
    files = sorted(glob.glob(os.path.join(BASE, subdir, "*.xml")))
    items = []
    for f in files:
        with open(f, encoding="utf-8") as fh:
            text = fh.read().strip()
        text = re.sub(r'<\?xml[^?]*\?>', '', text).strip()
        items.append((os.path.basename(f), text))
    return items

datasources = load_dir_raw("datasources")
elements    = load_dir_raw("elements")

# --- ID マッピング: 非UUID → UUID ---
id_map = {}

def get_uuid(old_id):
    """非UUID IDを再現可能なUUIDに変換（同じ old_id は同じ UUID を返す）"""
    if old_id not in id_map:
        # uuid5: 名前空間 + 文字列から決定論的UUID生成
        id_map[old_id] = str(uuid.uuid5(uuid.NAMESPACE_DNS, old_id))
    return id_map[old_id]

def replace_ids(text):
    """<ID>xxx</ID> と <DataSourceId>xxx</DataSourceId> を UUID に置換"""
    def repl_id(m):
        val = m.group(1)
        # 既にUUID形式ならそのまま
        if re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', val):
            return m.group(0)
        return f'<ID>{get_uuid(val)}</ID>'

    def repl_ds(m):
        val = m.group(1)
        if re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', val):
            return m.group(0)
        return f'<DataSourceId>{get_uuid(val)}</DataSourceId>'

    text = re.sub(r'<ID>([^<]+)</ID>', repl_id, text)
    text = re.sub(r'<DataSourceId>([^<]+)</DataSourceId>', repl_ds, text)
    return text

page_id = str(uuid.uuid4())

# ID置換を適用
ds_items = [(f, replace_ids(t)) for f, t in datasources]
el_items = [(f, replace_ids(t)) for f, t in elements]

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8" standalone=\'yes\'?>')
lines.append('<Page>')
lines.append('  <Author>IBM Tokku Team</Author>')
lines.append('  <Keywords>調達,購買,発注残,procurement</Keywords>')
lines.append('  <DescriptiveText>調達担当者向けロビー。発注残KPI・遅延アラート・発注残一覧・クイックリンクを集約。</DescriptiveText>')
lines.append('  <LastModified>2026-05-26-12.00.00</LastModified>')
lines.append('  <Locked>false</Locked>')
lines.append('  <Component>PURCH</Component>')
lines.append('  <AurenaLobby>true</AurenaLobby>')
lines.append(f'  <PageId>{page_id}</PageId>')
lines.append('  <PageTitle>調達担当者ロビー</PageTitle>')
lines.append('  <Layout><Groups><Group><Elements>')

for fname, text in el_items:
    lines.append(f'    <!-- {fname} -->')
    for line in text.splitlines():
        lines.append('    ' + line)

lines.append('  </Elements></Group></Groups></Layout>')
lines.append('  <DataSources>')

for fname, text in ds_items:
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
print(f"Elements  : {len(el_items)} files")
print(f"DataSources: {len(ds_items)} files")
print(f"ID mappings: {len(id_map)}")
