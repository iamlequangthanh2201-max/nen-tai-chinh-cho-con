#!/usr/bin/env python3
"""Dựng index.html từ các file .md nội dung.

Sửa nội dung ở file .md rồi chạy:  python3 build.py
"""
import html, re, pathlib

HERE = pathlib.Path(__file__).parent

CHAPTERS = [
    dict(id="nenmong", file="01-nen-mong.md", num="01", hero="c1",
         shape="sh-s", title="Nền móng",
         lede="Một nguyên tắc bao trùm, ba trụ, và bảy việc không được phép trong nhà."),
    dict(id="truockhisinh", file="02-truoc-khi-sinh.md", num="02", hero="c2",
         shape="sh-r",
         title="Trước khi con ra đời",
         lede="Sáu việc của bố mẹ. Chương này không có đứa trẻ nào trong đó."),
    dict(id="lotrinh", file="03-lo-trinh.md", num="03", hero="c3",
         shape="sh-b",
         title="Lộ trình 0–18",
         lede="Năm chặng, bảng tiền tiêu vặt theo tuổi, và bảng bốn ô ưu tiên chi tiêu."),
    dict(id="kichban", file="04-kich-ban.md", num="04", hero="c4",
         shape="sh-q",
         title="31 kịch bản",
         lede="Đọc trước lúc bình tĩnh. Giữa cơn thì không ai tra sổ tay — thứ chạy lúc đó là phản xạ."),
    dict(id="nghithuc", file="05-nghi-thuc-cong-cu.md", num="05", hero="c5",
         shape="sh-c",
         title="Nghi thức & công cụ",
         lede="Bốn nghi thức chạy suốt mười tám năm, và ba công cụ gắn vào chúng."),
    dict(id="tongket", file="06-tong-ket.md", num="06", hero="c6",
         shape="sh-a",
         title="Nên làm · Nên tránh · Dấu hiệu",
         lede="Một trang để dán, và bộ dấu hiệu tự chẩn đoán theo ba trụ."),
    dict(id="tuvung", file="07-tu-vung.md", num="PL", hero="c7",
         shape="sh-p",
         title="Từ vựng con cần nghe",
         lede="Ba mươi từ bố mẹ cố ý dùng trong đời sống thật, kèm câu mẫu và dấu hiệu con đã nắm."),
]

MOC = [
    ("0–3 tuổi", [
        ("Con đợi được vài phút sau câu “chờ bố một chút”", "sang chặng 3–6 tuổi"),
    ]),
    ("3–6 tuổi", [
        ("Nghe được “hôm nay mình không mua” mà không sụp đổ", "bắt đầu ba lọ Tiêu · Để dành · Cho"),
        ("Biết lọ nào dùng để làm gì", "mở ví tiêu vặt, sang chặng 6–10"),
    ]),
    ("6–10 tuổi", [
        ("Tự trả tiền ở quầy", "con cầm tiền đi mua một mình"),
        ("Ba tuần liền không hết tiền giữa tuần", "chuyển sang nhận theo tháng"),
        ("Để dành đến đích ít nhất một lần", "đặt mục tiêu dài hơn"),
        ("Hỏi giá trước khi đòi mua", "dùng đủ bảng bốn ô"),
    ]),
    ("11–14 tuổi", [
        ("Sống hết tháng, hai tháng liên tiếp", "giao thêm một khoản con tự mua"),
        ("Tự nói ra lý do đằng sau một quyết định mua", "tham gia một quyết định thật của nhà"),
        ("Tự xếp khoản chi vào bốn ô trước khi tiêu", "mở tài khoản cho phần để dành"),
    ]),
    ("15–18 tuổi", [
        ("Tự đối chiếu số dư tài khoản", "chuyển khoản toàn bộ, bố mẹ không xem lịch sử"),
        ("Từng tự từ chối một khoản mua vì hết ngân sách", "tự quyết rút sổ lì xì"),
        ("Vẫn kể với bố khi gặp chuyện tiền", "bàn giao quỹ 18 năm"),
    ]),
]

# ---------- markdown tối giản ----------
def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
    return s


