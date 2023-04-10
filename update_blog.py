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
            a_tag = soup.new_tag("a", href=f"{post['file']}")
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
def update_search_js(post_files):
    with open(search_js_file, "r", encoding="utf-8") as file:
        content = file.read()
        post_files_re = r"const postFiles = \[(.*?)\];"
        post_files_str = ',\n        '.join([f'"{file}"' for file in post_files])
        content = re.sub(post_files_re, f"const postFiles = [\n        {post_files_str}\n    ];", content)

    with open(search_js_file, "w", encoding="utf-8") as file:
        file.write(content)

# Main function
def main():
    post_data = []

    post_files = sorted([f"{posts_dir}{file}" for file in os.listdir(posts_dir) if file.endswith(".html")])

    for i, file in enumerate(post_files):
        title, summary = extract_post_data(file)
        post_data.append({
            "id": i + 1,
            "file": file,
            "title": title,
            "summary": summary
        })

    update_index_html(post_data)
    update_search_js(post_files)

if __name__ == "__main__":
    main()
