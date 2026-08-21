document.addEventListener("DOMContentLoaded", () => {
    const loader = document.querySelector(".page-loader");

    const hideLoader = () => {
        if (!loader) return;

        loader.classList.add("hidden");
        document.body.classList.remove("page-loading");
    };

    // Hide when the page is fully loaded
    window.addEventListener("load", hideLoader);

    // Fallback in case the load event is delayed
    setTimeout(hideLoader, 1500);

});

    // Smooth page transitions
    document.querySelectorAll("a").forEach((link) => {
        const href = link.getAttribute("href");

        if (
            href &&
            !href.startsWith("#") &&
            !href.startsWith("http") &&
            !link.hasAttribute("download")
        ) {
            link.addEventListener("click", (event) => {
                event.preventDefault();
                document.body.classList.add("page-exit");

                setTimeout(() => {
                    window.location.href = href;
                }, 250);
            });
        }
    });

    // Reveal elements while scrolling
    const revealItems = document.querySelectorAll(".card, .profile-head");

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.1 }
    );

    revealItems.forEach((item) => {
        item.classList.add("reveal");
        observer.observe(item);
    });

    // Button ripple effect
    document.querySelectorAll(".button").forEach((button) => {
        button.addEventListener("click", (event) => {
            const ripple = document.createElement("span");
            ripple.className = "ripple";

            const rect = button.getBoundingClientRect();
            ripple.style.left = `${event.clientX - rect.left}px`;
            ripple.style.top = `${event.clientY - rect.top}px`;

            button.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        });
    });

    // Show loading text when submitting forms
    document.querySelectorAll("form").forEach((form) => {
        form.addEventListener("submit", () => {
            const submitButton = form.querySelector("[type='submit']");

            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = "Please wait...";
            }
        });
    });