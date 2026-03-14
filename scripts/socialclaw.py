#!/usr/bin/env python3
"""
SocialClaw — X/Twitter Marketing Intelligence Workflows

Three core workflows:
  1. insight @username  — deep-dive account analysis
  2. radar <topic>      — trending topics + content opportunities
  3. compare @a @b      — side-by-side competitor analysis
"""

import json
import os
import subprocess
import sys
from typing import Any, Dict, Optional

# Auto-install dependencies if missing
def _ensure_deps():
    try:
        import blockrun_llm  # noqa: F401
    except ImportError:
        print("  Installing blockrun-llm[solana]...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-q", "blockrun-llm[solana]>=0.8.0"],
            stdout=subprocess.DEVNULL,
        )

_ensure_deps()

# Ensure blockrun-llm is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from scripts.utils.config import get_chain, get_wallet_source, get_private_key
except ImportError:
    from utils.config import get_chain, get_wallet_source, get_private_key


def _get_client():
    """Get a client using any available wallet (Solana or Base)."""
    from blockrun_llm.solana_wallet import load_solana_wallet
    from blockrun_llm.wallet import load_wallet

    # Try Solana first (cheaper), then Base
    sol_key = load_solana_wallet()
    if sol_key:
        from blockrun_llm import SolanaLLMClient
        client = SolanaLLMClient(private_key=sol_key)
        chain = "solana"
    else:
        base_key = load_wallet()
        if not base_key:
            print("  Error: No wallet found.")
            print("  Place wallet.json or solana-wallet.json in any ~/.<provider>/ folder.")
            sys.exit(1)
        from blockrun_llm import LLMClient
        client = LLMClient(private_key=base_key)
        chain = "base"

    addr = client.get_wallet_address()
    print(f"  Wallet: {addr[:6]}...{addr[-4:]} ({chain})")
    print(f"  Balance: ${client.get_balance():.2f}")
    return client


DATA_DIR = os.path.expanduser("~/.blockrun/data")


