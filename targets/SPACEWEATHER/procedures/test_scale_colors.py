# Test script to inject different NOAA Space Weather Scale values
# and verify the widget displays the correct colors.
#
# Scale color mapping:
#   0 = green       (none)
#   1 = light-green  (minor)
#   2 = yellow       (moderate)
#   3 = orange       (strong)
#   4 = deep-orange  (severe)
#   5 = red          (extreme)

import time

TARGET = "SPACEWEATHER"
SCALES_PKT = "SCALES_RESPONSE"
ALERTS_PKT = "ALERTS_RESPONSE"
DELAY = 5  # seconds between each test case

def inject_scales(r_scale, r_text, s_scale, s_text, g_scale, g_text,
                  today_r_minor="0", today_r_major="0", today_s="0",
                  today_g_scale="0", today_g_text="none",
                  tmrw_r_minor="0", tmrw_r_major="0", tmrw_s="0",
                  tmrw_g_scale="0", tmrw_g_text="none",
                  d3_r_minor="0", d3_r_major="0", d3_s="0",
                  d3_g_scale="0", d3_g_text="none"):
    inject_tlm(TARGET, SCALES_PKT, {
        "CURRENT_DATESTAMP": "2026-03-16",
        "CURRENT_TIMESTAMP": "12:00:00",
        "R_SCALE": str(r_scale),
        "R_TEXT": r_text,
        "S_SCALE": str(s_scale),
        "S_TEXT": s_text,
        "G_SCALE": str(g_scale),
        "G_TEXT": g_text,
        "TODAY_R_MINOR_PROB": str(today_r_minor),
        "TODAY_R_MAJOR_PROB": str(today_r_major),
        "TODAY_S_PROB": str(today_s),
        "TODAY_G_SCALE": str(today_g_scale),
        "TODAY_G_TEXT": today_g_text,
        "TOMORROW_DATE": "2026-03-17",
        "TOMORROW_R_MINOR_PROB": str(tmrw_r_minor),
        "TOMORROW_R_MAJOR_PROB": str(tmrw_r_major),
        "TOMORROW_S_PROB": str(tmrw_s),
        "TOMORROW_G_SCALE": str(tmrw_g_scale),
        "TOMORROW_G_TEXT": tmrw_g_text,
        "DAY3_DATE": "2026-03-18",
        "DAY3_R_MINOR_PROB": str(d3_r_minor),
        "DAY3_R_MAJOR_PROB": str(d3_r_major),
        "DAY3_S_PROB": str(d3_s),
        "DAY3_G_SCALE": str(d3_g_scale),
        "DAY3_G_TEXT": d3_g_text,
    }, type="CONVERTED")

def inject_alert(product_id, issue_datetime, message):
    inject_tlm(TARGET, ALERTS_PKT, {
        "PRODUCT_ID": product_id,
        "ISSUE_DATETIME": issue_datetime,
        "MESSAGE": message,
    }, type="CONVERTED")

# -------------------------------------------------------------------
# Test 1: All clear (green across the board)
# -------------------------------------------------------------------
print("Test 1: All clear - everything green (scale 0)")
inject_scales(0, "none", 0, "none", 0, "none")
inject_alert("TEST", "2026-03-16 12:00:00.000", "Test: All conditions nominal.")
wait(DELAY)

# -------------------------------------------------------------------
# Test 2: Minor activity (light-green)
# -------------------------------------------------------------------
print("Test 2: Minor activity - all scale 1 (light-green)")
inject_scales(1, "minor", 1, "minor", 1, "minor",
              today_r_minor="25", today_r_major="5", today_s="10",
              today_g_scale="1", today_g_text="minor")
inject_alert("K04W", "2026-03-16 12:01:00.000",
             "Test: Minor geomagnetic storm watch in effect.")
wait(DELAY)

