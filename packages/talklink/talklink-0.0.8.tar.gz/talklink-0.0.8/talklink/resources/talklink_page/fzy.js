(function () {
    const SCORE_MIN = -1 / 0,
      SCORE_MAX = 1 / 0,
      SCORE_GAP_LEADING = -0.000005,
      SCORE_GAP_TRAILING = -0.000005,
      SCORE_GAP_INNER = -0.000001,
      SCORE_MATCH_CONSECUTIVE = 1,
      SCORE_MATCH_SLASH = 0.4,
      SCORE_MATCH_WORD = 0.95,
      SCORE_MATCH_CAPITAL = 0.1,
      SCORE_MATCH_DOT = 0.6;

    function islower(r) {
      return r.toLowerCase() === r;
    }
    function isupper(r) {
      return r.toUpperCase() === r;
    }
    function precompute_bonus(r) {
      for (var C = r.length, _ = new Array(C), e = "/", t = 0; t < C; t++) {
        var A = r[t];
        "/" === e
          ? (_[t] = SCORE_MATCH_SLASH)
          : "-" === e || "_" === e || " " === e
          ? (_[t] = SCORE_MATCH_WORD)
          : "." === e
          ? (_[t] = SCORE_MATCH_DOT)
          : islower(e) && isupper(A)
          ? (_[t] = SCORE_MATCH_CAPITAL)
          : (_[t] = 0),
          (e = A);
      }
      return _;
    }
    function compute(r, C, _, e) {
      for (
        var t = r.length,
          A = C.length,
          E = r.toLowerCase(),
          O = C.toLowerCase(),
          o = precompute_bonus(C),
          S = 0;
        S < t;
        S++
      ) {
        (_[S] = new Array(A)), (e[S] = new Array(A));
        for (
          var R = SCORE_MIN,
            n = S === t - 1 ? SCORE_GAP_TRAILING : SCORE_GAP_INNER,
            s = 0;
          s < A;
          s++
        )
          if (E[S] === O[s]) {
            var M = SCORE_MIN;
            S
              ? s &&
                (M = Math.max(
                  e[S - 1][s - 1] + o[s],
                  _[S - 1][s - 1] + SCORE_MATCH_CONSECUTIVE
                ))
              : (M = s * SCORE_GAP_LEADING + o[s]),
              (_[S][s] = M),
              (e[S][s] = R = Math.max(M, R + n));
          } else (_[S][s] = SCORE_MIN), (e[S][s] = R += n);
      }
    }
    function score(r, C) {
      var _ = r.length,
        e = C.length;
      if (!_ || !e) return SCORE_MIN;
      if (_ === e) return SCORE_MAX;
      if (e > 1024) return SCORE_MIN;
      var t = new Array(_),
        A = new Array(_);
      return compute(r, C, t, A), A[_ - 1][e - 1];
    }
    function positions(r, C) {
      var _ = r.length,
        e = C.length,
        t = new Array(_);
      if (!_ || !e) return t;
      if (_ === e) {
        for (var A = 0; A < _; A++) t[A] = A;
        return t;
      }
      if (e > 1024) return t;
      var E = new Array(_),
        O = new Array(_);
      compute(r, C, E, O);
      for (var o = !1, S = (A = _ - 1, e - 1); A >= 0; A--)
        for (; S >= 0; S--)
          if (
            E[A][S] !== SCORE_MIN &&
            (o || E[A][S] === O[A][S])
          ) {
            (o = A && S && O[A][S] === E[A - 1][S - 1] + SCORE_MATCH_CONSECUTIVE),
              (t[A] = S--);
            break;
          }
      return t;
    }
    function hasMatch(r, C) {
      (r = r.toLowerCase()), (C = C.toLowerCase());
      for (var _ = r.length, e = 0, t = 0; e < _; e += 1)
        if (0 === (t = C.indexOf(r[e], t) + 1)) return !1;
      return !0;
    }

    // Expose functions and constants to the global scope
    window.stringScoring = {
      SCORE_GAP_INNER,
      SCORE_GAP_LEADING,
      SCORE_GAP_TRAILING,
      SCORE_MATCH_CAPITAL,
      SCORE_MATCH_CONSECUTIVE,
      SCORE_MATCH_DOT,
      SCORE_MATCH_SLASH,
      SCORE_MATCH_WORD,
      SCORE_MAX,
      SCORE_MIN,
      hasMatch,
      positions,
      score,
    };
  })();