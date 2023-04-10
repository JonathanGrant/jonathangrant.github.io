import os
import re
from bs4 import BeautifulSoup

posts_dir = "posts/"
index_file = "index.html"
search_js_file = "js/search.js"

# Extract title and summary from the post file
def extract_post_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file.read(), "html.parser")
        title = soup.title.string.replace(" - My Blog", "") if soup.title else ""
        summary = soup.article.p.string if soup.article and soup.article.p else ""
        return title, summary

# Update index.html
def update_index_html(post_data):
    with open(index_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file.read(), "html.parser")
        main_tag = soup.main
        main_tag.clear()

        for post in post_data:
            article_tag = soup.new_tag("article")
            h2_tag = soup.new_tag("h2")
            a_tag = soup.new_tag("a", href=f"posts/{post['file']}")
            a_tag.string = post["title"]
            h2_tag.append(a_tag)
            article_tag.append(h2_tag)

            p_tag = soup.new_tag("p")
            p_tag.string = post["summary"]
            article_tag.append(p_tag)

            main_tag.append(article_tag)

    with open(index_file, "w", encoding="utf-8") as file:
        file.write(str(soup))

# Update search.js
def update_search_js(post_data):
    with open(search_js_file, "r", encoding="utf-8") as file:
        content = file.read()
        search_data_re = r"const postData = \[(.*?)\];"
        search_data = re.search(search_data_re, content, re.DOTALL).group(1)

        new_data = []
        for post in post_data:
            new_data.append(f"""{{
                id: {post['id']},
                title: "{post['title']}",
                content: "{post['summary']}",
                href: "posts/{post['file']}"
            }}""")

        new_data_str = ",\n        ".join(new_data)
        content = re.sub(search_data_re, f"const postData = [\n        {new_data_str}\n    ];", content)

    with open(search_js_file, "w", encoding="utf-8") as file:
        file.write(content)

# Main function
def main():
    post_data = []

    for i, file in enumerate(sorted(os.listdir(posts_dir))):
        if file.endswith(".html"):
            title, summary = extract_post_data(f"{posts_dir}{file}")
            post_data.append({
                "id": i + 1,
                "file": file,
                "title": title,
                "summary": summary
            })

    update_index_html(post_data)
    update_search_js(post_data)

if __name__ == "__main__":
    main()