LAB_SAY = re.compile(r'^(Nói|Làm|Ví dụ)\b')
LAB_NO = re.compile(r'^(Đừng nói|Không)\b')

def split_label(txt):
    """'**Nói:** "..."' → ('Nói', '"..."'); không có nhãn → (None, txt)."""
    m = re.match(r'\*\*(.+?):\*\*\s*(.*)$', txt)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    m = re.match(r'\*\*(.+?)\*\*$', txt)
    if m:
        return None, txt
    return None, txt

def lab_class(lab):
    if not lab: return ''
    if LAB_NO.match(lab): return ' lab-no'
    if LAB_SAY.match(lab): return ' lab-say'
    return ''

def render_list(items):
    """Danh sách thường, hai cấp."""
    o, li, sub = ['<ul>'], False, False
    for d, txt in items:
        if d == 0:
            if sub: o.append('</ul>'); sub = False
            if li: o.append('</li>')
            o.append('<li>' + inline(txt)); li = True
        else:
            if not li: o.append('<li>'); li = True
            if not sub: o.append('<ul class="sub">'); sub = True
            lab, rest = split_label(txt)
            o.append('<li class="' + (lab_class(lab).strip() or 'plain') + '">' + inline(txt) + '</li>')
    if sub: o.append('</ul>')
    if li: o.append('</li>')
    o.append('</ul>')
    return ''.join(o)

def split_title(head):
    """'**Tiêu đề** — việc cần làm' → ('Tiêu đề', 'việc cần làm')."""
    m = re.match(r'^\*\*(.+?)\*\*(?:\s*—\s*(.*))?$', head.strip())
    if m:
        return m.group(1).strip(), (m.group(2) or '').strip()
    return None, ''

ORDER = {'Ví dụ': 0, 'Nói': 0, 'Làm': 1, 'Đừng nói': 2, 'Hệ quả': 3, 'Vì sao': 3}

def render_rows(items):
    """Hàng trong khối Nên làm / Nên tránh và trong thân kịch bản.
    Dòng thu gọn: tiêu đề + việc cần làm. Phần mở ra: câu mẫu, câu tránh, lý do.
    Hai phần không bao giờ lặp nội dung của nhau."""
    groups = []
    for d, txt in items:
        if d == 0:
            groups.append([txt, []])
        elif groups:
            groups[-1][1].append(txt)
    o = ['<ul class="rows">']
    for head, kids in groups:
        title, action = split_title(head)
        if title is None:
            # hàng có nhãn ở đầu — dùng trong kịch bản
            lab, rest = split_label(head)
            if lab:
                o.append('<li class="r--flat' + lab_class(lab) + '">'
                         '<span class="lab">' + inline(lab) + '</span>'
                         '<span class="ra">' + inline(rest) + '</span></li>')
            else:
                o.append('<li class="r--flat"><span class="ra">' + inline(head) + '</span></li>')
            continue
        ra = ('<span class="ra">' + inline(action) + '</span>') if action else ''
        if not kids:
            o.append('<li class="r--flat"><span class="rt">' + inline(title) + '</span>' + ra + '</li>')
            continue
        rows = []
        for k in kids:
            kl, kr = split_label(k)
            rows.append((ORDER.get(kl, 9), kl or 'Ghi chú', kr))
        # không có dòng việc cần làm thì lấy dòng 'Làm' lên, và bỏ khỏi phần mở ra
        if not action:
            for idx, (_, kl, kr) in enumerate(rows):
                if kl == 'Làm':
                    action = kr
                    ra = '<span class="ra">' + inline(action) + '</span>'
                    rows.pop(idx)
                    break
        rows.sort(key=lambda x: x[0])
        o.append('<li><details class="r"><summary>'
                 '<span class="rt">' + inline(title) + '</span>' + ra +
                 '</summary><div class="rmore">')
        for _, kl, kr in rows:
            cls = (lab_class(kl) or '').replace('lab-', '').strip()
            o.append('<p class="' + cls + '"><b>' + inline(kl) + '</b>' + inline(kr) + '</p>')
        o.append('</div></details></li>')
    o.append('</ul>')
    return ''.join(o)


