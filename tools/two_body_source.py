# tools/two_body_source.py
#
# N4 -- which body the signal is on.
#
# QUESTION
#   Two coupled bodies, one sensor site. Is the signal a property of the body
#   AT RISK, or of the body the SENSOR SITS ON?
#
# The sensor is mounted on body A and the question is about body B. A mode of
# the mounting body reads as a finding about the coupled system unless
# something separates them, and the separator is the pair (amplitude ratio,
# phase) -- neither alone.
#
# TWO REFUSALS BUILT IN, both found while building the fixtures
#
#   1. A PHASE LEAD AGAINST A QUIET CHANNEL IS NOT A MEASUREMENT. If body B
#      barely moves, the cross-correlation peak is set by whatever small
#      variation B does carry, and the lag it returns is a property of that
#      rather than of the coupling. The tool returns the phase as
#      NOT_EVALUABLE and decides on amplitude alone, saying so.
#
#   2. A LAG IS ONLY DETERMINED MODULO THE FORCING PERIOD. A lead of one full
#      forcing period and a lead of zero produce the same cross-correlation
#      peak. Every lead is therefore reported as a within-period value with
#      the ambiguity stated, and no verdict here rests on distinguishing
#      k periods from k+1.
#
# TRAILER_CHANNEL_ABSENT is an absence and is never inferred. A body that was
# not instrumented has not been shown to be quiet.
#
# Standard library only. Parses under Python 3.9.

from __future__ import annotations

import sys
from typing import Dict, List, Optional, Sequence

from typed import (load_threshold, mean, not_evaluable, rms,
                   threshold_report, typed)


def body(name: str, series: Optional[Sequence[float]], sample_rate_hz: float,
         role: str) -> Dict[str, object]:
    """One instrumented body.

    series=None means NOT INSTRUMENTED, which is not the same as instrumented
    and flat. The constructor keeps them apart because the verdict does.
    """
    if role not in ("SENSOR_SITE", "AT_RISK"):
        raise ValueError("role %r is outside the declared vocabulary" % role)
    return {"name": name,
            "series": None if series is None else list(series),
            "sample_rate_hz": sample_rate_hz, "role": role}


def _pearson(xs: Sequence[float], ys: Sequence[float]) -> Optional[float]:
    n = len(xs)
    if n < 2 or len(ys) != n:
        return None
    mx, my = mean(xs), mean(ys)
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    dx = sum((x - mx) ** 2 for x in xs) ** 0.5
    dy = sum((y - my) ** 2 for y in ys) ** 0.5
    if dx == 0 or dy == 0:
        return None
    return num / (dx * dy)


