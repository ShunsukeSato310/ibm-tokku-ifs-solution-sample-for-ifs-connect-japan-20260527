"""
調達担当者ロビー XML マージスクリプト
datasources/*.xml + elements/*.xml → lobby_procurement.xml

使い方: python3 merge.py
"""
import xml.etree.ElementTree as ET
import glob, os, uuid

BASE = os.path.dirname(os.path.abspath(__file__))

def load_dir(subdir):
    files = sorted(glob.glob(os.path.join(BASE, subdir, "*.xml")))
    nodes = []
    for f in files:
        root = ET.parse(f).getroot()
        ET.indent(root, space="    ")
        nodes.append((os.path.basename(f), root))
    return nodes

datasources = load_dir("datasources")
elements    = load_dir("elements")

page_id = str(uuid.uuid4())

out = []
out.append('<?xml version="1.0" encoding="UTF-8" standalone=\'yes\'?>')
out.append('<Page>')
out.append('  <Author>IBM Tokku Team</Author>')
out.append('  <Keywords>調達,購買,発注残,procurement</Keywords>')
out.append('  <DescriptiveText>調達担当者向けロビー。発注残KPI・遅延アラート・発注残一覧・クイックリンクを集約。</DescriptiveText>')
out.append('  <LastModified>2026-05-26-00.00.00</LastModified>')
out.append('  <Locked>false</Locked>')
out.append('  <Component>PURCH</Component>')
out.append('  <AurenaLobby>true</AurenaLobby>')
out.append(f'  <PageId>{page_id}</PageId>')
out.append('  <PageTitle>調達担当者ロビー</PageTitle>')
out.append('  <Layout><Groups><Group><Elements>')

for fname, node in elements:
    out.append(f'    <!-- {fname} -->')
    out.append('    ' + ET.tostring(node, encoding='unicode'))

out.append('  </Elements></Group></Groups></Layout>')
out.append('  <DataSources>')

for fname, node in datasources:
    out.append(f'    <!-- {fname} -->')
    out.append('    ' + ET.tostring(node, encoding='unicode'))

out.append('  </DataSources>')
out.append('  <Parameters/>')
out.append('  <Translations/>')
out.append('</Page>')

out_path = os.path.join(BASE, "lobby_procurement.xml")
with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print(f"Generated : {out_path}")
print(f"PageId    : {page_id}")
print(f"Elements  : {len(elements)} files")
print(f"DataSources: {len(datasources)} files")
