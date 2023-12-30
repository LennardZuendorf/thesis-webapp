const {
  SvelteComponent: lt,
  attr: he,
  detach: nt,
  element: it,
  init: st,
  insert: ft,
  noop: we,
  safe_not_equal: ot,
  toggle_class: W
} = window.__gradio__svelte__internal, { createEventDispatcher: at } = window.__gradio__svelte__internal;
function rt(n) {
  let t, e;
  return {
    c() {
      t = it("div"), he(t, "class", e = "prose " + /*elem_classes*/
      n[0].join(" ") + " svelte-2qygph"), W(
        t,
        "min",
        /*min_height*/
        n[3]
      ), W(t, "hide", !/*visible*/
      n[2]);
    },
    m(l, i) {
      ft(l, t, i), t.innerHTML = /*value*/
      n[1];
    },
    p(l, [i]) {
      i & /*value*/
      2 && (t.innerHTML = /*value*/
      l[1]), i & /*elem_classes*/
      1 && e !== (e = "prose " + /*elem_classes*/
      l[0].join(" ") + " svelte-2qygph") && he(t, "class", e), i & /*elem_classes, min_height*/
      9 && W(
        t,
        "min",
        /*min_height*/
        l[3]
      ), i & /*elem_classes, visible*/
      5 && W(t, "hide", !/*visible*/
      l[2]);
    },
    i: we,
    o: we,
    d(l) {
      l && nt(t);
    }
  };
}
function _t(n, t, e) {
  let { elem_classes: l = [] } = t, { value: i } = t, { visible: f = !0 } = t, { min_height: o = !1 } = t;
  const a = at();
  return n.$$set = (r) => {
    "elem_classes" in r && e(0, l = r.elem_classes), "value" in r && e(1, i = r.value), "visible" in r && e(2, f = r.visible), "min_height" in r && e(3, o = r.min_height);
  }, n.$$.update = () => {
    n.$$.dirty & /*value*/
    2 && a("change");
  }, [l, i, f, o];
}
class ut extends lt {
  constructor(t) {
    super(), st(this, t, _t, rt, ot, {
      elem_classes: 0,
      value: 1,
      visible: 2,
      min_height: 3
    });
  }
}
function X(n) {
  let t = ["", "k", "M", "G", "T", "P", "E", "Z"], e = 0;
  for (; n > 1e3 && e < t.length - 1; )
    n /= 1e3, e++;
  let l = t[e];
  return (Number.isInteger(n) ? n : n.toFixed(1)) + l;
}
function ee() {
}
function ct(n, t) {
  return n != n ? t == t : n !== t || n && typeof n == "object" || typeof n == "function";
}
const Oe = typeof window < "u";
let ve = Oe ? () => window.performance.now() : () => Date.now(), Re = Oe ? (n) => requestAnimationFrame(n) : ee;
const Y = /* @__PURE__ */ new Set();
function Ue(n) {
  Y.forEach((t) => {
    t.c(n) || (Y.delete(t), t.f());
  }), Y.size !== 0 && Re(Ue);
}
function dt(n) {
  let t;
  return Y.size === 0 && Re(Ue), {
    promise: new Promise((e) => {
      Y.add(t = { c: n, f: e });
    }),
    abort() {
      Y.delete(t);
    }
  };
}
const H = [];
function mt(n, t = ee) {
  let e;
  const l = /* @__PURE__ */ new Set();
  function i(a) {
    if (ct(n, a) && (n = a, e)) {
      const r = !H.length;
      for (const s of l)
        s[1](), H.push(s, n);
      if (r) {
        for (let s = 0; s < H.length; s += 2)
          H[s][0](H[s + 1]);
        H.length = 0;
      }
    }
  }
  function f(a) {
    i(a(n));
  }
  function o(a, r = ee) {
    const s = [a, r];
    return l.add(s), l.size === 1 && (e = t(i, f) || ee), a(n), () => {
      l.delete(s), l.size === 0 && e && (e(), e = null);
    };
  }
  return { set: i, update: f, subscribe: o };
}
function ye(n) {
  return Object.prototype.toString.call(n) === "[object Date]";
}
function se(n, t, e, l) {
  if (typeof e == "number" || ye(e)) {
    const i = l - e, f = (e - t) / (n.dt || 1 / 60), o = n.opts.stiffness * i, a = n.opts.damping * f, r = (o - a) * n.inv_mass, s = (f + r) * n.dt;
    return Math.abs(s) < n.opts.precision && Math.abs(i) < n.opts.precision ? l : (n.settled = !1, ye(e) ? new Date(e.getTime() + s) : e + s);
  } else {
    if (Array.isArray(e))
      return e.map(
        (i, f) => se(n, t[f], e[f], l[f])
      );
    if (typeof e == "object") {
      const i = {};
      for (const f in e)
        i[f] = se(n, t[f], e[f], l[f]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof e} values`);
  }
}
function ke(n, t = {}) {
  const e = mt(n), { stiffness: l = 0.15, damping: i = 0.8, precision: f = 0.01 } = t;
  let o, a, r, s = n, _ = n, c = 1, w = 0, h = !1;
  function y(p, L = {}) {
    _ = p;
    const F = r = {};
    return n == null || L.hard || C.stiffness >= 1 && C.damping >= 1 ? (h = !0, o = ve(), s = p, e.set(n = _), Promise.resolve()) : (L.soft && (w = 1 / ((L.soft === !0 ? 0.5 : +L.soft) * 60), c = 0), a || (o = ve(), h = !1, a = dt((u) => {
      if (h)
        return h = !1, a = null, !1;
      c = Math.min(c + w, 1);
      const k = {
        inv_mass: c,
        opts: C,
        settled: !0,
        dt: (u - o) * 60 / 1e3
      }, m = se(k, s, n, _);
      return o = u, s = n, e.set(n = m), k.settled && (a = null), !k.settled;
    })), new Promise((u) => {
      a.promise.then(() => {
        F === r && u();
      });
    }));
  }
  const C = {
    set: y,
    update: (p, L) => y(p(_, n), L),
    subscribe: e.subscribe,
    stiffness: l,
    damping: i,
    precision: f
  };
  return C;
}
const {
  SvelteComponent: bt,
  append: N,
  attr: v,
  component_subscribe: pe,
  detach: gt,
  element: ht,
  init: wt,
  insert: vt,
  noop: qe,
  safe_not_equal: yt,
  set_style: x,
  svg_element: T,
  toggle_class: Fe
} = window.__gradio__svelte__internal, { onMount: kt } = window.__gradio__svelte__internal;
function pt(n) {
  let t, e, l, i, f, o, a, r, s, _, c, w;
  return {
    c() {
      t = ht("div"), e = T("svg"), l = T("g"), i = T("path"), f = T("path"), o = T("path"), a = T("path"), r = T("g"), s = T("path"), _ = T("path"), c = T("path"), w = T("path"), v(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), v(i, "fill", "#FF7C00"), v(i, "fill-opacity", "0.4"), v(i, "class", "svelte-43sxxs"), v(f, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), v(f, "fill", "#FF7C00"), v(f, "class", "svelte-43sxxs"), v(o, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), v(o, "fill", "#FF7C00"), v(o, "fill-opacity", "0.4"), v(o, "class", "svelte-43sxxs"), v(a, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), v(a, "fill", "#FF7C00"), v(a, "class", "svelte-43sxxs"), x(l, "transform", "translate(" + /*$top*/
      n[1][0] + "px, " + /*$top*/
      n[1][1] + "px)"), v(s, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), v(s, "fill", "#FF7C00"), v(s, "fill-opacity", "0.4"), v(s, "class", "svelte-43sxxs"), v(_, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), v(_, "fill", "#FF7C00"), v(_, "class", "svelte-43sxxs"), v(c, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), v(c, "fill", "#FF7C00"), v(c, "fill-opacity", "0.4"), v(c, "class", "svelte-43sxxs"), v(w, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), v(w, "fill", "#FF7C00"), v(w, "class", "svelte-43sxxs"), x(r, "transform", "translate(" + /*$bottom*/
      n[2][0] + "px, " + /*$bottom*/
      n[2][1] + "px)"), v(e, "viewBox", "-1200 -1200 3000 3000"), v(e, "fill", "none"), v(e, "xmlns", "http://www.w3.org/2000/svg"), v(e, "class", "svelte-43sxxs"), v(t, "class", "svelte-43sxxs"), Fe(
        t,
        "margin",
        /*margin*/
        n[0]
      );
    },
    m(h, y) {
      vt(h, t, y), N(t, e), N(e, l), N(l, i), N(l, f), N(l, o), N(l, a), N(e, r), N(r, s), N(r, _), N(r, c), N(r, w);
    },
    p(h, [y]) {
      y & /*$top*/
      2 && x(l, "transform", "translate(" + /*$top*/
      h[1][0] + "px, " + /*$top*/
      h[1][1] + "px)"), y & /*$bottom*/
      4 && x(r, "transform", "translate(" + /*$bottom*/
      h[2][0] + "px, " + /*$bottom*/
      h[2][1] + "px)"), y & /*margin*/
      1 && Fe(
        t,
        "margin",
        /*margin*/
        h[0]
      );
    },
    i: qe,
    o: qe,
    d(h) {
      h && gt(t);
    }
  };
}
function qt(n, t, e) {
  let l, i, { margin: f = !0 } = t;
  const o = ke([0, 0]);
  pe(n, o, (w) => e(1, l = w));
  const a = ke([0, 0]);
  pe(n, a, (w) => e(2, i = w));
  let r;
  async function s() {
    await Promise.all([o.set([125, 140]), a.set([-125, -140])]), await Promise.all([o.set([-125, 140]), a.set([125, -140])]), await Promise.all([o.set([-125, 0]), a.set([125, -0])]), await Promise.all([o.set([125, 0]), a.set([-125, 0])]);
  }
  async function _() {
    await s(), r || _();
  }
  async function c() {
    await Promise.all([o.set([125, 0]), a.set([-125, 0])]), _();
  }
  return kt(() => (c(), () => r = !0)), n.$$set = (w) => {
    "margin" in w && e(0, f = w.margin);
  }, [f, l, i, o, a];
}
class Ft extends bt {
  constructor(t) {
    super(), wt(this, t, qt, pt, yt, { margin: 0 });
  }
}
const {
  SvelteComponent: Lt,
  append: I,
  attr: z,
  binding_callbacks: Le,
  check_outros: Je,
  create_component: Ct,
  create_slot: Mt,
  destroy_component: Vt,
  destroy_each: Ke,
  detach: b,
  element: P,
  empty: R,
  ensure_array_like: te,
  get_all_dirty_from_scope: St,
  get_slot_changes: Nt,
  group_outros: Qe,
  init: Tt,
  insert: g,
  mount_component: zt,
  noop: fe,
  safe_not_equal: jt,
  set_data: S,
  set_style: A,
  space: j,
  text: q,
  toggle_class: V,
  transition_in: G,
  transition_out: O,
  update_slot_base: Pt
} = window.__gradio__svelte__internal, { tick: Zt } = window.__gradio__svelte__internal, { onDestroy: Bt } = window.__gradio__svelte__internal, At = (n) => ({}), Ce = (n) => ({});
function Me(n, t, e) {
  const l = n.slice();
  return l[38] = t[e], l[40] = e, l;
}
function Ve(n, t, e) {
  const l = n.slice();
  return l[38] = t[e], l;
}
function Dt(n) {
  let t, e = (
    /*i18n*/
    n[1]("common.error") + ""
  ), l, i, f;
  const o = (
    /*#slots*/
    n[29].error
  ), a = Mt(
    o,
    n,
    /*$$scope*/
    n[28],
    Ce
  );
  return {
    c() {
      t = P("span"), l = q(e), i = j(), a && a.c(), z(t, "class", "error svelte-1txqlrd");
    },
    m(r, s) {
      g(r, t, s), I(t, l), g(r, i, s), a && a.m(r, s), f = !0;
    },
    p(r, s) {
      (!f || s[0] & /*i18n*/
      2) && e !== (e = /*i18n*/
      r[1]("common.error") + "") && S(l, e), a && a.p && (!f || s[0] & /*$$scope*/
      268435456) && Pt(
        a,
        o,
        r,
        /*$$scope*/
        r[28],
        f ? Nt(
          o,
          /*$$scope*/
          r[28],
          s,
          At
        ) : St(
          /*$$scope*/
          r[28]
        ),
        Ce
      );
    },
    i(r) {
      f || (G(a, r), f = !0);
    },
    o(r) {
      O(a, r), f = !1;
    },
    d(r) {
      r && (b(t), b(i)), a && a.d(r);
    }
  };
}
function Et(n) {
  let t, e, l, i, f, o, a, r, s, _ = (
    /*variant*/
    n[8] === "default" && /*show_eta_bar*/
    n[18] && /*show_progress*/
    n[6] === "full" && Se(n)
  );
  function c(u, k) {
    if (
      /*progress*/
      u[7]
    )
      return Xt;
    if (
      /*queue_position*/
      u[2] !== null && /*queue_size*/
      u[3] !== void 0 && /*queue_position*/
      u[2] >= 0
    )
      return Ht;
    if (
      /*queue_position*/
      u[2] === 0
    )
      return It;
  }
  let w = c(n), h = w && w(n), y = (
    /*timer*/
    n[5] && ze(n)
  );
  const C = [Rt, Ot], p = [];
  function L(u, k) {
    return (
      /*last_progress_level*/
      u[15] != null ? 0 : (
        /*show_progress*/
        u[6] === "full" ? 1 : -1
      )
    );
  }
  ~(f = L(n)) && (o = p[f] = C[f](n));
  let F = !/*timer*/
  n[5] && Ee(n);
  return {
    c() {
      _ && _.c(), t = j(), e = P("div"), h && h.c(), l = j(), y && y.c(), i = j(), o && o.c(), a = j(), F && F.c(), r = R(), z(e, "class", "progress-text svelte-1txqlrd"), V(
        e,
        "meta-text-center",
        /*variant*/
        n[8] === "center"
      ), V(
        e,
        "meta-text",
        /*variant*/
        n[8] === "default"
      );
    },
    m(u, k) {
      _ && _.m(u, k), g(u, t, k), g(u, e, k), h && h.m(e, null), I(e, l), y && y.m(e, null), g(u, i, k), ~f && p[f].m(u, k), g(u, a, k), F && F.m(u, k), g(u, r, k), s = !0;
    },
    p(u, k) {
      /*variant*/
      u[8] === "default" && /*show_eta_bar*/
      u[18] && /*show_progress*/
      u[6] === "full" ? _ ? _.p(u, k) : (_ = Se(u), _.c(), _.m(t.parentNode, t)) : _ && (_.d(1), _ = null), w === (w = c(u)) && h ? h.p(u, k) : (h && h.d(1), h = w && w(u), h && (h.c(), h.m(e, l))), /*timer*/
      u[5] ? y ? y.p(u, k) : (y = ze(u), y.c(), y.m(e, null)) : y && (y.d(1), y = null), (!s || k[0] & /*variant*/
      256) && V(
        e,
        "meta-text-center",
        /*variant*/
        u[8] === "center"
      ), (!s || k[0] & /*variant*/
      256) && V(
        e,
        "meta-text",
        /*variant*/
        u[8] === "default"
      );
      let m = f;
      f = L(u), f === m ? ~f && p[f].p(u, k) : (o && (Qe(), O(p[m], 1, 1, () => {
        p[m] = null;
      }), Je()), ~f ? (o = p[f], o ? o.p(u, k) : (o = p[f] = C[f](u), o.c()), G(o, 1), o.m(a.parentNode, a)) : o = null), /*timer*/
      u[5] ? F && (F.d(1), F = null) : F ? F.p(u, k) : (F = Ee(u), F.c(), F.m(r.parentNode, r));
    },
    i(u) {
      s || (G(o), s = !0);
    },
    o(u) {
      O(o), s = !1;
    },
    d(u) {
      u && (b(t), b(e), b(i), b(a), b(r)), _ && _.d(u), h && h.d(), y && y.d(), ~f && p[f].d(u), F && F.d(u);
    }
  };
}
function Se(n) {
  let t, e = `translateX(${/*eta_level*/
  (n[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      t = P("div"), z(t, "class", "eta-bar svelte-1txqlrd"), A(t, "transform", e);
    },
    m(l, i) {
      g(l, t, i);
    },
    p(l, i) {
      i[0] & /*eta_level*/
      131072 && e !== (e = `translateX(${/*eta_level*/
      (l[17] || 0) * 100 - 100}%)`) && A(t, "transform", e);
    },
    d(l) {
      l && b(t);
    }
  };
}
function It(n) {
  let t;
  return {
    c() {
      t = q("processing |");
    },
    m(e, l) {
      g(e, t, l);
    },
    p: fe,
    d(e) {
      e && b(t);
    }
  };
}
function Ht(n) {
  let t, e = (
    /*queue_position*/
    n[2] + 1 + ""
  ), l, i, f, o;
  return {
    c() {
      t = q("queue: "), l = q(e), i = q("/"), f = q(
        /*queue_size*/
        n[3]
      ), o = q(" |");
    },
    m(a, r) {
      g(a, t, r), g(a, l, r), g(a, i, r), g(a, f, r), g(a, o, r);
    },
    p(a, r) {
      r[0] & /*queue_position*/
      4 && e !== (e = /*queue_position*/
      a[2] + 1 + "") && S(l, e), r[0] & /*queue_size*/
      8 && S(
        f,
        /*queue_size*/
        a[3]
      );
    },
    d(a) {
      a && (b(t), b(l), b(i), b(f), b(o));
    }
  };
}
function Xt(n) {
  let t, e = te(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < e.length; i += 1)
    l[i] = Te(Ve(n, e, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      t = R();
    },
    m(i, f) {
      for (let o = 0; o < l.length; o += 1)
        l[o] && l[o].m(i, f);
      g(i, t, f);
    },
    p(i, f) {
      if (f[0] & /*progress*/
      128) {
        e = te(
          /*progress*/
          i[7]
        );
        let o;
        for (o = 0; o < e.length; o += 1) {
          const a = Ve(i, e, o);
          l[o] ? l[o].p(a, f) : (l[o] = Te(a), l[o].c(), l[o].m(t.parentNode, t));
        }
        for (; o < l.length; o += 1)
          l[o].d(1);
        l.length = e.length;
      }
    },
    d(i) {
      i && b(t), Ke(l, i);
    }
  };
}
function Ne(n) {
  let t, e = (
    /*p*/
    n[38].unit + ""
  ), l, i, f = " ", o;
  function a(_, c) {
    return (
      /*p*/
      _[38].length != null ? Gt : Yt
    );
  }
  let r = a(n), s = r(n);
  return {
    c() {
      s.c(), t = j(), l = q(e), i = q(" | "), o = q(f);
    },
    m(_, c) {
      s.m(_, c), g(_, t, c), g(_, l, c), g(_, i, c), g(_, o, c);
    },
    p(_, c) {
      r === (r = a(_)) && s ? s.p(_, c) : (s.d(1), s = r(_), s && (s.c(), s.m(t.parentNode, t))), c[0] & /*progress*/
      128 && e !== (e = /*p*/
      _[38].unit + "") && S(l, e);
    },
    d(_) {
      _ && (b(t), b(l), b(i), b(o)), s.d(_);
    }
  };
}
function Yt(n) {
  let t = X(
    /*p*/
    n[38].index || 0
  ) + "", e;
  return {
    c() {
      e = q(t);
    },
    m(l, i) {
      g(l, e, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && t !== (t = X(
        /*p*/
        l[38].index || 0
      ) + "") && S(e, t);
    },
    d(l) {
      l && b(e);
    }
  };
}
function Gt(n) {
  let t = X(
    /*p*/
    n[38].index || 0
  ) + "", e, l, i = X(
    /*p*/
    n[38].length
  ) + "", f;
  return {
    c() {
      e = q(t), l = q("/"), f = q(i);
    },
    m(o, a) {
      g(o, e, a), g(o, l, a), g(o, f, a);
    },
    p(o, a) {
      a[0] & /*progress*/
      128 && t !== (t = X(
        /*p*/
        o[38].index || 0
      ) + "") && S(e, t), a[0] & /*progress*/
      128 && i !== (i = X(
        /*p*/
        o[38].length
      ) + "") && S(f, i);
    },
    d(o) {
      o && (b(e), b(l), b(f));
    }
  };
}
function Te(n) {
  let t, e = (
    /*p*/
    n[38].index != null && Ne(n)
  );
  return {
    c() {
      e && e.c(), t = R();
    },
    m(l, i) {
      e && e.m(l, i), g(l, t, i);
    },
    p(l, i) {
      /*p*/
      l[38].index != null ? e ? e.p(l, i) : (e = Ne(l), e.c(), e.m(t.parentNode, t)) : e && (e.d(1), e = null);
    },
    d(l) {
      l && b(t), e && e.d(l);
    }
  };
}
function ze(n) {
  let t, e = (
    /*eta*/
    n[0] ? `/${/*formatted_eta*/
    n[19]}` : ""
  ), l, i;
  return {
    c() {
      t = q(
        /*formatted_timer*/
        n[20]
      ), l = q(e), i = q("s");
    },
    m(f, o) {
      g(f, t, o), g(f, l, o), g(f, i, o);
    },
    p(f, o) {
      o[0] & /*formatted_timer*/
      1048576 && S(
        t,
        /*formatted_timer*/
        f[20]
      ), o[0] & /*eta, formatted_eta*/
      524289 && e !== (e = /*eta*/
      f[0] ? `/${/*formatted_eta*/
      f[19]}` : "") && S(l, e);
    },
    d(f) {
      f && (b(t), b(l), b(i));
    }
  };
}
function Ot(n) {
  let t, e;
  return t = new Ft({
    props: { margin: (
      /*variant*/
      n[8] === "default"
    ) }
  }), {
    c() {
      Ct(t.$$.fragment);
    },
    m(l, i) {
      zt(t, l, i), e = !0;
    },
    p(l, i) {
      const f = {};
      i[0] & /*variant*/
      256 && (f.margin = /*variant*/
      l[8] === "default"), t.$set(f);
    },
    i(l) {
      e || (G(t.$$.fragment, l), e = !0);
    },
    o(l) {
      O(t.$$.fragment, l), e = !1;
    },
    d(l) {
      Vt(t, l);
    }
  };
}
function Rt(n) {
  let t, e, l, i, f, o = `${/*last_progress_level*/
  n[15] * 100}%`, a = (
    /*progress*/
    n[7] != null && je(n)
  );
  return {
    c() {
      t = P("div"), e = P("div"), a && a.c(), l = j(), i = P("div"), f = P("div"), z(e, "class", "progress-level-inner svelte-1txqlrd"), z(f, "class", "progress-bar svelte-1txqlrd"), A(f, "width", o), z(i, "class", "progress-bar-wrap svelte-1txqlrd"), z(t, "class", "progress-level svelte-1txqlrd");
    },
    m(r, s) {
      g(r, t, s), I(t, e), a && a.m(e, null), I(t, l), I(t, i), I(i, f), n[30](f);
    },
    p(r, s) {
      /*progress*/
      r[7] != null ? a ? a.p(r, s) : (a = je(r), a.c(), a.m(e, null)) : a && (a.d(1), a = null), s[0] & /*last_progress_level*/
      32768 && o !== (o = `${/*last_progress_level*/
      r[15] * 100}%`) && A(f, "width", o);
    },
    i: fe,
    o: fe,
    d(r) {
      r && b(t), a && a.d(), n[30](null);
    }
  };
}
function je(n) {
  let t, e = te(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < e.length; i += 1)
    l[i] = De(Me(n, e, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      t = R();
    },
    m(i, f) {
      for (let o = 0; o < l.length; o += 1)
        l[o] && l[o].m(i, f);
      g(i, t, f);
    },
    p(i, f) {
      if (f[0] & /*progress_level, progress*/
      16512) {
        e = te(
          /*progress*/
          i[7]
        );
        let o;
        for (o = 0; o < e.length; o += 1) {
          const a = Me(i, e, o);
          l[o] ? l[o].p(a, f) : (l[o] = De(a), l[o].c(), l[o].m(t.parentNode, t));
        }
        for (; o < l.length; o += 1)
          l[o].d(1);
        l.length = e.length;
      }
    },
    d(i) {
      i && b(t), Ke(l, i);
    }
  };
}
function Pe(n) {
  let t, e, l, i, f = (
    /*i*/
    n[40] !== 0 && Ut()
  ), o = (
    /*p*/
    n[38].desc != null && Ze(n)
  ), a = (
    /*p*/
    n[38].desc != null && /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[40]
    ] != null && Be()
  ), r = (
    /*progress_level*/
    n[14] != null && Ae(n)
  );
  return {
    c() {
      f && f.c(), t = j(), o && o.c(), e = j(), a && a.c(), l = j(), r && r.c(), i = R();
    },
    m(s, _) {
      f && f.m(s, _), g(s, t, _), o && o.m(s, _), g(s, e, _), a && a.m(s, _), g(s, l, _), r && r.m(s, _), g(s, i, _);
    },
    p(s, _) {
      /*p*/
      s[38].desc != null ? o ? o.p(s, _) : (o = Ze(s), o.c(), o.m(e.parentNode, e)) : o && (o.d(1), o = null), /*p*/
      s[38].desc != null && /*progress_level*/
      s[14] && /*progress_level*/
      s[14][
        /*i*/
        s[40]
      ] != null ? a || (a = Be(), a.c(), a.m(l.parentNode, l)) : a && (a.d(1), a = null), /*progress_level*/
      s[14] != null ? r ? r.p(s, _) : (r = Ae(s), r.c(), r.m(i.parentNode, i)) : r && (r.d(1), r = null);
    },
    d(s) {
      s && (b(t), b(e), b(l), b(i)), f && f.d(s), o && o.d(s), a && a.d(s), r && r.d(s);
    }
  };
}
function Ut(n) {
  let t;
  return {
    c() {
      t = q(" /");
    },
    m(e, l) {
      g(e, t, l);
    },
    d(e) {
      e && b(t);
    }
  };
}
function Ze(n) {
  let t = (
    /*p*/
    n[38].desc + ""
  ), e;
  return {
    c() {
      e = q(t);
    },
    m(l, i) {
      g(l, e, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && t !== (t = /*p*/
      l[38].desc + "") && S(e, t);
    },
    d(l) {
      l && b(e);
    }
  };
}
function Be(n) {
  let t;
  return {
    c() {
      t = q("-");
    },
    m(e, l) {
      g(e, t, l);
    },
    d(e) {
      e && b(t);
    }
  };
}
function Ae(n) {
  let t = (100 * /*progress_level*/
  (n[14][
    /*i*/
    n[40]
  ] || 0)).toFixed(1) + "", e, l;
  return {
    c() {
      e = q(t), l = q("%");
    },
    m(i, f) {
      g(i, e, f), g(i, l, f);
    },
    p(i, f) {
      f[0] & /*progress_level*/
      16384 && t !== (t = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[40]
      ] || 0)).toFixed(1) + "") && S(e, t);
    },
    d(i) {
      i && (b(e), b(l));
    }
  };
}
function De(n) {
  let t, e = (
    /*p*/
    (n[38].desc != null || /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[40]
    ] != null) && Pe(n)
  );
  return {
    c() {
      e && e.c(), t = R();
    },
    m(l, i) {
      e && e.m(l, i), g(l, t, i);
    },
    p(l, i) {
      /*p*/
      l[38].desc != null || /*progress_level*/
      l[14] && /*progress_level*/
      l[14][
        /*i*/
        l[40]
      ] != null ? e ? e.p(l, i) : (e = Pe(l), e.c(), e.m(t.parentNode, t)) : e && (e.d(1), e = null);
    },
    d(l) {
      l && b(t), e && e.d(l);
    }
  };
}
function Ee(n) {
  let t, e;
  return {
    c() {
      t = P("p"), e = q(
        /*loading_text*/
        n[9]
      ), z(t, "class", "loading svelte-1txqlrd");
    },
    m(l, i) {
      g(l, t, i), I(t, e);
    },
    p(l, i) {
      i[0] & /*loading_text*/
      512 && S(
        e,
        /*loading_text*/
        l[9]
      );
    },
    d(l) {
      l && b(t);
    }
  };
}
function Jt(n) {
  let t, e, l, i, f;
  const o = [Et, Dt], a = [];
  function r(s, _) {
    return (
      /*status*/
      s[4] === "pending" ? 0 : (
        /*status*/
        s[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(e = r(n)) && (l = a[e] = o[e](n)), {
    c() {
      t = P("div"), l && l.c(), z(t, "class", i = "wrap " + /*variant*/
      n[8] + " " + /*show_progress*/
      n[6] + " svelte-1txqlrd"), V(t, "hide", !/*status*/
      n[4] || /*status*/
      n[4] === "complete" || /*show_progress*/
      n[6] === "hidden"), V(
        t,
        "translucent",
        /*variant*/
        n[8] === "center" && /*status*/
        (n[4] === "pending" || /*status*/
        n[4] === "error") || /*translucent*/
        n[11] || /*show_progress*/
        n[6] === "minimal"
      ), V(
        t,
        "generating",
        /*status*/
        n[4] === "generating"
      ), V(
        t,
        "border",
        /*border*/
        n[12]
      ), A(
        t,
        "position",
        /*absolute*/
        n[10] ? "absolute" : "static"
      ), A(
        t,
        "padding",
        /*absolute*/
        n[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(s, _) {
      g(s, t, _), ~e && a[e].m(t, null), n[31](t), f = !0;
    },
    p(s, _) {
      let c = e;
      e = r(s), e === c ? ~e && a[e].p(s, _) : (l && (Qe(), O(a[c], 1, 1, () => {
        a[c] = null;
      }), Je()), ~e ? (l = a[e], l ? l.p(s, _) : (l = a[e] = o[e](s), l.c()), G(l, 1), l.m(t, null)) : l = null), (!f || _[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      s[8] + " " + /*show_progress*/
      s[6] + " svelte-1txqlrd")) && z(t, "class", i), (!f || _[0] & /*variant, show_progress, status, show_progress*/
      336) && V(t, "hide", !/*status*/
      s[4] || /*status*/
      s[4] === "complete" || /*show_progress*/
      s[6] === "hidden"), (!f || _[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && V(
        t,
        "translucent",
        /*variant*/
        s[8] === "center" && /*status*/
        (s[4] === "pending" || /*status*/
        s[4] === "error") || /*translucent*/
        s[11] || /*show_progress*/
        s[6] === "minimal"
      ), (!f || _[0] & /*variant, show_progress, status*/
      336) && V(
        t,
        "generating",
        /*status*/
        s[4] === "generating"
      ), (!f || _[0] & /*variant, show_progress, border*/
      4416) && V(
        t,
        "border",
        /*border*/
        s[12]
      ), _[0] & /*absolute*/
      1024 && A(
        t,
        "position",
        /*absolute*/
        s[10] ? "absolute" : "static"
      ), _[0] & /*absolute*/
      1024 && A(
        t,
        "padding",
        /*absolute*/
        s[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(s) {
      f || (G(l), f = !0);
    },
    o(s) {
      O(l), f = !1;
    },
    d(s) {
      s && b(t), ~e && a[e].d(), n[31](null);
    }
  };
}
let $ = [], ie = !1;
async function Kt(n, t = !0) {
  if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
    if ($.push(n), !ie)
      ie = !0;
    else
      return;
    await Zt(), requestAnimationFrame(() => {
      let e = [0, 0];
      for (let l = 0; l < $.length; l++) {
        const f = $[l].getBoundingClientRect();
        (l === 0 || f.top + window.scrollY <= e[0]) && (e[0] = f.top + window.scrollY, e[1] = l);
      }
      window.scrollTo({ top: e[0] - 20, behavior: "smooth" }), ie = !1, $ = [];
    });
  }
}
function Qt(n, t, e) {
  let l, { $$slots: i = {}, $$scope: f } = t, { i18n: o } = t, { eta: a = null } = t, { queue: r = !1 } = t, { queue_position: s } = t, { queue_size: _ } = t, { status: c } = t, { scroll_to_output: w = !1 } = t, { timer: h = !0 } = t, { show_progress: y = "full" } = t, { message: C = null } = t, { progress: p = null } = t, { variant: L = "default" } = t, { loading_text: F = "Loading..." } = t, { absolute: u = !0 } = t, { translucent: k = !1 } = t, { border: m = !1 } = t, { autoscroll: le } = t, U, J = !1, Q = 0, D = 0, ne = null, ce = 0, E = null, K, Z = null, de = !0;
  const $e = () => {
    e(25, Q = performance.now()), e(26, D = 0), J = !0, me();
  };
  function me() {
    requestAnimationFrame(() => {
      e(26, D = (performance.now() - Q) / 1e3), J && me();
    });
  }
  function be() {
    e(26, D = 0), J && (J = !1);
  }
  Bt(() => {
    J && be();
  });
  let ge = null;
  function et(d) {
    Le[d ? "unshift" : "push"](() => {
      Z = d, e(16, Z), e(7, p), e(14, E), e(15, K);
    });
  }
  function tt(d) {
    Le[d ? "unshift" : "push"](() => {
      U = d, e(13, U);
    });
  }
  return n.$$set = (d) => {
    "i18n" in d && e(1, o = d.i18n), "eta" in d && e(0, a = d.eta), "queue" in d && e(21, r = d.queue), "queue_position" in d && e(2, s = d.queue_position), "queue_size" in d && e(3, _ = d.queue_size), "status" in d && e(4, c = d.status), "scroll_to_output" in d && e(22, w = d.scroll_to_output), "timer" in d && e(5, h = d.timer), "show_progress" in d && e(6, y = d.show_progress), "message" in d && e(23, C = d.message), "progress" in d && e(7, p = d.progress), "variant" in d && e(8, L = d.variant), "loading_text" in d && e(9, F = d.loading_text), "absolute" in d && e(10, u = d.absolute), "translucent" in d && e(11, k = d.translucent), "border" in d && e(12, m = d.border), "autoscroll" in d && e(24, le = d.autoscroll), "$$scope" in d && e(28, f = d.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*eta, old_eta, queue, timer_start*/
    169869313 && (a === null ? e(0, a = ne) : r && e(0, a = (performance.now() - Q) / 1e3 + a), a != null && (e(19, ge = a.toFixed(1)), e(27, ne = a))), n.$$.dirty[0] & /*eta, timer_diff*/
    67108865 && e(17, ce = a === null || a <= 0 || !D ? null : Math.min(D / a, 1)), n.$$.dirty[0] & /*progress*/
    128 && p != null && e(18, de = !1), n.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (p != null ? e(14, E = p.map((d) => {
      if (d.index != null && d.length != null)
        return d.index / d.length;
      if (d.progress != null)
        return d.progress;
    })) : e(14, E = null), E ? (e(15, K = E[E.length - 1]), Z && (K === 0 ? e(16, Z.style.transition = "0", Z) : e(16, Z.style.transition = "150ms", Z))) : e(15, K = void 0)), n.$$.dirty[0] & /*status*/
    16 && (c === "pending" ? $e() : be()), n.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && U && w && (c === "pending" || c === "complete") && Kt(U, le), n.$$.dirty[0] & /*status, message*/
    8388624, n.$$.dirty[0] & /*timer_diff*/
    67108864 && e(20, l = D.toFixed(1));
  }, [
    a,
    o,
    s,
    _,
    c,
    h,
    y,
    p,
    L,
    F,
    u,
    k,
    m,
    U,
    E,
    K,
    Z,
    ce,
    de,
    ge,
    l,
    r,
    w,
    C,
    le,
    Q,
    D,
    ne,
    f,
    i,
    et,
    tt
  ];
}
class Wt extends Lt {
  constructor(t) {
    super(), Tt(
      this,
      t,
      Qt,
      Jt,
      jt,
      {
        i18n: 1,
        eta: 0,
        queue: 21,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 22,
        timer: 5,
        show_progress: 6,
        message: 23,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 24
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: xt,
  assign: $t,
  create_slot: el,
  detach: tl,
  element: ll,
  get_all_dirty_from_scope: nl,
  get_slot_changes: il,
  get_spread_update: sl,
  init: fl,
  insert: ol,
  safe_not_equal: al,
  set_dynamic_element_data: Ie,
  set_style: M,
  toggle_class: B,
  transition_in: We,
  transition_out: xe,
  update_slot_base: rl
} = window.__gradio__svelte__internal;
function _l(n) {
  let t, e, l;
  const i = (
    /*#slots*/
    n[17].default
  ), f = el(
    i,
    n,
    /*$$scope*/
    n[16],
    null
  );
  let o = [
    { "data-testid": (
      /*test_id*/
      n[7]
    ) },
    { id: (
      /*elem_id*/
      n[2]
    ) },
    {
      class: e = "block " + /*elem_classes*/
      n[3].join(" ") + " svelte-1t38q2d"
    }
  ], a = {};
  for (let r = 0; r < o.length; r += 1)
    a = $t(a, o[r]);
  return {
    c() {
      t = ll(
        /*tag*/
        n[14]
      ), f && f.c(), Ie(
        /*tag*/
        n[14]
      )(t, a), B(
        t,
        "hidden",
        /*visible*/
        n[10] === !1
      ), B(
        t,
        "padded",
        /*padding*/
        n[6]
      ), B(
        t,
        "border_focus",
        /*border_mode*/
        n[5] === "focus"
      ), B(t, "hide-container", !/*explicit_call*/
      n[8] && !/*container*/
      n[9]), M(t, "height", typeof /*height*/
      n[0] == "number" ? (
        /*height*/
        n[0] + "px"
      ) : void 0), M(t, "width", typeof /*width*/
      n[1] == "number" ? `calc(min(${/*width*/
      n[1]}px, 100%))` : void 0), M(
        t,
        "border-style",
        /*variant*/
        n[4]
      ), M(
        t,
        "overflow",
        /*allow_overflow*/
        n[11] ? "visible" : "hidden"
      ), M(
        t,
        "flex-grow",
        /*scale*/
        n[12]
      ), M(t, "min-width", `calc(min(${/*min_width*/
      n[13]}px, 100%))`), M(t, "border-width", "var(--block-border-width)");
    },
    m(r, s) {
      ol(r, t, s), f && f.m(t, null), l = !0;
    },
    p(r, s) {
      f && f.p && (!l || s & /*$$scope*/
      65536) && rl(
        f,
        i,
        r,
        /*$$scope*/
        r[16],
        l ? il(
          i,
          /*$$scope*/
          r[16],
          s,
          null
        ) : nl(
          /*$$scope*/
          r[16]
        ),
        null
      ), Ie(
        /*tag*/
        r[14]
      )(t, a = sl(o, [
        (!l || s & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          r[7]
        ) },
        (!l || s & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          r[2]
        ) },
        (!l || s & /*elem_classes*/
        8 && e !== (e = "block " + /*elem_classes*/
        r[3].join(" ") + " svelte-1t38q2d")) && { class: e }
      ])), B(
        t,
        "hidden",
        /*visible*/
        r[10] === !1
      ), B(
        t,
        "padded",
        /*padding*/
        r[6]
      ), B(
        t,
        "border_focus",
        /*border_mode*/
        r[5] === "focus"
      ), B(t, "hide-container", !/*explicit_call*/
      r[8] && !/*container*/
      r[9]), s & /*height*/
      1 && M(t, "height", typeof /*height*/
      r[0] == "number" ? (
        /*height*/
        r[0] + "px"
      ) : void 0), s & /*width*/
      2 && M(t, "width", typeof /*width*/
      r[1] == "number" ? `calc(min(${/*width*/
      r[1]}px, 100%))` : void 0), s & /*variant*/
      16 && M(
        t,
        "border-style",
        /*variant*/
        r[4]
      ), s & /*allow_overflow*/
      2048 && M(
        t,
        "overflow",
        /*allow_overflow*/
        r[11] ? "visible" : "hidden"
      ), s & /*scale*/
      4096 && M(
        t,
        "flex-grow",
        /*scale*/
        r[12]
      ), s & /*min_width*/
      8192 && M(t, "min-width", `calc(min(${/*min_width*/
      r[13]}px, 100%))`);
    },
    i(r) {
      l || (We(f, r), l = !0);
    },
    o(r) {
      xe(f, r), l = !1;
    },
    d(r) {
      r && tl(t), f && f.d(r);
    }
  };
}
function ul(n) {
  let t, e = (
    /*tag*/
    n[14] && _l(n)
  );
  return {
    c() {
      e && e.c();
    },
    m(l, i) {
      e && e.m(l, i), t = !0;
    },
    p(l, [i]) {
      /*tag*/
      l[14] && e.p(l, i);
    },
    i(l) {
      t || (We(e, l), t = !0);
    },
    o(l) {
      xe(e, l), t = !1;
    },
    d(l) {
      e && e.d(l);
    }
  };
}
function cl(n, t, e) {
  let { $$slots: l = {}, $$scope: i } = t, { height: f = void 0 } = t, { width: o = void 0 } = t, { elem_id: a = "" } = t, { elem_classes: r = [] } = t, { variant: s = "solid" } = t, { border_mode: _ = "base" } = t, { padding: c = !0 } = t, { type: w = "normal" } = t, { test_id: h = void 0 } = t, { explicit_call: y = !1 } = t, { container: C = !0 } = t, { visible: p = !0 } = t, { allow_overflow: L = !0 } = t, { scale: F = null } = t, { min_width: u = 0 } = t, k = w === "fieldset" ? "fieldset" : "div";
  return n.$$set = (m) => {
    "height" in m && e(0, f = m.height), "width" in m && e(1, o = m.width), "elem_id" in m && e(2, a = m.elem_id), "elem_classes" in m && e(3, r = m.elem_classes), "variant" in m && e(4, s = m.variant), "border_mode" in m && e(5, _ = m.border_mode), "padding" in m && e(6, c = m.padding), "type" in m && e(15, w = m.type), "test_id" in m && e(7, h = m.test_id), "explicit_call" in m && e(8, y = m.explicit_call), "container" in m && e(9, C = m.container), "visible" in m && e(10, p = m.visible), "allow_overflow" in m && e(11, L = m.allow_overflow), "scale" in m && e(12, F = m.scale), "min_width" in m && e(13, u = m.min_width), "$$scope" in m && e(16, i = m.$$scope);
  }, [
    f,
    o,
    a,
    r,
    s,
    _,
    c,
    h,
    y,
    C,
    p,
    L,
    F,
    u,
    k,
    w,
    i,
    l
  ];
}
class dl extends xt {
  constructor(t) {
    super(), fl(this, t, cl, ul, al, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 15,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const ml = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], He = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
ml.reduce(
  (n, { color: t, primary: e, secondary: l }) => ({
    ...n,
    [t]: {
      primary: He[t][e],
      secondary: He[t][l]
    }
  }),
  {}
);
const {
  SvelteComponent: bl,
  assign: gl,
  attr: hl,
  create_component: oe,
  destroy_component: ae,
  detach: Xe,
  element: wl,
  get_spread_object: vl,
  get_spread_update: yl,
  init: kl,
  insert: Ye,
  mount_component: re,
  safe_not_equal: pl,
  space: ql,
  toggle_class: Ge,
  transition_in: _e,
  transition_out: ue
} = window.__gradio__svelte__internal;
function Fl(n) {
  var r;
  let t, e, l, i, f;
  const o = [
    { autoscroll: (
      /*gradio*/
      n[5].autoscroll
    ) },
    { i18n: (
      /*gradio*/
      n[5].i18n
    ) },
    /*loading_status*/
    n[4],
    { variant: "center" }
  ];
  let a = {};
  for (let s = 0; s < o.length; s += 1)
    a = gl(a, o[s]);
  return t = new Wt({ props: a }), i = new ut({
    props: {
      min_height: (
        /*loading_status*/
        n[4] && /*loading_status*/
        ((r = n[4]) == null ? void 0 : r.status) !== "complete"
      ),
      value: (
        /*value*/
        n[3]
      ),
      elem_classes: (
        /*elem_classes*/
        n[1]
      ),
      visible: (
        /*visible*/
        n[2]
      )
    }
  }), i.$on(
    "change",
    /*change_handler*/
    n[7]
  ), {
    c() {
      var s;
      oe(t.$$.fragment), e = ql(), l = wl("div"), oe(i.$$.fragment), hl(l, "class", "svelte-gqsrr7"), Ge(
        l,
        "pending",
        /*loading_status*/
        ((s = n[4]) == null ? void 0 : s.status) === "pending"
      );
    },
    m(s, _) {
      re(t, s, _), Ye(s, e, _), Ye(s, l, _), re(i, l, null), f = !0;
    },
    p(s, _) {
      var h, y;
      const c = _ & /*gradio, loading_status*/
      48 ? yl(o, [
        _ & /*gradio*/
        32 && { autoscroll: (
          /*gradio*/
          s[5].autoscroll
        ) },
        _ & /*gradio*/
        32 && { i18n: (
          /*gradio*/
          s[5].i18n
        ) },
        _ & /*loading_status*/
        16 && vl(
          /*loading_status*/
          s[4]
        ),
        o[3]
      ]) : {};
      t.$set(c);
      const w = {};
      _ & /*loading_status*/
      16 && (w.min_height = /*loading_status*/
      s[4] && /*loading_status*/
      ((h = s[4]) == null ? void 0 : h.status) !== "complete"), _ & /*value*/
      8 && (w.value = /*value*/
      s[3]), _ & /*elem_classes*/
      2 && (w.elem_classes = /*elem_classes*/
      s[1]), _ & /*visible*/
      4 && (w.visible = /*visible*/
      s[2]), i.$set(w), (!f || _ & /*loading_status*/
      16) && Ge(
        l,
        "pending",
        /*loading_status*/
        ((y = s[4]) == null ? void 0 : y.status) === "pending"
      );
    },
    i(s) {
      f || (_e(t.$$.fragment, s), _e(i.$$.fragment, s), f = !0);
    },
    o(s) {
      ue(t.$$.fragment, s), ue(i.$$.fragment, s), f = !1;
    },
    d(s) {
      s && (Xe(e), Xe(l)), ae(t, s), ae(i);
    }
  };
}
function Ll(n) {
  let t, e;
  return t = new dl({
    props: {
      visible: (
        /*visible*/
        n[2]
      ),
      elem_id: (
        /*elem_id*/
        n[0]
      ),
      elem_classes: (
        /*elem_classes*/
        n[1]
      ),
      container: !1,
      $$slots: { default: [Fl] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      oe(t.$$.fragment);
    },
    m(l, i) {
      re(t, l, i), e = !0;
    },
    p(l, [i]) {
      const f = {};
      i & /*visible*/
      4 && (f.visible = /*visible*/
      l[2]), i & /*elem_id*/
      1 && (f.elem_id = /*elem_id*/
      l[0]), i & /*elem_classes*/
      2 && (f.elem_classes = /*elem_classes*/
      l[1]), i & /*$$scope, loading_status, value, elem_classes, visible, gradio*/
      318 && (f.$$scope = { dirty: i, ctx: l }), t.$set(f);
    },
    i(l) {
      e || (_e(t.$$.fragment, l), e = !0);
    },
    o(l) {
      ue(t.$$.fragment, l), e = !1;
    },
    d(l) {
      ae(t, l);
    }
  };
}
function Cl(n, t, e) {
  let { label: l } = t, { elem_id: i = "" } = t, { elem_classes: f = [] } = t, { visible: o = !0 } = t, { value: a = "" } = t, { loading_status: r } = t, { gradio: s } = t;
  const _ = () => s.dispatch("change");
  return n.$$set = (c) => {
    "label" in c && e(6, l = c.label), "elem_id" in c && e(0, i = c.elem_id), "elem_classes" in c && e(1, f = c.elem_classes), "visible" in c && e(2, o = c.visible), "value" in c && e(3, a = c.value), "loading_status" in c && e(4, r = c.loading_status), "gradio" in c && e(5, s = c.gradio);
  }, n.$$.update = () => {
    n.$$.dirty & /*label, gradio*/
    96 && s.dispatch("change");
  }, [
    i,
    f,
    o,
    a,
    r,
    s,
    l,
    _
  ];
}
class Ml extends bl {
  constructor(t) {
    super(), kl(this, t, Cl, Ll, pl, {
      label: 6,
      elem_id: 0,
      elem_classes: 1,
      visible: 2,
      value: 3,
      loading_status: 4,
      gradio: 5
    });
  }
}
export {
  Ml as default
};