def phase_lead(a: Sequence[float], b: Sequence[float], sample_rate_hz: float,
               forcing_period_s: float,
               variance_floor: Optional[float] = None) -> Dict[str, object]:
    """Lead of A over B, in seconds, reported within one forcing period.

    Positive means A moves first. The return carries `ambiguity` stating that
    any integer number of forcing periods may be added, because a periodic
    cross-correlation cannot tell them apart.
    """
    if variance_floor is None:
        variance_floor = float(load_threshold("n4.phase_variance_floor")["value"])
    ra, rb = rms(a), rms(b)
    if ra is None or rb is None:
        return not_evaluable("a channel is empty")
    if ra <= variance_floor or rb <= variance_floor:
        quiet = "A" if ra <= variance_floor else "B"
        return not_evaluable(
            "channel %s has rms %.3g at or below the variance floor %.3g; a "
            "phase lead against a channel that does not move is a property of "
            "its residual variation, not of the coupling"
            % (quiet, ra if quiet == "A" else rb, variance_floor),
            rms_a=ra, rms_b=rb)

    period_samples = forcing_period_s * sample_rate_hz
    if period_samples < 2:
        return not_evaluable(
            "the forcing period is %.4g s at %.4g Hz, under two samples; the "
            "sampling cannot resolve the feature"
            % (forcing_period_s, sample_rate_hz))
    max_lag = int(round(period_samples))
    if max_lag >= len(a):
        return not_evaluable(
            "one forcing period is %d samples against a record of %d; the "
            "record is shorter than the feature" % (max_lag, len(a)))

    best_lag, best_r = 0, None
    for lag in range(-max_lag, max_lag + 1):
        if lag >= 0:
            xs, ys = a[lag:], b[:len(b) - lag] if lag else b
        else:
            xs, ys = a[:len(a) + lag], b[-lag:]
        m = min(len(xs), len(ys))
        if m < 3:
            continue
        r = _pearson(xs[:m], ys[:m])
        if r is None:
            continue
        if best_r is None or r > best_r:
            best_lag, best_r = lag, r
    if best_r is None:
        return not_evaluable("no lag produced a computable correlation")

    # A positive lag here means A[t+lag] aligns with B[t], i.e. B moves first.
    raw_lead = -best_lag

    # Wrap into the principal branch (-P/2, +P/2]. Found while building F1b: a
    # LAG of 4 samples in a 40-sample period came back as a LEAD of 36, which
    # is the same peak read on the other branch. Without the wrap the branch is
    # chosen by where the search happened to land, and the SIGN of the lead --
    # which is what the agreement check reads -- is set by that accident.
    P = period_samples
    wrapped = raw_lead
    while wrapped > P / 2.0:
        wrapped -= P
    while wrapped <= -P / 2.0:
        wrapped += P

    # Near half a period the two branches are equally close and the sign is not
    # determined at all. The sign is then withheld rather than reported.
    sign_determined = abs(abs(wrapped) - P / 2.0) > max(1.0, 0.05 * P)

    return typed("VALUE", quantity="phase_lead_s",
                 lead_s=wrapped / sample_rate_hz,
                 lead_samples=wrapped,
                 raw_lead_samples=raw_lead,
                 sign_determined=sign_determined,
                 peak_correlation=best_r,
                 forcing_period_s=forcing_period_s,
                 ambiguity="reported in the principal branch (-P/2, +P/2] with "
                           "P = %.4g s; any integer number of forcing periods "
                           "may be added, and a periodic correlation cannot "
                           "tell them apart" % forcing_period_s,
                 sign_note="" if sign_determined else
                           "the lead sits near half a period, where the two "
                           "branches are equally close; the SIGN is not "
                           "determined and is not read",
                 rms_a=ra, rms_b=rb)


