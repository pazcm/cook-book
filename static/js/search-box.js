// hide when expanded
    document.querySelector(".search-field").addEventListener("focus", function() {
    let hidden = document.querySelectorAll(".search-icon");
        for (let i = 0; i < hidden.length; ++i) {
            hidden[i].style.display = "none";
        }
    });

// show when expanded
    document.querySelector(".search-field")
    .addEventListener("focusout", function() {
    let hidden = document.querySelectorAll(".search-icon");
        for (let i = 0; i < hidden.length; ++i) {
            hidden[i].style.display = "block";
        }
    });