def render_block(head, inner):
    """::: grp y | Tiêu đề   ·   ::: stage Tuổi | phụ đề   ·   ::: tl"""
    parts = [x.strip() for x in head.split('|')]
    spec = parts[0].split()
    kind = spec[0]
    if kind == 'grp':
        tone = spec[1] if len(spec) > 1 else 'y'
        title = parts[1] if len(parts) > 1 else ''
        return ('<div class="grp grp--' + tone + '"><div class="grp-h">' + inline(title) + '</div>'
                + md(inner, rows=True) + '</div>')
    if kind == 'stage':
        age = ' '.join(spec[1:])
        sub = parts[1] if len(parts) > 1 else ''
        return ('<div class="tl-i"><div class="tl-age"><b>' + inline(age) + '</b>'
                + ('<span>' + inline(sub) + '</span>' if sub else '')
                + '</div><div class="tl-card">' + md(inner) + '</div></div>')
    if kind == 'tl':
        return '<div class="tl">' + md(inner) + '</div>'
    if kind == 'rows':
        return md(inner, rows=True)
    return md(inner)

def md(lines, rows=False):
    """Chuyển một khối markdown thành HTML. rows=True: danh sách dựng thành hàng."""
    out, i = [], 0
    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if not s:
            i += 1; continue
        if s.startswith(':::'):
            head = s[3:].strip()
            depth, j, inner = 1, i + 1, []
            while j < len(lines):
                t = lines[j].strip()
                if t.startswith(':::') and t != ':::':
                    depth += 1
                elif t == ':::':
                    depth -= 1
                    if depth == 0: break
                inner.append(lines[j]); j += 1
            i = j + 1
            out.append(render_block(head, inner))
            continue
        if s.startswith('<!--'):
            out.append(s); i += 1; continue
        if s == '---':
            out.append('<hr>'); i += 1; continue
        if s.startswith('#'):
            lvl = len(s) - len(s.lstrip('#'))
            txt = s.lstrip('#').strip()
            tag = 'h3' if lvl <= 2 else 'h4'
            out.append(f'<{tag}>{inline(txt)}</{tag}>'); i += 1; continue
        if s.startswith('|'):
            tbl = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                tbl.append(lines[i].strip()); i += 1
            cells = lambda r: [c.strip() for c in r.strip('|').split('|')]
            head = cells(tbl[0])
            body = [cells(r) for r in tbl[2:]]
            h = ''.join(f'<th>{inline(c)}</th>' for c in head)
            b = ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in body)
            out.append(f'<div class="tw"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>')
            continue
        if s.startswith('> '):
            q = []
            while i < len(lines) and lines[i].strip().startswith('> '):
                q.append(lines[i].strip()[2:]); i += 1
            out.append('<blockquote><p>' + '<br>'.join(inline(x) for x in q) + '</p></blockquote>')
            continue
        if s.startswith('- '):
            items = []
            while i < len(lines):
                raw = lines[i]
                st = raw.strip()
                if st.startswith('- '):
                    items.append([1 if raw.startswith('  ') else 0, st[2:]])
                    i += 1
                elif st and raw.startswith(' ') and items:
                    # dòng tiếp theo của cùng một gạch đầu dòng — nối vào, đừng thả ra ngoài
                    items[-1][1] += ' ' + st
                    i += 1
                else:
                    break
            out.append(render_rows(items) if rows else render_list(items))
            continue
        # đoạn văn
        p = []
        while i < len(lines) and lines[i].strip() and not re.match(r'^\s*(#|\||>|- |---)', lines[i]) \
                and not lines[i].strip().startswith('<!--'):
            p.append(lines[i].strip()); i += 1
        txt = ' '.join(p)
        m = re.match(r'^\*?Cơ sở:\s*(.*?)\*?$', txt)
        if m:
            out.append('<details class="src"><summary>Cơ sở</summary><p>'
                       + inline(m.group(1)) + '</p></details>')
            continue
        cls = ' class="tip"' if txt.startswith('**') and len(txt) > 120 else ''
        out.append(f'<p{cls}>{inline(txt)}</p>')
    return '\n'.join(out)

