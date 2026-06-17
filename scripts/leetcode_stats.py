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


response = requests.post(
    url,
    json={
        "query": query,
        "variables": {
            "username": username
        }
    }
)


data = response.json()


stats = data["data"]["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"]


easy = 0
medium = 0
hard = 0
total = 0


for item in stats:
    if item["difficulty"] == "Easy":
        easy = item["count"]

    elif item["difficulty"] == "Medium":
        medium = item["count"]

    elif item["difficulty"] == "Hard":
        hard = item["count"]

    elif item["difficulty"] == "All":
        total = item["count"]

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


print("README updated successfully ✅")