!
function(e) {
    function t(t) {
        for (var o, a, u = t[0], c = t[1], f = t[2], p = 0, s = []; p < u.length; p++) a = u[p],
        r[a] && s.push(r[a][0]),
        r[a] = 0;
        for (o in c) Object.prototype.hasOwnProperty.call(c, o) && (e[o] = c[o]);
        for (l && l(t); s.length;) s.shift()();
        return i.push.apply(i, f || []),
        n()
    }
    function n() {
        for (var e, t = 0; t < i.length; t++) {
            for (var n = i[t], o = !0, u = 1; u < n.length; u++) {
                var c = n[u];
                0 !== r[c] && (o = !1)
            }
            o && (i.splice(t--, 1), e = a(a.s = n[0]))
        }
        return e
    }
    var o = {},
    r = {
        1 : 0
    },
    i = [];
    function a(t) {
        if (o[t]) return o[t].exports;
        var n = o[t] = {
            i: t,
            l: !1,
            exports: {}
        };
        return e[t].call(n.exports, n, n.exports, a),
        n.l = !0,
        n.exports
    }
    a.m = e,
    a.c = o,
    a.d = function(e, t, n) {
        a.o(e, t) || Object.defineProperty(e, t, {
            enumerable: !0,
            get: n
        })
    },
    a.r = function(e) {
        "undefined" != typeof Symbol && Symbol.toStringTag && Object.defineProperty(e, Symbol.toStringTag, {
            value: "Module"
        }),
        Object.defineProperty(e, "__esModule", {
            value: !0
        })
    },
    a.t = function(e, t) {
        if (1 & t && (e = a(e)), 8 & t) return e;
        if (4 & t && "object" == typeof e && e && e.__esModule) return e;
        var n = Object.create(null);
        if (a.r(n), Object.defineProperty(n, "default", {
            enumerable: !0,
            value: e
        }), 2 & t && "string" != typeof e) for (var o in e) a.d(n, o,
        function(t) {
            return e[t]
        }.bind(null, o));
        return n
    },
    a.n = function(e) {
        var t = e && e.__esModule ?
        function() {
            return e.
        default
        }:
        function() {
            return e
        };
        return a.d(t, "a", t),
        t
    },
    a.o = function(e, t) {
        return Object.prototype.hasOwnProperty.call(e, t)
    },
    a.p = "";
    var u = window.webpackJsonp = window.webpackJsonp || [],
    c = u.push.bind(u);
    u.push = t,
    u = u.slice();
    for (var f = 0; f < u.length; f++) t(u[f]);
    var l = c;
    i.push([18, 0]),
    n()
} ({
    18 : function(e, t, n) {
        "use strict";
        n.r(t);
        n(14),
        n(20);
        var o, r, i = n(1),
        a = n(6),
        u = n(10),
        c = n(9),
        f = n(2),
        l = n(11),
        p = n(7),
        s = n(8),
        b = n(4);
        function y(e, t) {
            for (var n = 0; n < t.length; n++) {
                var o = t[n];
                o.enumerable = o.enumerable || !1,
                o.configurable = !0,
                "value" in o && (o.writable = !0),
                Object.defineProperty(e, o.key, o)
            }
        }
        function d(e, t, n) {
            return (d = "undefined" != typeof Reflect && Reflect.get ? Reflect.get: function(e, t, n) {
                var o = function(e, t) {
                    for (; ! Object.prototype.hasOwnProperty.call(e, t) && null !== (e = w(e)););
                    return e
                } (e, t);
                if (o) {
                    var r = Object.getOwnPropertyDescriptor(o, t);
                    return r.get ? r.get.call(n) : r.value
                }
            })(e, t, n || e)
        }
        function h(e) {
            return (h = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ?
            function(e) {
                return typeof e
            }: function(e) {
                return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol": typeof e
            })(e)
        }
        function O(e, t) {
            if (! (e instanceof t)) throw new TypeError("Cannot call a class as a function")
        }
        function v(e, t) {
            return ! t || "object" !== h(t) && "function" != typeof t ?
            function(e) {
                if (void 0 === e) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
                return e
            } (e) : t
        }
        function w(e) {
            return (w = Object.setPrototypeOf ? Object.getPrototypeOf: function(e) {
                return e.__proto__ || Object.getPrototypeOf(e)
            })(e)
        }
        function j(e, t) {
            if ("function" != typeof t && null !== t) throw new TypeError("Super expression must either be null or a function");
            e.prototype = Object.create(t && t.prototype, {
                constructor: {
                    value: e,
                    writable: !0,
                    configurable: !0
                }
            }),
            t && m(e, t)
        }
        function m(e, t) {
            return (m = Object.setPrototypeOf ||
            function(e, t) {
                return e.__proto__ = t,
                e
            })(e, t)
        }
        var g = new(o = Object(p.a)({
            x: 4,
            y: 4
        }), Object(s.a)(r = o(r = function(e) {
            function t() {
                return O(this, t),
                v(this, w(t).apply(this, arguments))
            }
            return j(t, a["a"]),
            t
        } ()) || r) || r),
        P = new u.a("", {
            color: "#fff",
            size: b.a.isMobile ? .5 : .6
        });
        P.position.x -= .5 * P.basePosition,
        g.add(P);
        var _ = ["#4062BB", "#52489C", "#59C3C3", "#F45B69", "#F45B69"].map(function(e) {
            return new i.Color(e)
        }),
        S = new(function(e) {
            function t() {
                return O(this, t),
                v(this, w(t).apply(this, arguments))
            }
            var n, o, r;
            return j(t, c["a"]),
            n = t,
            (o = [{
                key: "addLine",
                value: function() {
                    d(w(t.prototype), "addLine", this).call(this, {
                        length: Object(f.a)(8, 15),
                        visibleLength: Object(f.a)(.05, .2),
                        position: new i.Vector3(1.5 * (Math.random() - .5), Math.random() - 1, 2 * (Math.random() - .5)).multiplyScalar(Object(f.a)(5, 20)),
                        turbulence: new i.Vector3(Object(f.a)( - 2, 2), Object(f.a)(0, 2), Object(f.a)( - 2, 2)),
                        orientation: new i.Vector3(Object(f.a)( - .8, .8), 1, 1),
                        speed: Object(f.a)(.004, .008),
                        color: Object(l.a)(_)
                    })
                }
            }]) && y(n.prototype, o),
            r && y(n, r),
            t
        } ())({
            frequency: .5
        },
        {
            width: .1,
            nbrOfPoints: 5
        });
        g.add(S),
        g.start();
        var x = new TimelineLite({
            delay: .2,
            onStart: function() {
                S.start()
            }
        });
        x.to(".overlay", .6, {
            autoAlpha: 0
        }),
        x.fromTo(g.lookAt, 3, {
            y: -4
        },
        {
            y: 0,
            ease: Power3.easeOut
        },
        "-=0.4"),
        x.add(P.show, "-=2"),
        b.a.onHide(function(e) {
            var t = new TimelineLite;
            t.to(g.lookAt, 2, {
                y: -6,
                ease: Power3.easeInOut
            }),
            t.add(P.hide, 0),
            t.add(S.stop),
            t.to(".overlay", .5, {
                autoAlpha: 1,
                onComplete: e
            },
            "-=1.5")
        })
    },
    20 : function(e, t, n) {}
});