def source(a: Dict[str, object], b: Dict[str, object], forcing_period_s: float,
           ratio_hi: Optional[float] = None, ratio_lo: Optional[float] = None,
           clock_tolerance_frac: Optional[float] = None) -> Dict[str, object]:
    """Which body the signal is on.

    Returns SOURCE_A_MODE, SOURCE_B, TRAILER_CHANNEL_ABSENT or NOT_EVALUABLE.
    The amplitude ratio decides; the phase is reported beside it and, where it
    is measurable, is reported as agreeing or not. A phase that disagrees with
    the amplitude verdict does not override it -- it downgrades the return to
    NOT_EVALUABLE, because two readings pointing opposite ways is not a
    verdict with a caveat.
    """
    if ratio_hi is None:
        ratio_hi = float(load_threshold("n4.amplitude_ratio_hi")["value"])
    if ratio_lo is None:
        ratio_lo = float(load_threshold("n4.amplitude_ratio_lo")["value"])
    if clock_tolerance_frac is None:
        clock_tolerance_frac = float(load_threshold("n4.clock_tolerance_frac")["value"])

    if a["role"] != "SENSOR_SITE" or b["role"] != "AT_RISK":
        return not_evaluable("body A must be the SENSOR_SITE and body B the "
                             "AT_RISK body; the question is not symmetric")
    if b["series"] is None:
        return typed("TRAILER_CHANNEL_ABSENT", body=b["name"],
                     reason="the at-risk body carries no channel. It has not "
                            "been shown to be quiet, and no verdict about "
                            "where the signal sits is available from one body.",
                     rms_a=rms(a["series"]) if a["series"] else None)
    if a["series"] is None:
        return not_evaluable("the sensor-site body carries no channel")
    if not a["series"] or not b["series"]:
        return not_evaluable("a channel is empty")

    ra_hz, rb_hz = a["sample_rate_hz"], b["sample_rate_hz"]
    if ra_hz <= 0 or rb_hz <= 0:
        return not_evaluable("a declared sample rate is not positive")
    mismatch = abs(ra_hz - rb_hz) / max(ra_hz, rb_hz)
    if mismatch > clock_tolerance_frac:
        return not_evaluable(
            "declared sample rates differ by %.2f%% (%g Hz vs %g Hz), above "
            "the %.2f%% tolerance; the two records are not on one clock and a "
            "lag between them is not a lag in the system"
            % (100 * mismatch, ra_hz, rb_hz, 100 * clock_tolerance_frac),
            clock_mismatch_frac=mismatch)
    if len(a["series"]) != len(b["series"]):
        return not_evaluable(
            "records differ in length (%d vs %d); they do not cover one "
            "interval" % (len(a["series"]), len(b["series"])))

    ra, rb = rms(a["series"]), rms(b["series"])
    if rb == 0 and ra == 0:
        return not_evaluable("neither body moved; there is no signal to source")
    ratio = float("inf") if rb == 0 else ra / rb
    ph = phase_lead(a["series"], b["series"], ra_hz, forcing_period_s)

    if ratio >= ratio_hi:
        verdict, why = "SOURCE_A_MODE", (
            "amplitude at the sensor site is %.3gx the at-risk body, at or "
            "above the declared ratio %g" % (ratio, ratio_hi))
    elif ratio <= ratio_lo:
        verdict, why = "SOURCE_B", (
            "amplitude at the sensor site is %.3gx the at-risk body, at or "
            "below the declared ratio %g" % (ratio, ratio_lo))
    else:
        return not_evaluable(
            "amplitude ratio %.3g sits between the declared bounds %g and %g; "
            "the two bodies move comparably and this record does not separate "
            "them" % (ratio, ratio_lo, ratio_hi),
            amplitude_ratio=ratio, phase=ph, rms_a=ra, rms_b=rb)

    phase_agrees: Optional[bool] = None
    if ph["kind"] == "VALUE":
        lead = ph["lead_s"]
        if not ph["sign_determined"] or abs(lead) < 1e-12:
            phase_agrees = None
        elif verdict == "SOURCE_A_MODE":
            phase_agrees = lead > 0
        else:
            phase_agrees = lead < 0
        if phase_agrees is False:
            return not_evaluable(
                "amplitude reads %s while the phase has the other body moving "
                "first (lead %+.4g s); two readings pointing opposite ways is "
                "not a verdict" % (verdict, lead),
                amplitude_ratio=ratio, phase=ph, rms_a=ra, rms_b=rb)

    return typed(verdict, amplitude_ratio=ratio, rms_a=ra, rms_b=rb,
                 phase=ph, phase_agrees=phase_agrees, reason=why,
                 decided_by="amplitude_ratio",
                 phase_note=("phase not measurable here; the verdict rests on "
                             "amplitude alone") if ph["kind"] != "VALUE" else
                            "phase reported beside the verdict, not summed with it")


# ---------------------------------------------------------------------------
# fixtures -- CONSTRUCTED
# ---------------------------------------------------------------------------

def _sine(n: int, period_samples: float, amp: float, phase_samples: float = 0.0,
          offset: float = 0.0) -> List[float]:
    import math
    return [offset + amp * math.sin(2 * math.pi * (i - phase_samples) / period_samples)
            for i in range(n)]


FIXTURE_NOTE = """\
CONSTRUCTED. No cab, no trailer, no descent and no accelerometer. The series
below are generated sines, and every verdict is a statement about the
instrument rather than about any vehicle.

WORKED INSTANCE the fixtures are shaped after, NOT RUN
  A tractor cab and its trailer on a serpentine descent: the sensor sits in
  the cab, the body at risk is the trailer, and a cab suspension mode reads
  as a trailer finding unless the two are separated.
  Cross-link: ESP-1 packet, stability-trigger-envelope/
  Status: NAMED_AND_ABSENT. No such folder exists in this repository and no
  such packet is reachable from this session. The pointer is recorded as
  absent rather than reconstructed -- writing a plausible envelope here would
  put a specification in someone else's mouth.
"""


def fixture_f1():
    """A oscillates, B quiet. As specified the lead is ~one forcing period --
    which is exactly the case the tool refuses to read, twice over."""
    n, per = 240, 40.0
    a = _sine(n, per, amp=1.0, phase_samples=-per)  # shifted a whole period
    b = [0.0] * n                                   # quiet
    return (body("cab", a, 100.0, "SENSOR_SITE"),
            body("trailer", b, 100.0, "AT_RISK"), per / 100.0)


