/* Nền tài chính cho con — điều hướng, tìm kiếm, ba công cụ.
   Không gọi ra mạng. Dữ liệu nằm trong localStorage của trình duyệt này. */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var esc = function (s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  };
  var pad = function (n) { return (n < 10 ? '0' : '') + n; };

  /* ================= điều hướng ================= */
  var SECS = [].slice.call(document.querySelectorAll('main section'));
  var navOl = $('chnav'), side = $('side'), scrim = $('scrim'), burger = $('burger'),
      nowEl = $('now'), ofEl = $('of'), pager = $('pager');
  var MAP = {}, cur = null, spy = null;

  SECS.forEach(function (sec, si) {
    var picks = [];
    [].slice.call(sec.querySelectorAll('h3')).forEach(function (el, hi) {
      var lab = el.textContent.replace(/\s+/g, ' ').trim();
      if (!lab) return;
      var id = sec.id + '--' + hi;
      el.id = id; el.classList.add('anchor');
      picks.push({ id: id, label: lab });
    });
    MAP[sec.id] = { sec: sec, idx: si, title: sec.dataset.title || sec.id, picks: picks };
  });

  navOl.innerHTML = SECS.map(function (sec, i) {
    var m = MAP[sec.id];
    var subs = m.picks.map(function (p) {
      return '<li><a href="#' + p.id + '" data-jump="' + p.id + '">' + esc(p.label) + '</a></li>';
    }).join('');
    return '<li data-sec="' + sec.id + '">' +
      '<button type="button" class="ch-btn" data-go="' + sec.id + '" aria-current="false">' +
      '<span class="n">' + pad(i + 1) + '</span><span>' + esc(m.title) + '</span></button>' +
      (subs ? '<ul class="sub-list">' + subs + '</ul>' : '') + '</li>';
  }).join('');

  function watch(sec) {
    if (spy) spy.disconnect();
    var as = [].slice.call(sec.querySelectorAll('.anchor'));
    if (!as.length || !window.IntersectionObserver) return;
    spy = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        [].slice.call(navOl.querySelectorAll('.sub-list a')).forEach(function (l) { l.classList.remove('on'); });
        var hit = navOl.querySelector('.sub-list a[data-jump="' + e.target.id + '"]');
        if (hit) hit.classList.add('on');
      });
    }, { rootMargin: '-12% 0px -74% 0px', threshold: 0 });
    as.forEach(function (a) { spy.observe(a); });
  }

  function buildPager(i) {
    var p = SECS[i - 1], n = SECS[i + 1];
    pager.innerHTML =
      (p ? '<button class="pg" type="button" data-go="' + p.id + '"><small>Chương trước</small><b>' + esc(MAP[p.id].title) + '</b></button>' : '<span></span>') +
      (n ? '<button class="pg pg--next" type="button" data-go="' + n.id + '"><small>Chương sau</small><b>' + esc(MAP[n.id].title) + '</b></button>' : '<span></span>');
  }

  function show(id, anchor, push) {
    var m = MAP[id]; if (!m) return;
    if (cur !== id) {
      SECS.forEach(function (s) { s.classList.toggle('live', s.id === id); });
      [].slice.call(navOl.children).forEach(function (li) {
        var on = li.getAttribute('data-sec') === id;
        li.classList.toggle('on', on);
        li.querySelector('.ch-btn').setAttribute('aria-current', on ? 'true' : 'false');
      });
      nowEl.textContent = m.title;
      ofEl.textContent = pad(m.idx + 1) + ' / ' + pad(SECS.length);
      buildPager(m.idx); watch(m.sec); cur = id;
    }
    if (push !== false) { try { history.replaceState(null, '', '#' + (anchor || id)); } catch (e) {} }
    var t = anchor ? document.getElementById(anchor) : null;
    if (t) {
      var off = (innerWidth < 1040 ? 66 : 14);
      window.scrollTo(0, Math.max(0, Math.round(t.getBoundingClientRect().top + window.pageYOffset - off)));
    } else window.scrollTo(0, 0);
  }

  function drawer(open) {
    side.classList.toggle('open', open);
    scrim.classList.toggle('on', open);
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.body.style.overflow = (open && innerWidth < 1040) ? 'hidden' : '';
  }
  burger.addEventListener('click', function () { drawer(!side.classList.contains('open')); });
  scrim.addEventListener('click', function () { drawer(false); });
  $('sidex').addEventListener('click', function () { drawer(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') drawer(false); });
  addEventListener('resize', function () {
    if (innerWidth >= 1040) { side.classList.remove('open'); scrim.classList.remove('on'); document.body.style.overflow = ''; }
  });

  document.addEventListener('click', function (e) {
    if (!e.target.closest) return;
    var g = e.target.closest('[data-go]');
    if (g) { show(g.getAttribute('data-go')); drawer(false); return; }
    var j = e.target.closest('[data-jump]');
    if (j) {
      e.preventDefault();
      var id = j.getAttribute('data-jump');
      show(id.split('--')[0], id);
      [].slice.call(navOl.querySelectorAll('.sub-list a')).forEach(function (l) { l.classList.remove('on'); });
      j.classList.add('on'); drawer(false);
    }
  });

  function route() {
    var h = (location.hash || '').replace(/^#/, '');
    if (!h) { show(SECS[0].id, null, false); return; }
    var base = h.split('--')[0];
    if (MAP[base]) show(base, h.indexOf('--') > 0 ? h : null, false);
    else show(SECS[0].id, null, false);
  }
  addEventListener('hashchange', route);
  route();

  /* ================= tìm kiếm ================= */
  function wireSearch(inputId, countId, sel, noun) {
    var input = $(inputId), out = $(countId);
    if (!input) return;
    var items = [].slice.call(document.querySelectorAll(sel));
    function run() {
      var q = input.value.trim().toLowerCase(), hit = 0;
      items.forEach(function (el) {
        var ok = !q || (el.dataset.text || '').indexOf(q) >= 0;
        el.hidden = !ok;
        if (ok) hit++;
        if (!ok && el.tagName === 'DETAILS') el.open = false;
      });
      [].slice.call(document.querySelectorAll(sel + ':first-child')).forEach(function () {});
      out.textContent = q ? (hit + ' / ' + items.length + ' ' + noun) : (items.length + ' ' + noun);
      // ẩn tiêu đề nhóm rỗng
      [].slice.call(document.querySelectorAll('.scen-list, .vocab')).forEach(function (box) {
        var any = [].slice.call(box.children).some(function (c) { return !c.hidden; });
        box.hidden = !any;
        var h = box.previousElementSibling;
        if (h && h.tagName === 'H3') h.hidden = !any;
      });
    }
    input.addEventListener('input', run);
    run();
  }
  wireSearch('q-scen', 'c-scen', '.scen', 'kịch bản');
  wireSearch('q-vocab', 'c-vocab', '.vword', 'từ');

  /* ================= lưu trữ ================= */
  var KEY = 'ntc-v1';
  var S = { fund: {}, lixi: [], moc: {} };
  try { var raw = localStorage.getItem(KEY); if (raw) S = Object.assign(S, JSON.parse(raw)); } catch (e) {}
  function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} }
  function num(v) {
    if (v === undefined || v === null) return NaN;
    var s = String(v).replace(/[^0-9,.\-]/g, '').replace(/\.(?=\d{3}\b)/g, '').replace(',', '.');
    var n = parseFloat(s); return isFinite(n) ? n : NaN;
  }
  function fmt(n) { return (Math.round(n * 10) / 10).toLocaleString('vi-VN'); }
  function today() { return new Date().toLocaleDateString('sv'); }

  /* ---------- máy tính quỹ ---------- */
  var FD = { monthly: '3', start: '0', rate: '6', infl: '4', years: '18', step: '0' };
  var FF = ['monthly', 'start', 'rate', 'infl', 'years', 'step'];
  function fval(f) {
    var v = S.fund[f];
    var n = num(v !== undefined && v !== '' ? v : FD[f]);
    return isFinite(n) ? n : num(FD[f]);
  }
  function paintFund() {
    FF.forEach(function (f) {
      var el = $('f-' + f);
      if (el) el.value = (S.fund[f] !== undefined && S.fund[f] !== '') ? S.fund[f] : FD[f];
    });
  }
  function calcFund() {
    if (!$('f-nominal')) return;
    var m = Math.max(0, fval('monthly')), s0 = Math.max(0, fval('start'));
    var r = fval('rate') / 100, inf = fval('infl') / 100, step = fval('step') / 100;
    var yrs = Math.max(1, Math.min(30, Math.round(fval('years'))));
    var mr = Math.pow(1 + r, 1 / 12) - 1;
    var bal = s0, paid = s0, rows = [];
    for (var y = 1; y <= yrs; y++) {
      var mm = m * Math.pow(1 + step, y - 1);
      for (var i = 0; i < 12; i++) { bal = (bal + mm) * (1 + mr); paid += mm; }
      rows.push({ y: y, bal: bal, real: bal / Math.pow(1 + inf, y), paid: paid });
    }
    var last = rows[rows.length - 1];
    $('f-nominal').textContent = fmt(Math.round(last.bal)) + ' triệu';
    $('f-real').textContent = 'Tương đương ' + fmt(Math.round(last.real)) +
      ' triệu theo sức mua của tiền hôm nay (lạm phát ' + fmt(inf * 100) + '%/năm).';
    $('f-break').textContent = 'Bố đã bỏ vào ' + fmt(Math.round(last.paid)) + ' triệu · phần sinh thêm ' +
      fmt(Math.round(last.bal - last.paid)) + ' triệu, tức ' +
      (last.paid > 0 ? Math.round((last.bal - last.paid) / last.paid * 100) : 0) + '% so với số đã bỏ.';
    $('f-grid').innerHTML = rows.filter(function (x) { return x.y % 3 === 0 || x.y === yrs; })
      .map(function (x) {
        return '<div><b>' + fmt(Math.round(x.real)) + '</b><span>năm ' + x.y + ' · thực</span></div>';
      }).join('');
  }
  FF.forEach(function (f) {
    var el = $('f-' + f); if (!el) return;
    el.addEventListener('input', function () { S.fund[f] = el.value; calcFund(); });
    el.addEventListener('blur', save);
  });
  if ($('f-reset')) $('f-reset').addEventListener('click', function () {
    S.fund = {}; paintFund(); calcFund(); save();
    $('f-stat').textContent = 'Đã về 6%/năm, lạm phát 4%, 18 năm.';
  });

  /* ---------- sổ lì xì ---------- */
  function renderLixi() {
    var box = $('li-log'); if (!box) return;
    var tot = 0, byYear = {};
    S.lixi.forEach(function (l) {
      tot += l.a;
      var y = String(l.d).slice(0, 4);
      byYear[y] = (byYear[y] || 0) + l.a;
    });
    $('li-total').textContent = S.lixi.length ? fmt(tot) : '—';
    $('li-count').textContent = S.lixi.length || '—';
    var ys = Object.keys(byYear).sort();
    $('li-year').textContent = ys.length ? fmt(byYear[ys[ys.length - 1]]) : '—';
    box.innerHTML = S.lixi.map(function (l, i) {
      return '<div class="log-i"><button type="button" data-delx="' + i + '">xoá</button>' +
        '<span class="m">' + esc(l.d) + '</span><br><span class="d">' + esc(l.w) + ' · ' + fmt(l.a) + ' nghìn</span></div>';
    }).join('');
  }
  if ($('li-add')) $('li-add').addEventListener('click', function () {
    var d = $('li-date').value.trim() || today(), w = $('li-who').value.trim(), a = num($('li-amt').value);
    if (!isFinite(a) || a <= 0) { $('li-stat').textContent = 'Cần nhập số tiền.'; return; }
    S.lixi.unshift({ d: d, w: w || 'Không ghi tên', a: a });
    $('li-who').value = ''; $('li-amt').value = '';
    save(); renderLixi();
    $('li-stat').textContent = 'Đã ghi vào sổ của con.';
  });

  /* ---------- sổ mốc ---------- */
  function paintMoc() {
    var btns = [].slice.call(document.querySelectorAll('button[data-ck]'));
    if (!btns.length) return;
    var done = 0;
    btns.forEach(function (b) {
      var k = b.getAttribute('data-ck'), on = !!S.moc[k];
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      var dt = b.querySelector('[data-dt]');
      if (dt) dt.textContent = on ? ('đạt ' + S.moc[k]) : '';
      if (on) done++;
    });
    var pc = Math.round(done / btns.length * 100);
    if ($('moc-bar')) $('moc-bar').style.width = pc + '%';
    if ($('moc-stat')) $('moc-stat').textContent = done ?
      ('Đã đạt ' + done + '/' + btns.length + ' mốc · ' + pc + '%') : 'Chưa tích mốc nào.';
    [].slice.call(document.querySelectorAll('.stage')).forEach(function (st) {
      var all = [].slice.call(st.querySelectorAll('button[data-ck]'));
      var d = all.filter(function (b) { return b.getAttribute('aria-pressed') === 'true'; }).length;
      var c = st.querySelector('.cnt');
      if (c) c.textContent = d + '/' + all.length;
    });
  }
  document.addEventListener('click', function (e) {
    if (!e.target.closest) return;
    var b = e.target.closest('button[data-ck]');
    if (b) {
      var k = b.getAttribute('data-ck');
      if (S.moc[k]) delete S.moc[k]; else S.moc[k] = today();
      save(); paintMoc(); return;
    }
    var dx = e.target.closest('[data-delx]');
    if (dx) { S.lixi.splice(+dx.getAttribute('data-delx'), 1); save(); renderLixi(); }
  });

  /* ---------- in ra giấy: mở hết phần thu gọn ---------- */
  var reopened = [];
  addEventListener('beforeprint', function () {
    reopened = [].slice.call(document.querySelectorAll('details:not([open])'));
    reopened.forEach(function (d) { d.open = true; });
  });
  addEventListener('afterprint', function () {
    reopened.forEach(function (d) { d.open = false; });
    reopened = [];
  });

  /* ---------- khởi động ---------- */
  if ($('li-date')) $('li-date').value = today();
  paintFund(); calcFund(); renderLixi(); paintMoc();
})();