# -------------------------------------------------------------------
# Test 3: Moderate activity (yellow)
# -------------------------------------------------------------------
print("Test 3: Moderate activity - all scale 2 (yellow)")
inject_scales(2, "moderate", 2, "moderate", 2, "moderate",
              today_r_minor="50", today_r_major="15", today_s="25",
              today_g_scale="2", today_g_text="moderate",
              tmrw_r_minor="30", tmrw_r_major="10", tmrw_s="15",
              tmrw_g_scale="1", tmrw_g_text="minor")
inject_alert("K05A", "2026-03-16 12:02:00.000",
             "Test: Moderate geomagnetic storm alert.")
wait(DELAY)

# -------------------------------------------------------------------
# Test 4: Strong activity (orange)
# -------------------------------------------------------------------
print("Test 4: Strong activity - all scale 3 (orange)")
inject_scales(3, "strong", 3, "strong", 3, "strong",
              today_r_minor="75", today_r_major="40", today_s="50",
              today_g_scale="3", today_g_text="strong",
              tmrw_r_minor="50", tmrw_r_major="25", tmrw_s="30",
              tmrw_g_scale="2", tmrw_g_text="moderate",
              d3_r_minor="30", d3_r_major="10", d3_s="15",
              d3_g_scale="1", d3_g_text="minor")
inject_alert("EF3A", "2026-03-16 12:03:00.000",
             "Test: Strong radio blackout and geomagnetic storm in progress.")
wait(DELAY)

# -------------------------------------------------------------------
# Test 5: Severe activity (deep-orange)
# -------------------------------------------------------------------
print("Test 5: Severe activity - all scale 4 (deep-orange)")
inject_scales(4, "severe", 4, "severe", 4, "severe",
              today_r_minor="90", today_r_major="60", today_s="70",
              today_g_scale="4", today_g_text="severe",
              tmrw_r_minor="70", tmrw_r_major="40", tmrw_s="50",
              tmrw_g_scale="3", tmrw_g_text="strong",
              d3_r_minor="40", d3_r_major="15", d3_s="25",
              d3_g_scale="2", d3_g_text="moderate")
inject_alert("K06A", "2026-03-16 12:04:00.000",
             "Test: Severe geomagnetic storm - widespread GPS and power grid impacts.")
wait(DELAY)

# -------------------------------------------------------------------
# Test 6: Extreme activity (red)
# -------------------------------------------------------------------
print("Test 6: Extreme activity - all scale 5 (red)")
inject_scales(5, "extreme", 5, "extreme", 5, "extreme",
              today_r_minor="99", today_r_major="80", today_s="90",
              today_g_scale="5", today_g_text="extreme",
              tmrw_r_minor="80", tmrw_r_major="60", tmrw_s="70",
              tmrw_g_scale="4", tmrw_g_text="severe",
              d3_r_minor="50", d3_r_major="30", d3_s="40",
              d3_g_scale="3", d3_g_text="strong")
inject_alert("A30F", "2026-03-16 12:05:00.000",
             "Test: EXTREME space weather event - complete HF radio blackout, grid collapse possible.")
wait(DELAY)

# -------------------------------------------------------------------
# Test 7: Mixed levels (one of each)
# -------------------------------------------------------------------
print("Test 7: Mixed - R0 (green), S3 (orange), G5 (red)")
inject_scales(0, "none", 3, "strong", 5, "extreme",
              today_r_minor="10", today_r_major="1", today_s="50",
              today_g_scale="5", today_g_text="extreme",
              tmrw_r_minor="5", tmrw_r_major="1", tmrw_s="30",
              tmrw_g_scale="3", tmrw_g_text="strong",
              d3_r_minor="5", d3_r_major="1", d3_s="15",
              d3_g_scale="1", d3_g_text="minor")
inject_alert("BHIS", "2026-03-16 12:06:00.000",
             "Test: Mixed conditions - radio clear, strong radiation, extreme geomagnetic storm.")
wait(DELAY)

# -------------------------------------------------------------------
# Reset to nominal
# -------------------------------------------------------------------
print("Resetting to nominal conditions")
inject_scales(0, "none", 0, "none", 0, "none")
inject_alert("TEST", "2026-03-16 12:07:00.000", "Test complete. Conditions reset to nominal.")

print("All tests complete!")