# ---------- các khối đặc biệt ----------
def build_scenarios(body):
    """04-kich-ban.md → danh sách <details class="scen">."""
    intro = re.split(r'(?m)^# Nhóm', body)[0]
    out = [md(intro.split('\n'))]
    blocks = re.split(r'\n(?=# Nhóm )', body)
    for blk in blocks:
        m = re.match(r'# (Nhóm [^\n]+)', blk)
        if not m:
            continue
        out.append(f'<h3>{inline(m.group(1))}</h3>')
        items = re.split(r'\n(?=## )', blk)[1:]
        out.append('<div class="scen-list">')
        for it in items:
            lines = it.strip().split('\n')
            head = lines[0][3:].strip()
            code, title = head.split('·', 1)
            code, title = code.strip(), title.strip()
            hard = title.endswith('★')
            title = title.rstrip('★').strip()
            meta, rest = '', lines[1:]
            if len(lines) > 1 and re.match(r'^\*[^*].*\*$', lines[1].strip()):
                meta = lines[1].strip().strip('*')
                rest = lines[2:]
            age = meta.split('·')[0].strip() if meta else ''
            why = ''
            if rest and rest[-1].strip().startswith('*') and rest[-1].strip().endswith('*'):
                why = rest[-1].strip().strip('*'); rest = rest[:-1]
            inner = md(rest, rows=True)
            txt = html.escape(' '.join([code, title, meta, ' '.join(rest)]).lower(), quote=True)
            star = ' <span class="hard">★</span>' if hard else ''
            out.append(
                f'<details class="scen" data-text="{txt}">'
                f'<summary class="{"" if age else "noage"}"><span class="scode">{inline(code)}</span>'
                f'<span class="stitle">{inline(title)}{star}</span>'
                + (f'<span class="sage">{inline(age)}</span>' if age else '') + '</summary>'
                f'<div class="sbody">{inner}'
                + (f'<span class="why">{inline(why)}</span>' if why else '')
                + '</div></details>')
        out.append('</div>')
    return '\n'.join(out)

def build_vocab(body):
    """07-tu-vung.md → thẻ từ vựng có thể lọc."""
    head = body.split('---', 1)[0]
    out = [md(head.split('\n'))]
    for blk in re.split(r'\n(?=## )', body)[1:]:
        lines = blk.strip().split('\n')
        group = lines[0][3:].strip()
        out.append(f'<h3>{inline(group)}</h3><div class="vocab">')
        for entry in re.split(r'\n\n', '\n'.join(lines[1:])):
            e = entry.strip()
            if not e.startswith('**'):
                continue
            el = e.split('\n')
            m = re.match(r'\*\*(.+?)\*\* · (.+)', el[0])
            if not m:
                continue
            word, age = m.group(1), m.group(2)
            quote = next((x[2:].strip() for x in el if x.startswith('> ')), '')
            sig = next((x.strip().replace('*', '') for x in el if x.strip().startswith('*Con đã nắm')), '')
            txt = html.escape(f'{word} {age} {quote} {sig}'.lower(), quote=True)
            out.append(
                f'<div class="vword" data-text="{txt}"><b>{inline(word)}</b>'
                f'<span class="age">{inline(age)}</span>'
                f'<q>{inline(quote)}</q><span class="sig">{inline(sig)}</span></div>')
        out.append('</div>')
    return '\n'.join(out)

