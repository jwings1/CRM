/* Banco: Brambilla CRM interface. No dependencies. Talks to the CRM's own HubSpot-style API (same origin). */
(function () {
  'use strict';
  var app = document.getElementById('app');
  var store = {
    get: function (k) { try { return localStorage.getItem(k) || ''; } catch (e) { return ''; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  /* ---------- helpers ---------- */
  function h(tag, attrs) {
    var el = document.createElement(tag);
    attrs = attrs || {};
    Object.keys(attrs).forEach(function (k) {
      var v = attrs[k];
      if (v == null || v === false) return;
      if (k === 'class') el.className = v;
      else if (k.slice(0, 2) === 'on') el.addEventListener(k.slice(2), v);
      else if (k === 'text') el.textContent = v;
      else el.setAttribute(k, v === true ? '' : v);
    });
    for (var i = 2; i < arguments.length; i++) add(el, arguments[i]);
    return el;
  }
  function add(el, c) {
    if (c == null || c === false) return;
    if (Array.isArray(c)) c.forEach(function (x) { add(el, x); });
    else el.appendChild(typeof c === 'object' ? c : document.createTextNode(String(c)));
  }
  function svg(d) {
    var s = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    s.setAttribute('viewBox', '0 0 24 24'); s.setAttribute('aria-hidden', 'true');
    var p = document.createElementNS('http://www.w3.org/2000/svg', 'path'); p.setAttribute('d', d); s.appendChild(p);
    return s;
  }
  var ICON = {
    co: 'M4 21V5a1 1 0 0 1 1-1h9a1 1 0 0 1 1 1v16M15 9h4a1 1 0 0 1 1 1v11M3 21h18M8 8h3M8 12h3M8 16h3',
    ct: 'M16 19v-1a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v1M10 10a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM20 19v-1a3.5 3.5 0 0 0-2.5-3.35M15.5 4.2a3 3 0 0 1 0 5.6',
    dl: 'M4 4h4v16H4zM10 4h4v10h-4zM16 4h4v7h-4z',
    tk: 'M3 7h18v3a2 2 0 0 0 0 4v3H3v-3a2 2 0 0 0 0-4zM14 7v10',
    moon: 'M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z',
    chat: 'M4 5h16v11H9l-5 4z',
    note: 'M6 3h9l4 4v14H6zM14 3v5h5M9 13h7M9 17h5',
    call: 'M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z',
    email: 'M3 5h18v14H3zM3 7l9 7 9-7',
    meeting: 'M4 6h16v14H4zM4 10h16M8 3v4M16 3v4'
  };
  var CUR = { EUR: '€', USD: '$', GBP: '£' };
  function money(v, cur) {
    if (v == null || v === '') return '—';
    var n = Number(v); if (isNaN(n)) return '—';
    var s = Math.abs(n).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    return (n < 0 ? '−' : '') + (CUR[cur || 'EUR'] || '€') + s;
  }
  function toEur(v, cur) { var n = Number(v) || 0; return cur === 'USD' ? n * 0.92 : cur === 'GBP' ? n * 1.17 : n; }
  function date(v, withYear) {
    if (!v) return '—';
    var d = new Date(/^\d+$/.test(String(v)) ? Number(v) : v);
    if (isNaN(d)) return '—';
    return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: withYear === false ? undefined : 'numeric' });
  }
  function initials(s) { return (s || '?').split(/[\s.@]+/).filter(Boolean).slice(0, 2).map(function (w) { return w[0].toUpperCase(); }).join(''); }
  function nameFromEmail(e) {
    if (!e) return '';
    return e.split('@')[0].split('.').map(function (w) { return w.charAt(0).toUpperCase() + w.slice(1); }).join(' ');
  }
  function repCell(email) {
    if (!email) return h('span', { class: 'unassigned', title: 'No current owner: the previous rep has left Brambilla' }, 'Unassigned');
    return h('span', { class: 'rep' }, h('span', { class: 'avatar' }, initials(nameFromEmail(email))), nameFromEmail(email));
  }
  function toast(msg, bad) {
    var t = h('div', { class: 'toast' + (bad ? ' bad' : ''), role: 'status' }, msg);
    document.body.appendChild(t); setTimeout(function () { t.remove(); }, 4200);
  }

  /* ---------- api ---------- */
  function api(path, opts) {
    opts = opts || {};
    var tok = store.get('crm_token');
    return fetch(tok ? path : '/ui-api' + path, {
      method: opts.method || 'GET',
      headers: Object.assign({ 'Content-Type': 'application/json' }, tok ? { Authorization: 'Bearer ' + tok } : {}),
      body: opts.body ? JSON.stringify(opts.body) : undefined
    }).then(function (r) {
      if (r.status === 401 && tok) { store.set('crm_token', ''); throw new Error('The access token was not accepted.'); }
      if (r.status === 204) return null;
      return r.json().catch(function () { return {}; }).then(function (j) {
        if (!r.ok) { var e = new Error(j.message || ('Request failed (' + r.status + ')')); e.status = r.status; throw e; }
        return j;
      });
    });
  }
  function search(type, body) { return api('/crm/v3/objects/' + type + '/search', { method: 'POST', body: body }); }
  function batchRead(type, ids, props) {
    ids = ids.filter(function (x, i) { return ids.indexOf(x) === i; });
    if (!ids.length) return Promise.resolve([]);
    var chunks = []; for (var i = 0; i < ids.length; i += 100) chunks.push(ids.slice(i, i + 100));
    return Promise.all(chunks.map(function (c) {
      return api('/crm/v3/objects/' + type + '/batch/read', { method: 'POST', body: { properties: props, inputs: c.map(function (id) { return { id: id }; }) } });
    })).then(function (rs) { return [].concat.apply([], rs.map(function (r) { return r.results || []; })); });
  }
  function assoc(from, id, to) {
    return api('/crm/v3/objects/' + from + '/' + id + '/associations/' + to).then(function (r) {
      return (r.results || []).map(function (x) { return String(x.toObjectId); });
    }).catch(function () { return []; });
  }
  /* map of source id -> first associated id, for many records at once */
  function assocMap(from, to, ids) {
    if (!ids.length) return Promise.resolve({});
    return api('/crm/v4/associations/' + from + '/' + to + '/batch/read', { method: 'POST', body: { inputs: ids.map(function (id) { return { id: id }; }) } })
      .then(function (r) {
        var m = {};
        (r.results || []).forEach(function (x) { if (x.to && x.to.length) m[String(x.from.id)] = String(x.to[0].toObjectId); });
        return m;
      }).catch(function () { return {}; });
  }
  var pipelinesCache = {};
  function pipelines(type) {
    if (pipelinesCache[type]) return Promise.resolve(pipelinesCache[type]);
    return api('/crm/v3/pipelines/' + type).then(function (r) {
      (r.results || []).forEach(function (p) { p.stages.sort(function (a, b) { return a.displayOrder - b.displayOrder; }); });
      return (pipelinesCache[type] = r.results || []);
    });
  }

  /* ---------- shell and routing ---------- */
  var NAV = [
    { href: '/companies', label: 'Companies', ic: 'co' },
    { href: '/contacts', label: 'Contacts', ic: 'ct' },
    { href: '/deals', label: 'Deals', ic: 'dl' },
    { href: '/tickets', label: 'Tickets', ic: 'tk' }
  ];
  var mainEl;
  function shell(active) {
    var path = location.pathname;
    var nav = h('nav', { class: 'nav', 'aria-label': 'Main' },
      h('div', { class: 'brand' }, h('i', {}, 'B'), h('div', {}, h('b', {}, 'BANCO'), h('small', {}, 'Brambilla Forniture S.p.A.'))),
      h('div', {}, h('h6', {}, 'Records'), NAV.map(function (n) {
        var a = h('a', { href: n.href, 'data-link': '' }, svg(ICON[n.ic]), n.label);
        if (active === n.href) a.setAttribute('aria-current', 'page');
        return a;
      })),
      h('div', {}, h('h6', {}, 'Lists'),
        (function () { var a = h('a', { href: '/dormant', 'data-link': '' }, svg(ICON.moon), 'Clienti dormienti'); if (active === '/dormant') a.setAttribute('aria-current', 'page'); return a; })()));
    var q = h('input', { class: 'search', type: 'search', 'aria-label': 'Search companies', placeholder: 'Search companies by name, domain or P.IVA…' });
    q.addEventListener('keydown', function (e) { if (e.key === 'Enter') go('/companies?q=' + encodeURIComponent(q.value)); });
    mainEl = h('main', {});
    app.replaceChildren(h('div', { class: 'shell' }, nav,
      h('div', { class: 'content' },
        h('header', { class: 'top' }, q, h('span', { class: 'grow' }),
          h('button', { class: 'btn dark', type: 'button', onclick: openAssistant }, 'Ask the assistant')),
        mainEl)));
    return mainEl;
  }
  function go(url) { history.pushState({}, '', url); route(); }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[data-link]');
    if (a && !e.metaKey && !e.ctrlKey && a.target !== '_blank') { e.preventDefault(); go(a.getAttribute('href')); }
  });
  window.addEventListener('popstate', route);

  function route() {
    var p = location.pathname.replace(/\/+$/, '') || '/';
    var m;
    closeDetail();
    if (p === '/' || p === '/companies') return companiesList();
    if ((m = p.match(/^\/companies\/(\d+)$/))) return companyPage(m[1]);
    if (p === '/contacts') return contactsList();
    if (p === '/deals') return dealsBoard();
    if (p === '/tickets') return ticketsView();
    if (p === '/dormant') return dormantList();
    shell('');
    mainEl.appendChild(h('div', { class: 'empty' }, h('b', {}, 'Page not found'), h('a', { href: '/companies', 'data-link': '' }, 'Go to companies')));
  }
  function loading(el) { el.replaceChildren(h('div', { class: 'empty', role: 'status' }, 'Loading…')); }
  function fail(el, e) { el.replaceChildren(h('div', { class: 'err', role: 'alert' }, 'Could not load this page. ' + (e && e.message ? e.message : ''))); }

  /* Reading is public. Changing data (moving a deal, the assistant) needs the access token. */
  function askToken(then) {
    if (store.get('crm_token')) return then();
    var t = h('input', { id: 'tok', type: 'password', autocomplete: 'off', placeholder: 'Access token' });
    var u = h('input', { id: 'usr', type: 'email', placeholder: 'you@brambillaforniture.it', value: store.get('crm_user') });
    var box = h('div', { class: 'drawer', style: 'top:20vh;bottom:auto;right:50%;transform:translateX(50%);border:1px solid #DCDFDD;border-radius:10px' },
      h('form', { class: 'login', style: 'margin:0;padding:20px', onsubmit: function (e) {
        e.preventDefault(); store.set('crm_token', t.value.trim()); store.set('crm_user', u.value.trim()); box.remove(); then();
      } },
        h('h2', {}, 'Sign in to make changes'),
        h('label', { for: 'tok' }, 'Access token'), t,
        h('label', { for: 'usr' }, 'Your work email (used for “my customers”)'), u,
        h('div', { class: 'row' }, h('button', { class: 'btn primary', type: 'submit' }, 'Continue'), h('button', { class: 'btn', type: 'button', onclick: function () { box.remove(); } }, 'Cancel'))));
    document.body.appendChild(box); t.focus();
  }

  /* ---------- companies list ---------- */
  var CO_PROPS = ['name', 'domain', 'city', 'state', 'partita_iva', 'fatturato_2025', 'classe_cliente', 'id_legacy'];
  function companiesList() {
    var el = shell('/companies');
    var qs = new URLSearchParams(location.search), q = qs.get('q') || '', stack = [], after;
    var body = h('div', { class: 'card' });
    el.append(h('div', { class: 'row' }, h('h1', {}, q ? 'Search: ' + q : 'Companies')), body);
    function load() {
      loading(body);
      var req = { limit: 25, properties: CO_PROPS, sorts: [{ propertyName: 'fatturato_2025', direction: 'DESCENDING' }] };
      if (q) req.query = q;
      if (after) req.after = after;
      search('companies', req).then(function (r) {
        var rows = (r.results || []).map(function (c) {
          var p = c.properties;
          return h('tr', { class: 'click', onclick: function () { go('/companies/' + c.id); } },
            h('td', {}, h('a', { href: '/companies/' + c.id, 'data-link': '', style: 'font-weight:600' }, p.name || '(no name)'),
              h('div', { class: 'small' }, [p.city, p.state && '(' + p.state + ')'].filter(Boolean).join(' '))),
            h('td', {}, p.domain || '—'),
            h('td', { class: 'mono' }, p.partita_iva || '—'),
            h('td', {}, p.classe_cliente ? h('span', { class: 'cls ' + p.classe_cliente }, p.classe_cliente) : h('span', { class: 'small' }, '—')),
            h('td', { class: 'num' }, money(p.fatturato_2025)));
        });
        body.replaceChildren(
          h('div', { class: 'tablewrap' }, h('table', {},
            h('thead', {}, h('tr', {}, h('th', {}, 'Company'), h('th', {}, 'Domain'), h('th', {}, 'P.IVA'), h('th', {}, 'Class'), h('th', { class: 'num' }, 'Revenue 2025'))),
            h('tbody', {}, rows.length ? rows : h('tr', {}, h('td', { colspan: 5 }, h('div', { class: 'empty' }, h('b', {}, 'No companies found'), 'Try another name, domain or partita IVA.')))))),
          h('div', { class: 'pager' }, h('span', {}, (r.total != null ? r.total.toLocaleString('en-US') : '') + ' companies'), h('span', { class: 'grow' }),
            h('button', { class: 'btn', type: 'button', disabled: !stack.length, onclick: function () { after = stack.pop(); load(); } }, 'Previous'),
            h('button', { class: 'btn', type: 'button', disabled: !(r.paging && r.paging.next), onclick: function () { stack.push(after); after = r.paging.next.after; load(); } }, 'Next')));
      }).catch(function (e) { fail(body, e); });
    }
    load();
  }

  /* ---------- contacts list ---------- */
  function contactsList() {
    var el = shell('/contacts'), body = h('div', { class: 'card' }), after, stack = [];
    el.append(h('h1', {}, 'Contacts'), body);
    function load() {
      loading(body);
      var req = { limit: 25, properties: ['firstname', 'lastname', 'email', 'phone', 'lifecyclestage'], sorts: [{ propertyName: 'lastname', direction: 'ASCENDING' }] };
      if (after) req.after = after;
      search('contacts', req).then(function (r) {
        var map = {};
        return assocMap('contacts', 'companies', (r.results || []).map(function (c) { return c.id; })).then(function (m) {
          map = m; return batchRead('companies', Object.keys(m).map(function (k) { return m[k]; }), ['name']);
        }).then(function (cos) {
          var names = {}; cos.forEach(function (c) { names[c.id] = c.properties.name; });
          body.replaceChildren(h('div', { class: 'tablewrap' }, h('table', {},
            h('thead', {}, h('tr', {}, h('th', {}, 'Name'), h('th', {}, 'Email'), h('th', {}, 'Phone'), h('th', {}, 'Company'), h('th', {}, 'Stage'))),
            h('tbody', {}, (r.results || []).map(function (c) {
              var p = c.properties, cid = map[c.id];
              return h('tr', {}, h('td', { style: 'font-weight:600' }, [p.firstname, p.lastname].filter(Boolean).join(' ') || '—'), h('td', {}, p.email || '—'), h('td', {}, p.phone || '—'),
                h('td', {}, cid ? h('a', { href: '/companies/' + cid, 'data-link': '' }, names[cid] || 'Company') : h('span', { class: 'small' }, 'No company')),
                h('td', {}, p.lifecyclestage ? h('span', { class: 'pill' }, p.lifecyclestage) : '—'));
            }))),
          ), h('div', { class: 'pager' }, h('span', { class: 'grow' }),
            h('button', { class: 'btn', type: 'button', disabled: !stack.length, onclick: function () { after = stack.pop(); load(); } }, 'Previous'),
            h('button', { class: 'btn', type: 'button', disabled: !(r.paging && r.paging.next), onclick: function () { stack.push(after); after = r.paging.next.after; load(); } }, 'Next')));
        });
      }).catch(function (e) { fail(body, e); });
    }
    load();
  }

  /* ---------- company page ---------- */
  var DEAL_PROPS = ['dealname', 'amount', 'deal_currency_code', 'pipeline', 'dealstage', 'closedate', 'commerciale', 'id_legacy'];
  var ACT = {
    notes: { label: 'Note', icon: 'note', body: 'hs_note_body' },
    calls: { label: 'Call', icon: 'call', body: 'hs_call_body' },
    emails: { label: 'Email', icon: 'email', body: 'hs_email_text' },
    meetings: { label: 'Meeting', icon: 'meeting', body: 'hs_meeting_body' }
  };
  function stageLabelMap(plist) {
    var m = {};
    plist.forEach(function (p) {
      p.stages.forEach(function (s) {
        var md = s.metadata || {}, closed = String(md.isClosed) === 'true' || String(md.ticketState) === 'CLOSED';
        m[s.id] = { label: s.label, closed: closed, won: closed && Number(md.probability) === 1, pipeline: p.label };
      });
    });
    return m;
  }
  function stagePill(st) {
    if (!st) return h('span', { class: 'pill' }, '—');
    return h('span', { class: 'pill' + (st.closed ? (st.won ? ' won' : ' lost') : '') }, st.label);
  }

  function companyPage(id) {
    var el = shell('/companies');
    loading(el);
    Promise.all([
      api('/crm/v3/objects/companies/' + id + '?properties=' + CO_PROPS.concat(['hs_additional_domains']).join(',')),
      assoc('companies', id, 'contacts'), assoc('companies', id, 'deals'), assoc('companies', id, 'tickets'),
      pipelines('deals'), pipelines('tickets')
    ]).then(function (a) {
      var co = a[0], contactIds = a[1], dealIds = a[2], ticketIds = a[3], dpl = a[4], tpl = a[5];
      return Promise.all([
        batchRead('contacts', contactIds, ['firstname', 'lastname', 'email', 'phone', 'lifecyclestage']),
        batchRead('deals', dealIds, DEAL_PROPS),
        batchRead('tickets', ticketIds, ['subject', 'hs_pipeline_stage', 'hs_ticket_priority', 'createdate', 'assegnatario']),
        loadActivities(contactIds.slice(0, 25), dealIds.slice(0, 25))
      ]).then(function (b) { renderCompany(el, co, b[0], b[1], b[2], b[3], stageLabelMap(dpl), stageLabelMap(tpl)); });
    }).catch(function (e) { fail(el, e); });
  }

  function loadActivities(contactIds, dealIds) {
    var types = Object.keys(ACT), jobs = [];
    var sources = contactIds.map(function (id) { return ['contacts', id]; }).concat(dealIds.map(function (id) { return ['deals', id]; }));
    sources.forEach(function (s) { types.forEach(function (t) { jobs.push(assoc(s[0], s[1], t).then(function (ids) { return ids.map(function (i) { return { t: t, id: i }; }); })); }); });
    return Promise.all(jobs).then(function (r) {
      var seen = {}, byType = {};
      [].concat.apply([], r).forEach(function (x) { if (!seen[x.t + x.id]) { seen[x.t + x.id] = 1; (byType[x.t] = byType[x.t] || []).push(x.id); } });
      return Promise.all(types.map(function (t) {
        return batchRead(t, (byType[t] || []).slice(0, 200), ['hs_timestamp', ACT[t].body, 'autore']).then(function (rs) { return rs.map(function (x) { return { type: t, p: x.properties }; }); });
      }));
    }).then(function (r) { return [].concat.apply([], r).sort(function (a, b) { return new Date(b.p.hs_timestamp) - new Date(a.p.hs_timestamp); }); });
  }

  function renderCompany(el, co, contacts, deals, tickets, acts, dst, tst) {
    var p = co.properties;
    var won = 0, openSum = 0, openN = 0;
    deals.forEach(function (d) {
      var s = dst[d.properties.dealstage] || {};
      if (!s.closed) { openSum += toEur(d.properties.amount, d.properties.deal_currency_code); openN++; }
    });
    var rev = Number(p.fatturato_2025 || 0), cls = p.classe_cliente || '';
    var lastAct = acts[0];
    var has2025 = acts.some(function (a) { return new Date(a.p.hs_timestamp).getFullYear() === 2025; });
    var wonAny = deals.some(function (d) { var s = dst[d.properties.dealstage]; return s && s.closed && s.won; });
    var dormant = wonAny && !has2025;

    var years = {};
    acts.forEach(function (a) { var y = new Date(a.p.hs_timestamp).getFullYear() || 'Undated'; (years[y] = years[y] || []).push(a); });
    if (!years[2025] && acts.length) years[2025] = [];
    var yearKeys = Object.keys(years).sort(function (a, b) { return b - a; });

    var domains = [p.domain].concat((p.hs_additional_domains || '').split(/[;,\s]+/)).filter(Boolean);
    el.replaceChildren(
      h('div', { class: 'row', style: 'align-items:flex-start;justify-content:space-between' },
        h('div', { style: 'display:flex;flex-direction:column;gap:8px;min-width:0' },
          h('nav', { class: 'small', 'aria-label': 'Breadcrumb' }, h('a', { href: '/companies', 'data-link': '' }, 'Companies'), ' / ' + (p.name || '')),
          h('h1', {}, p.name || '(no name)'),
          h('div', { class: 'row small', style: 'gap:6px 18px' },
            domains.length ? h('span', {}, domains.join(' · ')) : null,
            (p.city || p.state) ? h('span', {}, [p.city, p.state && '(' + p.state + ')'].filter(Boolean).join(' ')) : null),
          h('div', { class: 'row', style: 'gap:8px' },
            p.partita_iva ? h('span', { class: 'pill' }, 'P.IVA ', h('span', { class: 'mono' }, p.partita_iva)) : null,
            p.id_legacy ? h('span', { class: 'pill' }, 'Sinergia ', h('span', { class: 'mono' }, p.id_legacy)) : null,
            dormant ? h('a', { href: '/dormant', 'data-link': '', class: 'pill', style: 'background:#FBF0D6;color:#7A5410' }, 'In Clienti dormienti') : null))),
      h('section', { class: 'stats', 'aria-label': 'Key figures' },
        h('div', {}, h('span', { class: 'label' }, 'Revenue won · 2025'), h('span', { class: 'big' }, money(rev)), h('span', { class: 'small' }, 'Net of credit notes')),
        h('div', {}, h('span', { class: 'label' }, 'Customer class'), cls ? h('span', { class: 'cls ' + cls, style: 'width:40px;height:40px;font-size:28px' }, cls) : h('span', { class: 'big', style: 'color:#6B7280' }, '—'),
          h('span', { class: 'small' }, cls ? 'A ≥ €100k · B ≥ €20k · C above 0' : 'No revenue won in 2025')),
        h('div', {}, h('span', { class: 'label' }, 'Open pipeline'), h('span', { class: 'big' }, money(openSum)), h('span', { class: 'small' }, openN + ' open deal' + (openN === 1 ? '' : 's') + ' (non-euro converted)')),
        h('div', {}, h('span', { class: 'label' }, 'Last activity'), h('span', { class: 'big' }, lastAct ? date(lastAct.p.hs_timestamp) : '—'), h('span', { class: 'small' }, lastAct ? ACT[lastAct.type].label + (lastAct.p.autore ? ' by ' + nameFromEmail(lastAct.p.autore) : '') : 'None logged'))),
      h('div', { class: 'cols' },
        h('div', { class: 'l' },
          h('section', { class: 'card', 'aria-labelledby': 'dh' },
            h('header', {}, h('h2', { id: 'dh' }, 'Deals ', h('span', { class: 'small' }, deals.length)), h('span', { class: 'grow' }), h('a', { href: '/deals', 'data-link': '' }, 'Open board')),
            deals.length ? h('div', { class: 'tablewrap' }, h('table', {},
              h('thead', {}, h('tr', {}, h('th', {}, 'Deal'), h('th', {}, 'Stage'), h('th', { class: 'num' }, 'Amount'), h('th', {}, 'Close date'), h('th', {}, 'Sales rep'))),
              h('tbody', {}, deals.sort(function (a, b) { return new Date(b.properties.closedate || 0) - new Date(a.properties.closedate || 0); }).map(function (d) {
                var q = d.properties, s = dst[q.dealstage];
                return h('tr', {}, h('td', {}, h('b', {}, q.dealname || '—'), h('div', { class: 'small mono' }, (s && s.pipeline ? s.pipeline + ' · ' : '') + (q.id_legacy ? 'Sinergia ' + q.id_legacy : ''))),
                  h('td', {}, stagePill(s)), h('td', { class: 'num', style: 'font-weight:500' }, money(q.amount, q.deal_currency_code)),
                  h('td', {}, date(q.closedate)), h('td', {}, repCell(q.commerciale)));
              })))) : h('div', { class: 'empty' }, h('b', {}, 'No deals'), 'Deals associated with this company appear here.')),
          h('section', { class: 'card', 'aria-labelledby': 'ah' },
            h('header', {}, h('h2', { id: 'ah' }, 'Activity ', h('span', { class: 'small' }, acts.length))),
            acts.length ? h('div', { class: 'tl' }, yearKeys.map(function (y) {
              return h('div', {}, h('h3', {}, y),
                years[y].length ? years[y].slice(0, 40).map(function (a) {
                  return h('div', { class: 'ev' }, h('span', { class: 'mono small', style: 'padding-top:5px' }, date(a.p.hs_timestamp, false)),
                    h('span', { class: 'ic' }, (function () { var s = svg(ICON[ACT[a.type].icon]); s.style.cssText = 'width:15px;height:15px;fill:none;stroke:currentColor;stroke-width:1.8'; return s; })()),
                    h('div', {}, h('div', { class: 'small' }, h('b', { style: 'color:#16191D' }, ACT[a.type].label), a.p.autore ? ' by ' + nameFromEmail(a.p.autore) : ''), h('p', {}, a.p[ACT[a.type].body] || '')));
                }) : h('div', { class: 'silent' }, 'No activity logged in ' + y + '.' + (wonAny ? ' With won deals, a silent 2025 puts this company on Clienti dormienti.' : '')));
            })) : h('div', { class: 'empty' }, h('b', {}, 'No activity yet'), 'Notes, calls, emails and meetings on this company’s contacts and deals show up here.'))),
        h('aside', { class: 'r' },
          h('section', { class: 'card' }, h('header', {}, h('h2', {}, 'About')),
            h('dl', {}, [['Company name', p.name], ['Domain', p.domain], ['Additional domains', (p.hs_additional_domains || '').replace(/;/g, ', ')], ['City', p.city], ['Province', p.state], ['Partita IVA', p.partita_iva, 1], ['Customer class', p.classe_cliente], ['Revenue won 2025', money(rev)], ['Sinergia code', p.id_legacy, 1]].map(function (r) {
              return h('div', {}, h('dt', {}, r[0]), h('dd', { class: r[2] ? 'mono' : '' }, r[1] || '—'));
            }))),
          h('section', { class: 'card' }, h('header', {}, h('h2', {}, 'Contacts ', h('span', { class: 'small' }, contacts.length))),
            contacts.length ? contacts.map(function (c) {
              var q = c.properties;
              return h('div', { class: 'pad', style: 'display:flex;gap:12px;border-bottom:1px solid #F0F1F0' }, h('span', { class: 'avatar', style: 'width:36px;height:36px;font-size:12px;background:#EEF1F4;color:#333A42' }, initials([q.firstname, q.lastname].join(' '))),
                h('div', { style: 'min-width:0' }, h('b', {}, [q.firstname, q.lastname].filter(Boolean).join(' ') || '—'), ' ', q.lifecyclestage ? h('span', { class: 'pill' }, q.lifecyclestage) : null,
                  h('div', { class: 'small', style: 'overflow-wrap:anywhere' }, q.email || 'No email'), h('div', { class: 'small' }, q.phone || '')));
            }) : h('div', { class: 'empty' }, 'No contacts. A contact whose email domain matches this company’s website is linked automatically.')),
          h('section', { class: 'card' }, h('header', {}, h('h2', {}, 'Tickets ', h('span', { class: 'small' }, tickets.length)), h('span', { class: 'grow' }), h('a', { href: '/tickets', 'data-link': '' }, 'All tickets')),
            tickets.length ? tickets.slice(0, 8).map(function (t) {
              var q = t.properties, s = tst[q.hs_pipeline_stage];
              return h('div', { class: 'pad', style: 'border-bottom:1px solid #F0F1F0' }, h('b', {}, q.subject || '—'), h('div', { class: 'row small', style: 'gap:8px' }, stagePill(s), date(q.createdate), repCell(q.assegnatario)));
            }) : h('div', { class: 'empty' }, h('b', {}, 'No support tickets'), 'Tickets in the Assistenza pipeline show up here.')))));
  }

  /* ---------- deals board ---------- */
  var boardPipe = 'default';
  function dealsBoard() {
    var el = shell('/deals'); loading(el);
    pipelines('deals').then(function (pl) {
      if (!pl.some(function (p) { return p.id === boardPipe; })) boardPipe = (pl[0] || {}).id;
      var pipe = pl.filter(function (p) { return p.id === boardPipe; })[0];
      var seg = h('div', { class: 'seg', role: 'group', 'aria-label': 'Pipeline' }, pl.map(function (p) {
        return h('button', { type: 'button', 'aria-pressed': String(p.id === boardPipe), onclick: function () { boardPipe = p.id; dealsBoard(); } }, p.label);
      }));
      var board = h('div', { class: 'board' });
      el.replaceChildren(h('div', { class: 'row' }, h('h1', {}, 'Deals'), seg, h('span', { class: 'small' }, 'Drag a card to change its stage')), board);
      pipe.stages.forEach(function (s) { board.appendChild(boardColumn(pipe, s)); });
    }).catch(function (e) { fail(el, e); });
  }
  function boardColumn(pipe, stage) {
    var closed = String(stage.metadata && stage.metadata.isClosed) === 'true', won = closed && Number(stage.metadata.probability) === 1;
    var count = h('span', { class: 'small mono grow', style: 'text-align:right' }, '…'), sum = h('div', { class: 'small' }, ' ');
    var list = h('div', { style: 'display:flex;flex-direction:column;gap:8px' });
    var col = h('section', { class: 'col' + (closed ? (won ? ' won' : ' lost') : ''), 'data-stage': stage.id },
      h('header', {}, h('h3', {}, stage.label, count), sum), list);
    col.addEventListener('dragover', function (e) { e.preventDefault(); col.classList.add('over'); });
    col.addEventListener('dragleave', function () { col.classList.remove('over'); });
    col.addEventListener('drop', function (e) {
      e.preventDefault(); col.classList.remove('over');
      var id = e.dataTransfer.getData('text/plain'); if (!id) return;
      askToken(function () { api('/crm/v3/objects/deals/' + id, { method: 'PATCH', body: { properties: { dealstage: stage.id } } }).then(function () {
        toast('Moved to ' + stage.label + (won && pipe.id === 'default' ? '. Supply kickoff ticket is being opened.' : (closed && !won ? '. Call-back task is being created.' : '')));
        dealsBoard();
      }).catch(function (err) { toast('Could not move the deal. ' + err.message, true); }); });
    });
    search('deals', { limit: 20, properties: DEAL_PROPS, sorts: [{ propertyName: 'amount', direction: 'DESCENDING' }],
      filterGroups: [{ filters: [{ propertyName: 'pipeline', operator: 'EQ', value: pipe.id }, { propertyName: 'dealstage', operator: 'EQ', value: stage.id }] }] })
      .then(function (r) {
        var deals = r.results || [];
        count.textContent = (r.total || 0).toLocaleString('en-US');
        sum.textContent = deals.length ? 'Top ' + deals.length + ': ' + money(deals.reduce(function (t, d) { return t + toEur(d.properties.amount, d.properties.deal_currency_code); }, 0)) : 'No deals';
        return assocMap('deals', 'companies', deals.map(function (d) { return d.id; })).then(function (m) {
          return batchRead('companies', Object.keys(m).map(function (k) { return m[k]; }), ['name']).then(function (cos) {
            var names = {}; cos.forEach(function (c) { names[c.id] = c.properties.name; });
            deals.forEach(function (d) { list.appendChild(dealCard(d, m[d.id], names[m[d.id]])); });
          });
        });
      }).catch(function (e) { count.textContent = '!'; list.appendChild(h('div', { class: 'err' }, e.message)); });
    return col;
  }
  function dealCard(d, cid, cname) {
    var p = d.properties, cur = p.deal_currency_code || 'EUR';
    var c = h('article', { class: 'deal', draggable: 'true' },
      h('b', {}, p.dealname || '—'),
      cname ? h('a', { class: 'small', href: '/companies/' + cid, 'data-link': '' }, cname) : null,
      h('div', { style: 'display:flex;justify-content:space-between;align-items:baseline' }, h('span', { class: 'amt' }, money(p.amount, cur)), h('span', { class: 'small mono' }, p.amount ? cur : '')),
      cur !== 'EUR' && p.amount ? h('span', { class: 'small' }, '≈ ' + money(toEur(p.amount, cur)) + ' at ' + (cur === 'USD' ? '0.92' : '1.17')) : null,
      h('div', { style: 'display:flex;justify-content:space-between;gap:8px;padding-top:6px;border-top:1px solid #F0F1F0' }, h('span', { class: 'small' }, p.closedate ? date(p.closedate) : 'No close date'), repCell(p.commerciale)));
    c.addEventListener('dragstart', function (e) { e.dataTransfer.setData('text/plain', d.id); e.dataTransfer.effectAllowed = 'move'; });
    return c;
  }

  /* ---------- tickets ---------- */
  var ticketTab = 'all';
  function ticketsView() {
    var el = shell('/tickets'); loading(el);
    pipelines('tickets').then(function (pl) {
      var pipe = pl.filter(function (p) { return p.label === 'Assistenza'; })[0] || pl[0];
      if (!pipe) throw new Error('No ticket pipeline yet.');
      var openIds = pipe.stages.filter(function (s) { return String(s.metadata && s.metadata.ticketState) !== 'CLOSED'; }).map(function (s) { return s.id; });
      var tabs = [{ id: 'all', label: 'All open', ids: openIds }].concat(pipe.stages.map(function (s) { return { id: s.id, label: s.label, ids: [s.id] }; }));
      var tbody = h('tbody', {}), tabsEl = h('div', { class: 'tabs', role: 'tablist', 'aria-label': 'Status' }), pager = h('div', { class: 'pager' });
      var after, stack = [], smap = {};
      pipe.stages.forEach(function (s) { smap[s.id] = s; });
      el.replaceChildren(h('div', { class: 'row' }, h('h1', {}, 'Tickets'), h('span', { class: 'pill' }, 'Pipeline ', h('b', {}, pipe.label))), tabsEl,
        h('section', { class: 'card' }, h('div', { class: 'tablewrap' }, h('table', {}, h('thead', {}, h('tr', {}, h('th', {}, 'Subject'), h('th', {}, 'Company'), h('th', {}, 'Status'), h('th', {}, 'Priority'), h('th', {}, 'Assignee'), h('th', {}, 'Opened'))), tbody)), pager));
      function drawTabs() {
        tabsEl.replaceChildren.apply(tabsEl, tabs.map(function (t) {
          return h('button', { type: 'button', role: 'tab', 'aria-selected': String(t.id === ticketTab), onclick: function () { ticketTab = t.id; after = undefined; stack = []; drawTabs(); load(); } }, t.label);
        }));
      }
      function load() {
        var tab = tabs.filter(function (t) { return t.id === ticketTab; })[0] || tabs[0];
        tbody.replaceChildren(h('tr', {}, h('td', { colspan: 6 }, h('div', { class: 'empty' }, 'Loading…'))));
        var req = { limit: 25, properties: ['subject', 'content', 'hs_pipeline_stage', 'hs_ticket_priority', 'createdate', 'assegnatario', 'id_legacy'], sorts: [{ propertyName: 'createdate', direction: 'DESCENDING' }],
          filterGroups: [{ filters: [{ propertyName: 'hs_pipeline', operator: 'EQ', value: pipe.id }, { propertyName: 'hs_pipeline_stage', operator: 'IN', values: tab.ids }] }] };
        if (after) req.after = after;
        search('tickets', req).then(function (r) {
          var ts = r.results || [];
          return assocMap('tickets', 'companies', ts.map(function (t) { return t.id; })).then(function (m) {
            return batchRead('companies', Object.keys(m).map(function (k) { return m[k]; }), ['name']).then(function (cos) {
              var names = {}; cos.forEach(function (c) { names[c.id] = c.properties.name; });
              tbody.replaceChildren.apply(tbody, ts.length ? ts.map(function (t) {
                var p = t.properties, s = smap[p.hs_pipeline_stage], cid = m[t.id];
                return h('tr', { class: 'click', onclick: function () { openTicket(t, s, cid, names[cid]); } },
                  h('td', { style: 'max-width:340px' }, h('b', {}, p.subject || '—'), p.id_legacy ? h('div', { class: 'small mono' }, 'Sinergia ' + p.id_legacy) : null),
                  h('td', {}, cid ? h('a', { href: '/companies/' + cid, 'data-link': '' }, names[cid] || 'Company') : '—'),
                  h('td', {}, s ? h('span', { class: 'pill' }, s.label) : '—'),
                  h('td', {}, p.hs_ticket_priority ? h('span', { class: 'pri ' + p.hs_ticket_priority }, p.hs_ticket_priority) : h('span', { class: 'small' }, '—')),
                  h('td', {}, repCell(p.assegnatario)), h('td', { style: 'white-space:nowrap' }, date(p.createdate)));
              }) : [h('tr', {}, h('td', { colspan: 6 }, h('div', { class: 'empty' }, h('b', {}, 'No tickets here'), 'Nothing is in this status right now.')))]);
              pager.replaceChildren(h('span', {}, (r.total || 0).toLocaleString('en-US') + ' tickets'), h('span', { class: 'grow' }),
                h('button', { class: 'btn', type: 'button', disabled: !stack.length, onclick: function () { after = stack.pop(); load(); } }, 'Previous'),
                h('button', { class: 'btn', type: 'button', disabled: !(r.paging && r.paging.next), onclick: function () { stack.push(after); after = r.paging.next.after; load(); } }, 'Next'));
            });
          });
        }).catch(function (e) { tbody.replaceChildren(h('tr', {}, h('td', { colspan: 6 }, h('div', { class: 'err' }, e.message)))); });
      }
      drawTabs(); load();
    }).catch(function (e) { fail(el, e); });
  }
  function closeDetail() { var d = document.getElementById('tdetail'); if (d) d.remove(); }
  function openTicket(t, s, cid, cname) {
    closeDetail();
    var p = t.properties;
    document.body.appendChild(h('aside', { class: 'tdetail', id: 'tdetail', 'aria-label': 'Ticket detail' },
      h('div', { class: 'pad', style: 'border-bottom:1px solid #E6E8E6;display:flex;flex-direction:column;gap:6px' },
        h('div', { class: 'row' }, h('span', { class: 'small mono grow' }, (p.id_legacy ? 'Sinergia ' + p.id_legacy + ' · ' : '') + 'opened ' + date(p.createdate)), h('button', { class: 'btn', type: 'button', 'aria-label': 'Close', onclick: closeDetail }, 'Close')),
        h('h2', { style: 'font-size:26px' }, p.subject || '—')),
      h('dl', {}, [['Status', s ? s.label : '—'], ['Priority', p.hs_ticket_priority || 'None'], ['Assignee', nameFromEmail(p.assegnatario) || 'Unassigned']].map(function (r) { return h('div', {}, h('dt', {}, r[0]), h('dd', {}, r[1])); })),
      h('div', { class: 'pad' }, h('div', { class: 'label' }, 'Description'), h('p', { style: 'white-space:pre-line;margin:8px 0 0' }, p.content || '—')),
      h('div', { class: 'pad' }, h('div', { class: 'label' }, 'Associated with'), cid ? h('p', {}, h('a', { href: '/companies/' + cid, 'data-link': '' }, cname || 'Company')) : h('p', { class: 'small' }, 'No company'))));
  }

  /* ---------- clienti dormienti ---------- */
  function dormantList() {
    var el = shell('/dormant'), body = h('div', { class: 'card' }), after, stack = [];
    el.replaceChildren(h('div', { class: 'row' }, h('h1', {}, 'Clienti dormienti'), h('span', { class: 'small', id: 'dcount' })),
      h('div', { class: 'row small' }, h('span', { class: 'pill won' }, 'Won at least one deal'), 'and', h('span', { class: 'pill', style: 'background:#FBF0D6;color:#7A5410' }, 'No activity in 2025'), 'on the company’s contacts or deals'), body);
    loading(body);
    api('/crm/v3/lists/search', { method: 'POST', body: { query: 'Clienti dormienti', objectTypeId: '0-2' } }).then(function (r) {
      var l = (r.lists || []).filter(function (x) { return x.name === 'Clienti dormienti'; })[0];
      if (!l) { body.replaceChildren(h('div', { class: 'empty' }, h('b', {}, 'The list does not exist yet'), 'It is created by the Sinergia migration.')); return; }
      function page() {
        loading(body);
        api('/crm/v3/lists/' + l.listId + '/memberships?limit=25' + (after ? '&after=' + encodeURIComponent(after) : '')).then(function (m) {
          var ids = (m.results || []).map(function (x) { return String(x.recordId); });
          return Promise.all([batchRead('companies', ids, CO_PROPS), assocMap('companies', 'deals', ids)]).then(function (z) {
            var order = {}; ids.forEach(function (id, i) { order[id] = i; });
            var cos = z[0].sort(function (a, b) { return order[a.id] - order[b.id]; });
            var cnt = document.getElementById('dcount'); if (cnt && l.size != null) cnt.textContent = Number(l.size).toLocaleString('en-US') + ' companies';
            body.replaceChildren(h('div', { class: 'tablewrap' }, h('table', {},
              h('thead', {}, h('tr', {}, h('th', {}, 'Company'), h('th', {}, 'Class'), h('th', {}, 'City'), h('th', {}, 'P.IVA'), h('th', { class: 'num' }, 'Revenue 2025'), h('th', {}, ''))),
              h('tbody', {}, cos.length ? cos.map(function (c) {
                var p = c.properties;
                return h('tr', {}, h('td', {}, h('a', { href: '/companies/' + c.id, 'data-link': '', style: 'font-weight:600' }, p.name || '—'), h('div', { class: 'small' }, p.domain || '')),
                  h('td', {}, p.classe_cliente ? h('span', { class: 'cls ' + p.classe_cliente }, p.classe_cliente) : h('span', { class: 'small' }, '—')),
                  h('td', {}, [p.city, p.state && '(' + p.state + ')'].filter(Boolean).join(' ') || '—'), h('td', { class: 'mono' }, p.partita_iva || '—'), h('td', { class: 'num' }, money(p.fatturato_2025)),
                  h('td', { class: 'num' }, h('a', { class: 'btn', href: '/companies/' + c.id, 'data-link': '' }, 'Open')));
              }) : h('tr', {}, h('td', { colspan: 6 }, h('div', { class: 'empty' }, h('b', {}, 'No dormant customers'), 'Every customer with won deals had activity in 2025.')))))),
              h('div', { class: 'pager' }, h('span', { class: 'grow' }),
                h('button', { class: 'btn', type: 'button', disabled: !stack.length, onclick: function () { after = stack.pop(); page(); } }, 'Previous'),
                h('button', { class: 'btn', type: 'button', disabled: !(m.paging && m.paging.next), onclick: function () { stack.push(after); after = m.paging.next.after; page(); } }, 'Next')));
          });
        }).catch(function (e) { fail(body, e); });
      }
      page();
    }).catch(function (e) { fail(body, e); });
  }

  /* ---------- assistant ---------- */
  var chat = [];
  function openAssistant() {
    if (document.getElementById('assistant')) return;
    if (!store.get('crm_token')) return askToken(openAssistant);
    var log = h('div', { class: 'body', 'aria-live': 'polite' });
    var input = h('textarea', { id: 'ask', rows: 2, placeholder: 'Write it the way you would to a colleague…' });
    var send = h('button', { class: 'btn primary', type: 'submit' }, 'Send');
    function draw() {
      log.replaceChildren(chat.length ? chat.map(function (m) { return h('div', { class: 'msg ' + (m.role === 'user' ? 'user' : 'bot') }, m.content); })
        : h('div', { class: 'small' }, 'Ask for a number, or ask it to update the CRM. Examples: “Segna come vinta la trattativa di …”, “Quanto abbiamo fatturato con … nel 2025?”'));
      log.scrollTop = log.scrollHeight;
    }
    function submit(e) {
      e.preventDefault();
      var text = input.value.trim(); if (!text) return;
      chat.push({ role: 'user', content: text }); input.value = ''; send.disabled = true; draw();
      var pending = h('div', { class: 'msg bot small' }, 'Working…'); log.appendChild(pending);
      api('/__agente', { method: 'POST', body: { context: { now: new Date().toISOString(), user: store.get('crm_user') }, messages: chat } })
        .then(function (r) { chat.push({ role: 'assistant', content: r.reply || '(no reply)' }); })
        .catch(function (err) { chat.push({ role: 'assistant', content: 'The assistant could not answer. ' + err.message }); })
        .then(function () { send.disabled = false; draw(); input.focus(); });
    }
    input.addEventListener('keydown', function (e) { if (e.key === 'Enter' && !e.shiftKey) submit(e); });
    document.body.appendChild(h('aside', { class: 'drawer', id: 'assistant', 'aria-label': 'Assistant' },
      h('header', {}, h('h2', { class: 'grow' }, 'Assistant'),
        h('button', { class: 'btn', type: 'button', onclick: function () { chat = []; draw(); } }, 'New'),
        h('button', { class: 'btn', type: 'button', 'aria-label': 'Close assistant', onclick: function () { document.getElementById('assistant').remove(); } }, 'Close')),
      log,
      h('form', { onsubmit: submit }, h('label', { class: 'label', for: 'ask' }, 'Ask the CRM'), input, h('div', { class: 'row' }, h('span', { class: 'small grow' }, 'Follows the CRM rules'), send))));
    draw(); input.focus();
  }

  route();
})();
