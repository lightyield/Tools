import sys
import os
import tempfile

# ✅ srcディレクトリをimportパスに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from parser import parse_enex

def test_parse_enex():
    test_enex = '''
    <en-export>
      <note>
        <title>2025.01.01_接待交際費_スターバックス_1,100円_Aさん</title>
      </note>
      <note>
        <title>2025.01.02_旅費交通費_日本交通_3,000円_領収済</title>
      </note>
    </en-export>
    '''
    with tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8', suffix='.enex') as f:
        f.write(test_enex)
        f.seek(0)
        titles = parse_enex(f.name)
        assert len(titles) == 2
        assert "スターバックス" in titles[0]
        assert "日本交通" in titles[1]
