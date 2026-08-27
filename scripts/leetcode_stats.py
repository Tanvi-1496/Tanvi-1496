import sys
import requests

username = "Tanvi_1496"

query = """
query getUserProfile($username: String!) {
    matchedUser(username: $username) {
        submitStatsGlobal {
            acSubmissionNum {
                difficulty
                count
            }
        }
    }
}
"""

url = "https://leetcode.com/graphql"

# LeetCode's GraphQL endpoint is behind Cloudflare and will silently
# reject/challenge requests that don't look like they come from a browser.
# Requests without these headers often get a non-JSON (HTML) response back,
# or a JSON body where "matchedUser" is null - this is the #1 reason the
# stats end up staying at 0.
headers = {
    "Content-Type": "application/json",
    "Referer": f"https://leetcode.com/{username}/",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
}

response = requests.post(
    url,
    json={"query": query, "variables": {"username": username}},
    headers=headers,
    timeout=15,
)

# Fail LOUDLY instead of silently. If something is wrong, we want the
# GitHub Actions run to show a red X with a clear reason in the logs,
# not quietly leave README.md untouched.
if response.status_code != 200:
    print(f"❌ LeetCode API returned HTTP {response.status_code}")
    print(response.text[:500])
    sys.exit(1)

try:
    data = response.json()
except ValueError:
    print("❌ LeetCode did not return valid JSON (likely blocked by Cloudflare).")
    print(response.text[:500])
    sys.exit(1)

matched_user = data.get("data", {}).get("matchedUser")

if matched_user is None:
    print("❌ 'matchedUser' was null. Check that the username is correct "
          f"({username}) and that the LeetCode profile is public.")
    print(data)
    sys.exit(1)

stats = matched_user["submitStatsGlobal"]["acSubmissionNum"]

easy = medium = hard = total = 0

for item in stats:
    if item["difficulty"] == "Easy":
        easy = item["count"]
    elif item["difficulty"] == "Medium":
        medium = item["count"]
    elif item["difficulty"] == "Hard":
        hard = item["count"]
    elif item["difficulty"] == "All":
        total = item["count"]

# Sanity check: if everything came back 0 even though the request
# "succeeded", don't overwrite the README with a bad value - fail instead
# so the workflow log flags it clearly.
if total == 0 and easy == 0 and medium == 0 and hard == 0:
    print("⚠️ All values came back 0 - this looks wrong, not writing README.")
    sys.exit(1)

leetcode_section = f"""
<div align="center">

## 🧩 LeetCode Statistics

<table>
<tr>
<td align="center">

🔥 <b>Total Solved</b><br>
<h2>{total}</h2>

</td>

<td align="center">

🟢 <b>Easy</b><br>
<h2>{easy}</h2>

</td>

<td align="center">

🟡 <b>Medium</b><br>
<h2>{medium}</h2>

</td>

<td align="center">

🔴 <b>Hard</b><br>
<h2>{hard}</h2>

</td>

</tr>
</table>

</div>
"""

readme_path = "README.md"

with open(readme_path, "r", encoding="utf-8") as file:
    readme = file.read()

start = "<!-- LEETCODE_STATS_START -->"
end = "<!-- LEETCODE_STATS_END -->"

if start not in readme or end not in readme:
    print("❌ Could not find LEETCODE_STATS_START/END markers in README.md. "
          "Did the README get edited manually and the markers removed?")
    sys.exit(1)

updated_readme = (
    readme.split(start)[0]
    + start
    + "\n\n"
    + leetcode_section
    + "\n"
    + end
    + readme.split(end)[1]
)

with open(readme_path, "w", encoding="utf-8") as file:
    file.write(updated_readme)

print(f"✅ README updated successfully: Total={total}, Easy={easy}, Medium={medium}, Hard={hard}")