def fixture_f2():
    """B oscillates; the sensor site barely moves -> SOURCE_B."""
    n, per = 240, 40.0
    b = _sine(n, per, amp=1.0)
    a = _sine(n, per, amp=0.1, phase_samples=2.0)  # A delayed: B moves first
    return (body("cab", a, 100.0, "SENSOR_SITE"),
            body("trailer", b, 100.0, "AT_RISK"), per / 100.0)


def fixture_f3():
    """B missing. An absence, never inferred."""
    n, per = 240, 40.0
    a = _sine(n, per, amp=1.0)
    return (body("cab", a, 100.0, "SENSOR_SITE"),
            body("trailer", None, 100.0, "AT_RISK"), per / 100.0)


def fixture_f1b():
    """F1 with B instrumented and genuinely moving a little -- the case F1 was
    trying to be. A dominates in amplitude AND the phase is measurable."""
    n, per = 240, 40.0
    a = _sine(n, per, amp=1.0, phase_samples=-4.0)  # A advanced: A leads by 4
    b = _sine(n, per, amp=0.1)
    return (body("cab", a, 100.0, "SENSOR_SITE"),
            body("trailer", b, 100.0, "AT_RISK"), per / 100.0)


# ---------------------------------------------------------------------------
# render
# ---------------------------------------------------------------------------

def render(result: Dict[str, object]) -> List[str]:
    k = result["kind"]
    if k == "TRAILER_CHANNEL_ABSENT":
        return ["  VERDICT: TRAILER_CHANNEL_ABSENT (%s)" % result["body"],
                "    %s" % result["reason"]]
    if k == "NOT_EVALUABLE":
        out = ["  VERDICT: NOT_EVALUABLE", "    %s" % result["reason"]]
        if result.get("amplitude_ratio") is not None:
            out.append("    amplitude ratio A/B: %.4g" % result["amplitude_ratio"])
        return out
    out = ["  VERDICT: %s" % k,
           "    %s" % result["reason"],
           "    amplitude ratio A/B: %.4g   (rms A %.4g, rms B %.4g)"
           % (result["amplitude_ratio"], result["rms_a"], result["rms_b"]),
           "    decided by: %s" % result["decided_by"]]
    ph = result["phase"]
    if ph["kind"] == "VALUE":
        out.append("    phase lead of A over B: %+.4g s (%+d samples), peak r %.3f"
                   % (ph["lead_s"], ph["lead_samples"], ph["peak_correlation"]))
        out.append("    ambiguity: %s" % ph["ambiguity"])
        if not ph["sign_determined"]:
            out.append("    SIGN NOT DETERMINED -- %s" % ph["sign_note"])
        out.append("    phase agrees with amplitude: %s" % result["phase_agrees"])
    else:
        out.append("    phase lead: NOT_EVALUABLE -- %s" % ph["reason"])
    out.append("    %s" % result["phase_note"])
    return out


def run_fixture() -> int:
    print("N4 two_body_source.py -- which body the signal is on")
    print("=" * 72)
    print()
    print(FIXTURE_NOTE)
    print("F1 -- A oscillates, B quiet, A 'leads by one forcing period'")
    a, b, per = fixture_f1()
    for line in render(source(a, b, per)):
        print(line)
    print("    The fixture as specified asks for a lead against a body that")
    print("    does not move, and for a lead of one full period. Neither is")
    print("    readable: the first has no phase to measure, and the second is")
    print("    indistinguishable from zero by any periodic correlation. The")
    print("    amplitude ratio carries the verdict alone, and says so.")
    print()
    print("F1b -- the case F1 was reaching for: B instrumented and moving a")
    print("little, A dominant, a lead of 4 samples inside one period.")
    a, b, per = fixture_f1b()
    for line in render(source(a, b, per)):
        print(line)
    print()
    print("F2 -- B oscillates")
    a, b, per = fixture_f2()
    for line in render(source(a, b, per)):
        print(line)
    print()
    print("F3 -- B missing")
    a, b, per = fixture_f3()
    for line in render(source(a, b, per)):
        print(line)
    print()
    print("CONTRAST -- clocks misaligned beyond the declared tolerance")
    a, b, per = fixture_f1b()
    b2 = body("trailer", b["series"], 97.0, "AT_RISK")
    for line in render(source(a, b2, per)):
        print(line)
    print()
    print("CONTRAST -- the two bodies move comparably; the record does not")
    print("separate them, and that is a result rather than a default verdict.")
    n, p = 240, 40.0
    mid_a = body("cab", _sine(n, p, 1.0), 100.0, "SENSOR_SITE")
    mid_b = body("trailer", _sine(n, p, 0.9), 100.0, "AT_RISK")
    for line in render(source(mid_a, mid_b, p / 100.0)):
        print(line)
    print()
    print("thresholds in force:")
    for line in threshold_report():
        print(line)
    return 0


