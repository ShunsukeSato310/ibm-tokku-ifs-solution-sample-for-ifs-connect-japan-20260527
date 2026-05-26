"""
調達担当者ロビー XML マージスクリプト
datasources.xml + elements.xml → lobby_procurement.xml
"""
import xml.etree.ElementTree as ET
import uuid, os

BASE = os.path.dirname(os.path.abspath(__file__))

ds_tree = ET.parse(os.path.join(BASE, "datasources.xml"))
el_tree = ET.parse(os.path.join(BASE, "elements.xml"))

ds_root = ds_tree.getroot()   # <DataSources>
el_root = el_tree.getroot()   # <Elements>

page_id = str(uuid.uuid4())

lines = [
    '<?xml version="1.0" encoding="UTF-8" standalone=\'yes\'?>',
    '<Page>',
    '  <Author>IBM Tokku Team</Author>',
    '  <Keywords>調達,購買,発注残,procurement</Keywords>',
    '  <DescriptiveText>調達担当者向けロビー。発注残KPI・遅延アラート・発注残一覧・クイックリンクを集約したホーム画面。</DescriptiveText>',
    '  <LastModified>2026-05-26-00.00.00</LastModified>',
    '  <Locked>false</Locked>',
    '  <Component>PURCH</Component>',
    '  <AurenaLobby>true</AurenaLobby>',
    f'  <PageId>{page_id}</PageId>',
    '  <PageTitle>調達担当者ロビー</PageTitle>',
    '  <Layout>',
    '    <Groups>',
    '      <Group>',
    '        <Elements>',
]

# elements を挿入
ET.indent(el_root, space="          ")
for child in el_root:
    lines.append("          " + ET.tostring(child, encoding="unicode"))

lines += [
    '        </Elements>',
    '      </Group>',
    '    </Groups>',
    '  </Layout>',
]

# datasources を挿入
lines.append("  <DataSources>")
ET.indent(ds_root, space="    ")
for child in ds_root:
    lines.append("    " + ET.tostring(child, encoding="unicode"))
lines.append("  </DataSources>")

lines += [
    '  <Parameters/>',
    '  <Translations/>',
    '</Page>',
]

out_path = os.path.join(BASE, "lobby_procurement.xml")
with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Generated: {out_path}")
print(f"PageId: {page_id}")