def _save_local(endpoint: str, body: dict, result: dict):
    """Save every paid API response locally — you paid for it, keep it."""
    from datetime import datetime

    os.makedirs(DATA_DIR, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Clean endpoint for filename: /v1/x/trending → x_trending
    slug = endpoint.strip("/").replace("v1/x/", "").replace("v1/", "").replace("/", "_")

    # Add context from body (username, query, etc.)
    ctx = body.get("username") or body.get("query") or body.get("handle") or ""
    ctx = ctx.replace(" ", "-").replace("@", "")[:30]
    if ctx:
        slug = f"{slug}_{ctx}"

    filename = f"{ts}_{slug}.json"
    filepath = os.path.join(DATA_DIR, filename)

    with open(filepath, "w") as f:
        json.dump({"endpoint": endpoint, "request": body, "response": result,
                    "timestamp": ts}, f, indent=2, ensure_ascii=False)

    return filepath


def _api(client, endpoint: str, body: dict) -> Dict[str, Any]:
    """Make a paid API call with retry on 502. Saves result locally."""
    try:
        result = client._request_with_payment_raw(endpoint, body)
    except Exception as e:
        if "502" in str(e):
            import time
            time.sleep(2)
            result = client._request_with_payment_raw(endpoint, body)
        else:
            raise

    # Save locally — you paid for this data
    _save_local(endpoint, body, result)
    return result


def _tweet_link(tw: dict) -> str:
    """Get direct link to a tweet. Always show links — user needs to find the tweet."""
    tid = tw.get("id", "")
    author = tw.get("author", {})
    handle = author.get("userName", "")
    if tid and handle:
        return f"https://x.com/{handle}/status/{tid}"
    elif tid:
        return f"https://x.com/i/status/{tid}"
    return ""


def _print_tweet(tw: dict, indent: str = "    ", max_text: int = 100):
    """Print a tweet with author, engagement, text, and link."""
    author = tw.get("author", {})
    handle = author.get("userName", "?")
    text = tw.get("text", "")[:max_text].replace("\n", " ")
    likes = tw.get("likeCount", 0)
    rts = tw.get("retweetCount", 0)
    link = _tweet_link(tw)
    print(f"{indent}@{handle:<16} {likes:>3} likes  {rts:>3} RTs  {text}")
    if link:
        print(f"{indent}  {link}")


# ── Workflow 1: Insight Report ──────────────────────────────────

def insight(username: str):
    """Deep-dive analysis of an X/Twitter account."""
    username = username.lstrip("@")
    client = _get_client()

    print(f"\n{'=' * 60}")
    print(f"  SOCIALCLAW INSIGHT — @{username}")
    print(f"{'=' * 60}")

    # 1. Profile
    print("\n  Fetching profile...")
    info = _api(client, "/v1/x/users/info", {"username": username})
    d = info.get("data", {})

    followers = d.get("followers") or d.get("followersCount") or 0
    following = d.get("following") or d.get("followingCount") or 0
    tweets = d.get("statusesCount") or d.get("tweetsCount") or 0
    verified = d.get("isBlueVerified", False)
    bio = d.get("description") or d.get("bio") or ""
    name = d.get("name") or username
    created = d.get("createdAt") or d.get("created_at") or ""

    print(f"\n  PROFILE")
    print(f"  {'Name:':<14} {name}")
    print(f"  {'Bio:':<14} {bio[:120]}")
    print(f"  {'Followers:':<14} {followers:,}")
    print(f"  {'Following:':<14} {following:,}")
    print(f"  {'Tweets:':<14} {tweets:,}")
    print(f"  {'Verified:':<14} {'Yes' if verified else 'No'}")
    if followers and following:
        ratio = followers / max(following, 1)
        print(f"  {'F/F Ratio:':<14} {ratio:.1f}x")

    # 2. Mentions — who's talking about them
    print("\n  Fetching mentions...")
    mentions = _api(client, "/v1/x/users/mentions", {"username": username})
    mention_tweets = mentions.get("tweets", [])

    print(f"\n  MENTIONS ({mentions.get('total_returned', 0)} recent)")
    for tw in mention_tweets[:5]:
        _print_tweet(tw)

    # 3. Followers — top by influence
    print("\n  Fetching followers...")
    fdata = _api(client, "/v1/x/users/followers", {"username": username})
    follower_list = fdata.get("followers", [])

    top_followers = sorted(
        follower_list, key=lambda x: x.get("followers_count", 0), reverse=True
    )[:10]

    print(f"\n  TOP FOLLOWERS (by their follower count)")
    for f in top_followers:
        v = "✓" if f.get("isBlueVerified") else " "
        fname = f.get("userName", "?")
        fc = f.get("followers_count", 0)
        print(f"    {v} @{fname:<22} {fc:>10,} followers")

    # 4. Engagement analysis
    if mention_tweets:
        total_likes = sum(tw.get("likeCount", 0) for tw in mention_tweets)
        total_rts = sum(tw.get("retweetCount", 0) for tw in mention_tweets)
        avg_likes = total_likes / len(mention_tweets)
        avg_rts = total_rts / len(mention_tweets)
        print(f"\n  MENTION ENGAGEMENT (last {len(mention_tweets)} mentions)")
        print(f"    Avg likes per mention:    {avg_likes:.1f}")
        print(f"    Avg retweets per mention: {avg_rts:.1f}")
        print(f"    Total reach (likes+RTs):  {total_likes + total_rts:,}")

    s = client.get_spending()
    print(f"\n{'=' * 60}")
    print(f"  Cost: ${s['total_usd']:.4f} ({s['calls']} calls)")
    print(f"{'=' * 60}")
    client.close()


# ── Workflow 2: Topic Radar ─────────────────────────────────────

def radar(topic: str):
    """What's hot on X/Twitter around a topic."""
    client = _get_client()

    print(f"\n{'=' * 60}")
    print(f"  SOCIALCLAW RADAR — \"{topic}\"")
    print(f"{'=' * 60}")

    # 1. Trending
    print("\n  Fetching trending topics...")
    trending = _api(client, "/v1/x/trending", {})
    topics = trending.get("data", {}).get("topics", [])

    print(f"\n  TRENDING NOW (top 10)")
    for t in topics[:10]:
        name = t.get("name", "?")
        articles = t.get("articleCount", 0)
        views = t.get("totalViews", 0)
        # Highlight if matches topic
        match = " <--" if topic.lower() in name.lower() else ""
        print(f"    {name:<28} {articles:>4} articles  {views:>12,} views{match}")

    # 2. Search latest
    print(f"\n  Searching \"{topic}\"...")
    search = _api(client, "/v1/x/search", {"query": topic, "queryType": "Latest"})
    search_tweets = search.get("tweets", [])

    print(f"\n  LATEST TWEETS ({len(search_tweets)} found)")
    for tw in search_tweets[:8]:
        _print_tweet(tw, max_text=110)

    # 3. Top tweets (may not be available on all endpoints)
    top_tweets = []
    try:
        print(f"\n  Searching top tweets...")
        top = _api(client, "/v1/x/search", {"query": topic, "queryType": "Top"})
        top_tweets = top.get("tweets", [])
    except Exception:
        print("    (Top search unavailable, skipping)")

    if top_tweets:
        print(f"\n  TOP PERFORMING TWEETS ({len(top_tweets)})")
        for tw in top_tweets[:5]:
            author = tw.get("author", {})
            a_followers = author.get("followers", author.get("followersCount", 0))
            handle = author.get("userName", "?")
            print(f"    @{handle} ({a_followers:,} followers)")
            _print_tweet(tw, indent="      ", max_text=110)
            print()

    # 4. Rising articles
    print("  Fetching rising articles...")
    rising = _api(client, "/v1/x/articles/rising", {})
    articles = rising.get("data", {}).get("articles", [])

    # Filter relevant ones
    relevant = [a for a in articles if topic.lower() in json.dumps(a).lower()]
    show_articles = relevant[:5] if relevant else articles[:5]

    print(f"\n  RISING ARTICLES {'(topic-related)' if relevant else '(general)'}")
    for a in show_articles:
        title = a.get("title", "?")[:70]
        url = a.get("url", "")
        score = a.get("score", "?")
        print(f"    [{score}] {title}")
        if url:
            print(f"         {url[:80]}")

    # Summary
    if search_tweets:
        total_likes = sum(tw.get("likeCount", 0) for tw in search_tweets)
        total_rts = sum(tw.get("retweetCount", 0) for tw in search_tweets)
        print(f"\n  TOPIC PULSE")
        print(f"    Total engagement (latest {len(search_tweets)} tweets): {total_likes + total_rts:,}")
        print(f"    Avg likes per tweet: {total_likes / len(search_tweets):.1f}")

    s = client.get_spending()
    print(f"\n{'=' * 60}")
    print(f"  Cost: ${s['total_usd']:.4f} ({s['calls']} calls)")
    print(f"{'=' * 60}")
    client.close()


# ── Workflow 3: Competitor Compare ──────────────────────────────

def compare(user1: str, user2: str):
    """Side-by-side comparison of two X accounts."""
    user1 = user1.lstrip("@")
    user2 = user2.lstrip("@")
    client = _get_client()

    print(f"\n{'=' * 60}")
    print(f"  SOCIALCLAW COMPARE — @{user1} vs @{user2}")
    print(f"{'=' * 60}")

    # Fetch both profiles
    print("\n  Fetching profiles...")
    info1 = _api(client, "/v1/x/users/info", {"username": user1}).get("data", {})
    info2 = _api(client, "/v1/x/users/info", {"username": user2}).get("data", {})

    def _get(d, *keys):
        for k in keys:
            if d.get(k):
                return d[k]
        return 0

    f1 = _get(info1, "followersCount", "followers")
    f2 = _get(info2, "followersCount", "followers")
    fw1 = _get(info1, "followingCount", "following")
    fw2 = _get(info2, "followingCount", "following")
    t1 = _get(info1, "statusesCount", "tweetsCount")
    t2 = _get(info2, "statusesCount", "tweetsCount")

    print(f"\n  {'METRIC':<20} {'@' + user1:>18} {'@' + user2:>18}")
    print(f"  {'-' * 56}")
    print(f"  {'Followers':<20} {f1:>18,} {f2:>18,}")
    print(f"  {'Following':<20} {fw1:>18,} {fw2:>18,}")
    print(f"  {'Tweets':<20} {t1:>18,} {t2:>18,}")

    v1 = "Yes" if info1.get("isBlueVerified") else "No"
    v2 = "Yes" if info2.get("isBlueVerified") else "No"
    print(f"  {'Verified':<20} {v1:>18} {v2:>18}")

    r1 = f1 / max(fw1, 1)
    r2 = f2 / max(fw2, 1)
    print(f"  {'F/F Ratio':<20} {r1:>17.1f}x {r2:>17.1f}x")

    # Mentions for both
    print("\n  Fetching mentions...")
    m1 = _api(client, "/v1/x/users/mentions", {"username": user1}).get("tweets", [])
    m2 = _api(client, "/v1/x/users/mentions", {"username": user2}).get("tweets", [])

    ml1 = sum(tw.get("likeCount", 0) for tw in m1)
    ml2 = sum(tw.get("likeCount", 0) for tw in m2)
    mr1 = sum(tw.get("retweetCount", 0) for tw in m1)
    mr2 = sum(tw.get("retweetCount", 0) for tw in m2)

    print(f"\n  {'MENTIONS':<20} {'@' + user1:>18} {'@' + user2:>18}")
    print(f"  {'-' * 56}")
    print(f"  {'Recent mentions':<20} {len(m1):>18} {len(m2):>18}")
    print(f"  {'Total likes':<20} {ml1:>18,} {ml2:>18,}")
    print(f"  {'Total RTs':<20} {mr1:>18,} {mr2:>18,}")
    if m1:
        print(f"  {'Avg likes/mention':<20} {ml1/len(m1):>17.1f} ", end="")
    else:
        print(f"  {'Avg likes/mention':<20} {'—':>18} ", end="")
    if m2:
        print(f"{ml2/len(m2):>17.1f}")
    else:
        print(f"{'—':>18}")

    # Top followers comparison
    print("\n  Fetching followers...")
    fl1 = _api(client, "/v1/x/users/followers", {"username": user1}).get("followers", [])
    fl2 = _api(client, "/v1/x/users/followers", {"username": user2}).get("followers", [])

    top1 = sorted(fl1, key=lambda x: x.get("followers_count", 0), reverse=True)[:3]
    top2 = sorted(fl2, key=lambda x: x.get("followers_count", 0), reverse=True)[:3]

    print(f"\n  TOP FOLLOWERS")
    print(f"  @{user1}:")
    for f in top1:
        print(f"    @{f.get('userName', '?'):<20} {f.get('followers_count', 0):>10,}")
    print(f"  @{user2}:")
    for f in top2:
        print(f"    @{f.get('userName', '?'):<20} {f.get('followers_count', 0):>10,}")

    # Verdict
    print(f"\n  QUICK TAKE")
    if f1 > f2:
        print(f"    @{user1} has {f1/max(f2,1):.1f}x more followers")
    else:
        print(f"    @{user2} has {f2/max(f1,1):.1f}x more followers")

    if ml1 + mr1 > ml2 + mr2:
        print(f"    @{user1} gets more mention engagement ({ml1+mr1:,} vs {ml2+mr2:,})")
    else:
        print(f"    @{user2} gets more mention engagement ({ml2+mr2:,} vs {ml1+mr1:,})")

    s = client.get_spending()
    print(f"\n{'=' * 60}")
    print(f"  Cost: ${s['total_usd']:.4f} ({s['calls']} calls)")
    print(f"{'=' * 60}")
    client.close()


# ── CLI ─────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("SocialClaw — X/Twitter Marketing Intelligence")
        print()
        print("Usage:")
        print("  socialclaw insight @username     Account deep-dive")
        print("  socialclaw radar <topic>         Topic trends + opportunities")
        print("  socialclaw compare @a @b         Side-by-side comparison")
        return

    cmd = sys.argv[1].lower()

    if cmd == "insight" and len(sys.argv) >= 3:
        insight(sys.argv[2])
    elif cmd == "radar" and len(sys.argv) >= 3:
        radar(" ".join(sys.argv[2:]))
    elif cmd == "compare" and len(sys.argv) >= 4:
        compare(sys.argv[2], sys.argv[3])
    else:
        print(f"Unknown: {cmd}. Try: insight, radar, compare")


if __name__ == "__main__":
    main()
