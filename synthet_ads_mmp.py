#!/usr/bin/env python3
# synthet_ads_mmp.py
# Generate synthetic Facebook Ads, Google Ads, and MMP (Adjust/AppsFlyer) datasets for the last N days.
# Outputs: CSVs with realistic distributions and consistent campaign_id/name references.

import csv
import argparse
import random
from datetime import date, timedelta
import math
import sys

# -----------------------------
# Configurable generators
# -----------------------------
OS_LIST = ["Android", "iOS"]
OBJECTIVES = ["Prospecting", "Retargeting", "Installs", "Search"]
REGIONS = ["US", "EU", "LATAM", "APAC", "MENA"]
CREATIVES = ["Video", "Static", "Carousel", "UGC", "Playables"]
GOOGLE_TYPES = ["Search - Brand - Exact", "Search - Non-Brand - Broad", "UAC - Installs", "UAC - Value"]
FACEBOOK_TYPES = ["UA - Prospecting - Broad", "UA - Retargeting - Value", "UA - Lookalike - 1%", "UA - Lookalike - 5%"]

# Seed for reproducibility
DEFAULT_SEED = 42

def parse_args():
    parser = argparse.ArgumentParser(description="Synthesize Facebook/Google ads and MMP datasets for last N days.")
    parser.add_argument("--days", type=int, default=14, help="Number of last days to generate (default: 14)")
    parser.add_argument("--fb-campaigns", type=int, default=350, help="Number of Facebook campaigns (default: 350)")
    parser.add_argument("--gg-campaigns", type=int, default=350, help="Number of Google campaigns (default: 350)")
    parser.add_argument("--currency", type=str, default="USD", help="Currency label for spend/revenue (metadata only)")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="Random seed (default: 42)")
    parser.add_argument("--out-prefix", type=str, default="", help="Optional prefix for output filenames")
    return parser.parse_args()

def daterange_last_n_days(n_days):
    start = date.today() - timedelta(days=n_days)
    return [start + timedelta(days=i) for i in range(n_days)]

def make_campaign_catalog(num, source):
    """Create a list of (campaign_id, campaign_name, attributes) per source."""
    catalog = []
    for idx in range(num):
        os = random.choice(OS_LIST)
        region = random.choice(REGIONS)
        creative = random.choice(CREATIVES)
        if source == "Facebook Ads":
            ctype = random.choice(FACEBOOK_TYPES)
            cid = f"FB-{100000 + idx}"
            cname = f"{ctype} | {os} | {region} | {creative}"
        else:
            ctype = random.choice(GOOGLE_TYPES)
            cid = f"GG-{200000 + idx}"
            cname = f"{ctype} | {os} | {region} | {creative}"
        catalog.append((cid, cname, os, region, creative, ctype))
    return catalog

# -----------------------------
# Metric synthesis functions
# -----------------------------
def clamp(x, lo, hi):
    return max(lo, min(hi, x))

def synthetic_impressions(source, campaign_type, os):
    base = 15000
    if source == "Facebook Ads":
        base = 18000
        if "Lookalike" in campaign_type: base *= 1.1
        if "Retargeting" in campaign_type: base *= 0.7
    else:
        base = 14000
        if "Search" in campaign_type: base *= 0.8
        if "UAC" in campaign_type: base *= 1.2
    if os == "iOS": base *= 0.9
    m = math.log(base + 1)
    s = 0.35
    val = int(math.exp(random.gauss(m, s)))
    return clamp(val, 2000, 250000)

def synthetic_ctr(source, campaign_type):
    if source == "Facebook Ads":
        base = 0.015 if "Retargeting" in campaign_type else 0.025
        if "Lookalike" in campaign_type: base += 0.005
    else:
        base = 0.02 if "Search" in campaign_type else 0.03
        if "Brand" in campaign_type: base += 0.01
    noise = random.uniform(-0.01, 0.02)
    return clamp(base + noise, 0.002, 0.08)

def synthetic_cpc(source, campaign_type, os, region):
    base = 0.3
    if source == "Facebook Ads":
        base = 0.25
        if "Retargeting" in campaign_type: base += 0.1
    else:
        base = 0.35
        if "Brand" in campaign_type: base -= 0.05
        if "UAC" in campaign_type: base += 0.05
    if os == "iOS": base += 0.05
    if region in ["US", "EU"]: base += 0.05
    noise = random.uniform(-0.1, 0.2)
    return round(clamp(base + noise, 0.10, 1.50), 4)

def synthetic_cr(source, campaign_type, os):
    base = 0.08
    if source == "Google Ads":
        if "UAC" in campaign_type: base = 0.18
        elif "Search" in campaign_type: base = 0.12
    else:
        if "Retargeting" in campaign_type: base = 0.14
        elif "Lookalike" in campaign_type: base = 0.10
        else: base = 0.09
    if os == "iOS": base -= 0.02
    noise = random.uniform(-0.05, 0.12)
    return clamp(base + noise, 0.02, 0.35)

