document.addEventListener("DOMContentLoaded", () => {
    // Theme Toggle
    const themeToggle = document.getElementById("theme-toggle");
    if (themeToggle) {
        themeToggle.addEventListener("click", () => {
            if (document.body.classList.contains('dark')) {
                document.body.classList.remove('dark');
                localStorage.setItem("pref-theme", 'light');
            } else {
                document.body.classList.add('dark');
                localStorage.setItem("pref-theme", 'dark');
            }
        });
    }

    // Go to Top link
    const topLink = document.getElementById("top-link");
    if (topLink) {
        window.onscroll = function () {
            if (document.body.scrollTop > 800 || document.documentElement.scrollTop > 800) {
                topLink.style.visibility = "visible";
                topLink.style.opacity = "1";
            } else {
                topLink.style.visibility = "hidden";
                topLink.style.opacity = "0";
            }
        };
    }
});
