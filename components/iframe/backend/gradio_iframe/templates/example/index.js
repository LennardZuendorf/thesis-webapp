const {
  SvelteComponent: c,
  attr: u,
  detach: r,
  element: o,
  init: d,
  insert: g,
  noop: _,
  safe_not_equal: v,
  toggle_class: s
} = window.__gradio__svelte__internal;
function y(n) {
  let e;
  return {
    c() {
      e = o("div"), u(e, "class", "prose svelte-180qqaf"), s(
        e,
        "table",
        /*type*/
        n[1] === "table"
      ), s(
        e,
        "gallery",
        /*type*/
        n[1] === "gallery"
      ), s(
        e,
        "selected",
        /*selected*/
        n[2]
      );
    },
    m(l, t) {
      g(l, e, t), e.innerHTML = /*value*/
      n[0];
    },
    p(l, [t]) {
      t & /*value*/
      1 && (e.innerHTML = /*value*/
      l[0]), t & /*type*/
      2 && s(
        e,
        "table",
        /*type*/
        l[1] === "table"
      ), t & /*type*/
      2 && s(
        e,
        "gallery",
        /*type*/
        l[1] === "gallery"
      ), t & /*selected*/
      4 && s(
        e,
        "selected",
        /*selected*/
        l[2]
      );
    },
    i: _,
    o: _,
    d(l) {
      l && r(e);
    }
  };
}
function m(n, e, l) {
  let { value: t } = e, { type: i } = e, { selected: f = !1 } = e;
  return n.$$set = (a) => {
    "value" in a && l(0, t = a.value), "type" in a && l(1, i = a.type), "selected" in a && l(2, f = a.selected);
  }, [t, i, f];
}
class b extends c {
  constructor(e) {
    super(), d(this, e, m, y, v, { value: 0, type: 1, selected: 2 });
  }
}
export {
  b as default
};