# ---------------------------------------------------------------------------

def _selftest() -> int:
    checks = 0

    def ck(cond, label):
        nonlocal checks
        checks += 1
        if not cond:
            raise AssertionError("FAILED: " + label)

    # F1: A dominant, B quiet
    a, b, per = fixture_f1()
    r1 = source(a, b, per)
    ck(r1["kind"] == "SOURCE_A_MODE", "F1 returns SOURCE_A_MODE")
    ck(r1["phase"]["kind"] == "NOT_EVALUABLE",
       "F1 refuses a phase lead against a quiet channel")
    ck("does not move" in r1["phase"]["reason"], "the phase refusal says why")
    ck(r1["phase_agrees"] is None, "no phase agreement is claimed in F1")
    ck(r1["decided_by"] == "amplitude_ratio", "F1 is decided on amplitude alone")
    ck("amplitude alone" in r1["phase_note"], "F1 states what carried the verdict")

    # F1b: both measurable, A leads, verdict and phase agree
    a, b, per = fixture_f1b()
    r1b = source(a, b, per)
    ck(r1b["kind"] == "SOURCE_A_MODE", "F1b returns SOURCE_A_MODE")
    ck(r1b["phase"]["kind"] == "VALUE", "F1b has a measurable phase")
    ck(r1b["phase"]["lead_s"] > 0, "F1b reads A as moving first")
    ck(abs(r1b["phase"]["lead_samples"] - 4) <= 1,
       "F1b recovers the constructed 4-sample lead")
    ck(r1b["phase_agrees"] is True, "F1b phase agrees with amplitude")
    ck("principal branch" in r1b["phase"]["ambiguity"]
       and "forcing periods" in r1b["phase"]["ambiguity"],
       "the lead states its period ambiguity")

    # the period ambiguity is real and is demonstrated, not asserted:
    # a lead of one full period reads the same as a lead of zero
    n, p = 240, 40.0
    zero = _sine(n, p, 1.0, phase_samples=0.0)
    onep = _sine(n, p, 1.0, phase_samples=p)
    ref = _sine(n, p, 1.0)
    pz = phase_lead(zero, ref, 100.0, p / 100.0)
    po = phase_lead(onep, ref, 100.0, p / 100.0)
    ck(pz["kind"] == "VALUE" and po["kind"] == "VALUE", "both leads compute")
    ck(abs(pz["lead_s"] - po["lead_s"]) < 1e-9,
       "a lead of one full period is indistinguishable from zero lead")
    # the wrap: a lag of 4 in a 40-sample period must not report as a lead of 36
    lag4 = phase_lead(_sine(n, p, 1.0, phase_samples=4.0), ref, 100.0, p / 100.0)
    ck(lag4["raw_lead_samples"] == 36,
       "the unwrapped search returns the far branch (36 of 40)")
    ck(lag4["lead_samples"] == -4,
       "the wrap puts it in the principal branch as a lag of 4")
    ck(lag4["sign_determined"] is True, "a lag of 4 in 40 has a determined sign")
    # near half a period the sign is withheld
    half = phase_lead(_sine(n, p, 1.0, phase_samples=p / 2.0), ref, 100.0, p / 100.0)
    ck(half["sign_determined"] is False,
       "a lead near half a period has no determined sign")
    ck("not determined" in half["sign_note"], "the withheld sign says why")

    # F2: B dominant
    a, b, per = fixture_f2()
    r2 = source(a, b, per)
    ck(r2["kind"] == "SOURCE_B", "F2 returns SOURCE_B")
    ck(r2["amplitude_ratio"] < 0.34, "F2 amplitude ratio is below the low bound")
    ck(r2["phase"]["kind"] == "VALUE" and r2["phase"]["lead_s"] < 0,
       "F2 reads B as moving first")
    ck(r2["phase_agrees"] is True, "F2 phase agrees with amplitude")

    # F3: absence, never inferred
    a, b, per = fixture_f3()
    r3 = source(a, b, per)
    ck(r3["kind"] == "TRAILER_CHANNEL_ABSENT", "F3 returns the absence")
    ck("has not been shown to be quiet" in r3["reason"],
       "the absence refuses the inference it would most invite")
    ck("amplitude_ratio" not in r3, "no ratio is computed against a missing body")

    # a body instrumented and flat is NOT the same return as a body absent
    flat = body("trailer", [0.0] * 240, 100.0, "AT_RISK")
    rflat = source(a, flat, per)
    ck(rflat["kind"] == "SOURCE_A_MODE",
       "an instrumented flat body gives a verdict where an absent one does not")
    ck(rflat["kind"] != r3["kind"], "absent and flat do not collapse")

    # clocks
    a, b, per = fixture_f1b()
    skew = source(a, body("trailer", b["series"], 97.0, "AT_RISK"), per)
    ck(skew["kind"] == "NOT_EVALUABLE", "misaligned clocks refuse")
    ck("not on one clock" in skew["reason"], "the clock refusal says why")
    near = source(a, body("trailer", b["series"], 100.5, "AT_RISK"), per)
    ck(near["kind"] == "SOURCE_A_MODE", "a mismatch inside tolerance is accepted")

    # unequal lengths do not cover one interval
    short = source(a, body("trailer", b["series"][:100], 100.0, "AT_RISK"), per)
    ck(short["kind"] == "NOT_EVALUABLE", "unequal record lengths refuse")

    # the middle band is a result, not a default
    mid = source(body("cab", _sine(n, p, 1.0), 100.0, "SENSOR_SITE"),
                 body("trailer", _sine(n, p, 0.9), 100.0, "AT_RISK"), p / 100.0)
    ck(mid["kind"] == "NOT_EVALUABLE", "comparable amplitudes refuse")
    ck("does not separate them" in mid["reason"], "the refusal names what is missing")

    # disagreement between the two readings is a refusal, not a caveat
    dis_a = _sine(n, p, 1.0, phase_samples=4.0)    # A dominant but LAGGING
    dis_b = _sine(n, p, 0.1)
    dis = source(body("cab", dis_a, 100.0, "SENSOR_SITE"),
                 body("trailer", dis_b, 100.0, "AT_RISK"), p / 100.0)
    ck(dis["kind"] == "NOT_EVALUABLE",
       "amplitude and phase pointing opposite ways is not a verdict")
    ck("opposite ways" in dis["reason"], "the disagreement is named")

    # sampling that cannot resolve the feature
    ck(phase_lead(_sine(n, p, 1.0), _sine(n, p, 1.0), 1.0, 0.5)["kind"]
       == "NOT_EVALUABLE", "a sub-two-sample period refuses")
    ck(phase_lead(_sine(20, p, 1.0), _sine(20, p, 1.0), 100.0, 1.0)["kind"]
       == "NOT_EVALUABLE", "a record shorter than the feature refuses")

    # roles are not symmetric
    swapped = source(body("trailer", b["series"], 100.0, "AT_RISK"),
                     body("cab", a["series"], 100.0, "SENSOR_SITE"), per)
    ck(swapped["kind"] == "NOT_EVALUABLE", "swapped roles refuse")
    try:
        body("x", [1.0], 1.0, "EITHER")
        ck(False, "an undeclared role was accepted")
    except ValueError:
        ck(True, "an undeclared role is refused")

    # the cross-link is recorded as absent rather than reconstructed
    ck("NAMED_AND_ABSENT" in FIXTURE_NOTE,
       "the ESP-1 cross-link is marked named-and-absent")
    ck("rather than reconstructed" in FIXTURE_NOTE,
       "the cross-link records that nothing was invented in its place")
    ck("CONSTRUCTED" in FIXTURE_NOTE, "the fixtures are marked constructed")

    text = "\n".join(render(r1))
    ck("noise" not in text.lower(), "the render does not return 'noise'")

    print("two_body_source.py: %d checks, 0 failed" % checks)
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(_selftest())
    raise SystemExit(run_fixture())