def synthetic_d1_arpu(os, region, campaign_type):
    base = 2.50
    if os == "iOS": base += 0.50
    if region in ["US", "EU"]: base += 0.50
    if "Retargeting" in campaign_type or "Value" in campaign_type: base += 0.75
    noise = random.uniform(-0.5, 1.5)
    return round(clamp(base + noise, 0.50, 7.00), 4)

def synthetic_d7_multiplier(campaign_type):
    base = 4.0
    if "Value" in campaign_type: base += 1.0
    if "Brand" in campaign_type: base -= 0.5
    noise = random.uniform(-1.0, 1.5)
    return round(clamp(base + noise, 2.5, 6.0), 3)

# -----------------------------
# Row synthesis
# -----------------------------
def synth_ads_row(dt, source, cid, cname, os, region, ctype):
    imps = synthetic_impressions(source, ctype, os)
    ctr = synthetic_ctr(source, ctype)
    clicks = min(imps, int(imps * ctr))
    cpc = synthetic_cpc(source, ctype, os, region)
    spend = round(clicks * cpc, 2)
    cr = synthetic_cr(source, ctype, os)
    installs = int(clicks * cr)
    return {
        "date": dt.isoformat(),
        "source": source,
        "campaign_id": cid,
        "campaign_name": cname,
        "impressions": imps,
        "clicks": clicks,
        "spend": spend,
        "installs": installs
    }

def synth_mmp_row(dt, cid, cname, os, region, ctype, reference_installs):
    """Generates MMP data based on a reference number of installs from an ad platform."""
    # MMP installs are based on ads installs, with slight variance
    variance = random.uniform(-0.05, 0.05) # Reduced variance for closer match
    installs = max(0, int(reference_installs * (1 + variance)))
    d1_arpu = synthetic_d1_arpu(os, region, ctype)
    d7_mult = synthetic_d7_multiplier(ctype)
    d1_rev = round(installs * d1_arpu, 2)
    d7_rev = round(d1_rev * d7_mult, 2)
    return {
        "date": dt.isoformat(),
        "campaign_id": cid,
        "campaign_name": cname,
        "installs": installs,
        "d1_revenue": d1_rev,
        "d7_revenue": d7_rev
    }

# -----------------------------
# Main generation routine
# -----------------------------
def main():
    args = parse_args()
    random.seed(args.seed)

    days_list = daterange_last_n_days(args.days)

    fb_catalog = make_campaign_catalog(args.fb_campaigns, "Facebook Ads")
    gg_catalog = make_campaign_catalog(args.gg_campaigns, "Google Ads")

    prefix = (args.out_prefix + "_") if args.out_prefix else ""
    fb_out = f"{prefix}ads_facebook_ads_last_{args.days}_days.csv"
    gg_out = f"{prefix}ads_google_ads_last_{args.days}_days.csv"
    mmp_out = f"{prefix}mmp_last_{args.days}_days.csv"

    # Open all files at once to write rows concurrently
    with open(fb_out, "w", newline="", encoding="utf-8") as fbf, \
         open(gg_out, "w", newline="", encoding="utf-8") as ggf, \
         open(mmp_out, "w", newline="", encoding="utf-8") as mmf:

        # Create CSV writers
        fb_writer = csv.writer(fbf)
        gg_writer = csv.writer(ggf)
        mmp_writer = csv.writer(mmf)

        # Write headers
        fb_writer.writerow(["date", "source", "campaign_id", "campaign_name", "impressions", "clicks", "spend", "installs"])
        gg_writer.writerow(["date", "source", "campaign_id", "campaign_name", "impressions", "clicks", "spend", "installs"])
        mmp_writer.writerow(["date", "campaign_id", "campaign_name", "installs", "d1_revenue", "d7_revenue"])

        for dt in days_list:
            # --- Process Facebook campaigns ---
            for cid, cname, os, region, creative, ctype in fb_catalog:
                # 1. Generate the ads row
                ads_row = synth_ads_row(dt, "Facebook Ads", cid, cname, os, region, ctype)
                fb_writer.writerow(ads_row.values())

                # 2. Generate the corresponding MMP row using installs from the ads row
                mmp_row = synth_mmp_row(dt, cid, cname, os, region, ctype, reference_installs=ads_row["installs"])
                mmp_writer.writerow(mmp_row.values())

            # --- Process Google campaigns ---
            for cid, cname, os, region, creative, ctype in gg_catalog:
                # 1. Generate the ads row
                ads_row = synth_ads_row(dt, "Google Ads", cid, cname, os, region, ctype)
                gg_writer.writerow(ads_row.values())

                # 2. Generate the corresponding MMP row using installs from the ads row
                mmp_row = synth_mmp_row(dt, cid, cname, os, region, ctype, reference_installs=ads_row["installs"])
                mmp_writer.writerow(mmp_row.values())


    fb_rows = args.days * args.fb_campaigns
    gg_rows = args.days * args.gg_campaigns
    mmp_rows = args.days * (args.fb_campaigns + args.gg_campaigns)
    print(f"[OK] Wrote:\n - {fb_out} ({fb_rows} rows)\n - {gg_out} ({gg_rows} rows)\n - {mmp_out} ({mmp_rows} rows)")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)