WIDGETS = {}
WIDGETS['quy'] = '''
<div class="card" id="quy">
 <h4>Máy tính quỹ 18 năm</h4>
 <p>Công cụ ước tính theo giả định bố tự nhập — không phải cam kết lợi suất. Đơn vị: triệu đồng.</p>
 <div class="fld fld--2">
  <div><label for="f-monthly">Nạp mỗi tháng <span>Số tiền đều đặn hằng tháng.</span></label>
   <input type="text" id="f-monthly" inputmode="decimal" placeholder="3"></div>
  <div><label for="f-start">Có sẵn ban đầu <span>Để trống nếu bắt đầu từ 0.</span></label>
   <input type="text" id="f-start" inputmode="decimal" placeholder="0"></div>
  <div><label for="f-rate">Lợi suất mỗi năm (%) <span>Mặc định 6 — mức thận trọng.</span></label>
   <input type="text" id="f-rate" inputmode="decimal" placeholder="6"></div>
  <div><label for="f-infl">Lạm phát mỗi năm (%) <span>Mặc định 4 — để quy về sức mua hôm nay.</span></label>
   <input type="text" id="f-infl" inputmode="decimal" placeholder="4"></div>
  <div><label for="f-years">Số năm nạp <span>Từ bây giờ đến năm con 18 tuổi.</span></label>
   <input type="text" id="f-years" inputmode="decimal" placeholder="18"></div>
  <div><label for="f-step">Tăng mức nạp mỗi năm (%) <span>Để 0 nếu giữ nguyên.</span></label>
   <input type="text" id="f-step" inputmode="decimal" placeholder="0"></div>
 </div>
 <div class="out">
  <span class="cap">Quỹ khi con mười tám tuổi</span>
  <span class="big" id="f-nominal">—</span>
  <p id="f-real">—</p>
  <p id="f-break">—</p>
 </div>
 <div class="grid-y" id="f-grid"></div>
 <div class="tools" style="margin-top:14px">
  <button class="btn btn--q" id="f-reset" type="button">Về giả định mặc định</button>
  <span class="jstat" id="f-stat">Sửa số nào cũng tính lại ngay · giả định được lưu lại</span>
 </div>
</div>'''

WIDGETS['lixi'] = '''
<div class="card" id="lixi">
 <h4>Sổ lì xì của con</h4>
 <p>Ghi trước mặt con — đó mới là phần có tác dụng. Đơn vị: nghìn đồng.</p>
 <div class="li-row">
  <div><label class="fld" for="li-date" style="margin:0 0 5px;font-size:12.5px;font-weight:600">Ngày</label>
   <input type="text" id="li-date" placeholder="2027-02-06"></div>
  <div><label for="li-who" style="display:block;margin:0 0 5px;font-size:12.5px;font-weight:600">Người mừng</label>
   <input type="text" id="li-who" placeholder="Ông bà nội"></div>
  <div><label for="li-amt" style="display:block;margin:0 0 5px;font-size:12.5px;font-weight:600">Số tiền</label>
   <input type="text" id="li-amt" inputmode="decimal" placeholder="500"></div>
  <button class="btn" id="li-add" type="button">Thêm vào sổ</button>
 </div>
 <div class="stats">
  <div class="stat"><b id="li-total">—</b><span>Tổng đã ghi · nghìn đồng</span></div>
  <div class="stat"><b id="li-count">—</b><span>Số lần được mừng</span></div>
  <div class="stat"><b id="li-year">—</b><span>Năm gần nhất</span></div>
 </div>
 <span class="jstat" id="li-stat"></span>
 <div class="log" id="li-log"></div>
</div>'''

def widget_moc():
    out = ['<div class="card" id="moc"><h4>Sổ mốc của con</h4>',
           '<p>Mốc không phải để khen. Mốc là thứ mở thêm quyền tự quản cho con.</p>',
           '<div class="bar"><i id="moc-bar" style="width:0%"></i></div>',
           '<span class="jstat" id="moc-stat">Chưa tích mốc nào.</span>']
    n = 0
    for gi, (stage, items) in enumerate(MOC):
        opened = ' open' if gi == 0 else ''
        out.append(f'<details class="stage"{opened}><summary>{html.escape(stage)}'
                   f'<span class="cnt" data-cnt="{gi}"></span></summary><ul class="ck">')
        for label, opens in items:
            out.append(
                f'<li><button type="button" data-ck="m{n}" aria-pressed="false">'
                f'<span class="box" aria-hidden="true"></span>'
                f'<span><span class="t">{html.escape(label)}</span>'
                f'<span class="w">→ mở: {html.escape(opens)}</span>'
                f'<span class="dt" data-dt="m{n}"></span></span></button></li>')
            n += 1
        out.append('</ul></details>')
    out.append('</div>')
    return '\n'.join(out)

