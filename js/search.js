document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search-input");
    const searchResults = document.getElementById("search-results");

    const postData = [
        {
            id: 1,
            title: "Post 1",
            content: "Post 1 content...",
            href: "posts/post-1.html"
        },
        {
            id: 2,
            title: "Post 2",
            content: "Post 2 content...",
            href: "posts/post-2.html"
        }
    ];

    const idx = lunr(function () {
        this.ref("id");
        this.field("title");
        this.field("content");

        postData.forEach(function (doc) {
            this.add(doc);
        }, this);
    });

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
});
