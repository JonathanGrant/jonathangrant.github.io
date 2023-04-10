document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search-input");
    const searchResults = document.getElementById("search-results");

    let postData = [];
    let idx;

    const postFiles = [
        "posts/post-1.html",
        "posts/post-2.html"
    ];

    // Fetch the content of a post file
    async function fetchPostContent(postFile) {
        const response = await fetch(postFile);
        const content = await response.text();
        return content;
    }

    // Initialize the search index
    async function initSearchIndex() {
        const postContents = await Promise.all(postFiles.map(fetchPostContent));

        postData = postContents.map((content, index) => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(content, "text/html");
            const title = doc.title.replace(" - My Blog", "");
            const href = postFiles[index];
            return {
                id: index + 1,
                title: title,
                content: content,
                href: href
            };
        });

        idx = lunr(function () {
            this.ref("id");
            this.field("title");
            this.field("content", { boost: 2 });

            postData.forEach(function (doc) {
                this.add(doc);
            }, this);
        });
    }

    // Add the input event listener for search functionality
    function addSearchEventListener() {
        searchInput.addEventListener("input", function () {
            const query = searchInput.value.trim();
            const results = idx.search(query);

            searchResults.innerHTML = "";

            if (results.length === 0) {
                searchResults.innerHTML = "<li>No results found</li>";
            } else {
                results.forEach(function (result) {
                    const post = postData.find((post) => post.id === parseInt(result.ref));
                    const listItem = document.createElement("li");
                    const link = document.createElement("a");
                    link.textContent = post.title;
                    link.href = post.href;
                    listItem.appendChild(link);
                    searchResults.appendChild(listItem);
                });
            }
        });
    }

    // Initialize the search index and add the event listener
    initSearchIndex().then(() => {
        addSearchEventListener();
    });
});