WIDGETS['moc'] = widget_moc()

# ---------- dựng trang ----------
def section(ch):
    raw = (HERE / ch['file']).read_text(encoding='utf-8')
    body = re.sub(r'^# [^\n]+\n', '', raw, count=1).strip()
    if ch['id'] == 'kichban':
        inner = build_scenarios(body)
        tools = ('<div class="searchbox"><div class="tools"><div class="search">'
                 '<input type="text" id="q-scen" placeholder="Tìm kịch bản: “ăn vạ”, “lì xì”, “game”…" '
                 'autocomplete="off"></div><span class="count" id="c-scen"></span></div>'
                 '<span class="hint">Khi không nhớ nổi gì, câu chờ vạn năng: '
                 '<b>“Bố cần một phút, rồi mình nói tiếp.”</b></span></div>')
    elif ch['id'] == 'tuvung':
        inner = build_vocab(body)
        tools = ('<div class="searchbox"><div class="tools"><div class="search">'
                 '<input type="text" id="q-vocab" placeholder="Tìm từ: “lãi kép”, “hớ”, “ngân sách”…" '
                 'autocomplete="off"></div><span class="count" id="c-vocab"></span></div>'
                 '<span class="hint">Đây là từ <b>bố mẹ cố ý dùng trong đời sống thật</b>, '
                 'không phải bài học để dạy con. Mỗi kết quả có kèm độ tuổi.</span></div>')
    else:
        inner = md(body.split('\n'))
        tools = ''
    for k, v in WIDGETS.items():
        inner = inner.replace(f'<!--WIDGET:{k}-->', v)
    return (f'<section id="{ch["id"]}" data-title="{html.escape(ch["title"])}">\n'
            f'<header class="chero {ch["hero"]}">'
            f'<span class="cshape {ch.get("shape", "sh-c")}" aria-hidden="true"></span>'
            f'<span class="pnum">Chương {ch["num"]}</span>'
            f'<h2>{html.escape(ch["title"])}</h2>'
            f'<p class="lede">{html.escape(ch["lede"])}</p></header>\n'
            f'{tools}\n{inner}\n</section>')

PAGE = '''<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nền tài chính cho con</title>
<meta name="description" content="Sổ tay của người cha: xây nền tảng tư duy và thói quen tài chính cho con, từ thai kỳ đến năm con 18 tuổi.">
<meta name="color-scheme" content="light">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@700;800&family=Be+Vietnam+Pro:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>💸</text></svg>">
</head>
<body>
<div class="app">
  <header class="topbar">
    <button class="burger" id="burger" type="button" aria-expanded="false" aria-controls="side"><i aria-hidden="true"></i><span>Mục lục</span></button>
    <span class="now" id="now">&nbsp;</span>
    <span class="of" id="of">&nbsp;</span>
  </header>
  <aside class="side" id="side" aria-label="Mục lục">
    <div class="side-head">
      <b><span class="bmoji" aria-hidden="true">💸</span>Nền tài chính cho con</b>
      <button class="side-x" id="sidex" type="button" aria-label="Đóng mục lục">&times;</button>
    </div>
    <nav class="side-nav"><ol id="chnav"></ol></nav>
  </aside>
  <main class="doc">
    <div class="doc-in">
__SECTIONS__
      <nav class="pager" id="pager" aria-label="Chuyển chương"></nav>
      <footer>
        Con sao chép cách bố sống với tiền, không sao chép lời bố giảng.
        <br><br>Trang tĩnh, không gọi ra mạng ngoài phông chữ, không theo dõi.
        Mọi thứ bố ghi ở chương 05 chỉ nằm trên trình duyệt này.
      </footer>
    </div>
  </main>
  <div class="scrim" id="scrim"></div>
</div>
<script src="app.js"></script>
</body>
</html>
'''

def main():
    secs = '\n\n'.join(section(c) for c in CHAPTERS)
    (HERE / 'index.html').write_text(PAGE.replace('__SECTIONS__', secs), encoding='utf-8')
    print('index.html:', (HERE / 'index.html').stat().st_size, 'bytes')

if __name__ == '__main__':
    main()
