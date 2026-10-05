// -------------------------
// DARK MODE
// -------------------------

const darkModeBtn = document.getElementById("darkModeBtn");

if (darkModeBtn) {

    darkModeBtn.addEventListener("click", function () {

        document.body.classList.toggle("dark-mode");

        if (document.body.classList.contains("dark-mode")) {

            darkModeBtn.textContent = "Light Mode";

        } else {

            darkModeBtn.textContent = "Dark Mode";

        }

    });

}


// -------------------------
// CONTACT FORM
// -------------------------

const contactForm = document.getElementById("contactForm");

if (contactForm) {

    contactForm.addEventListener("submit", function (event) {

        event.preventDefault();

        const name = document.getElementById("name").value;

        const formMessage =
            document.getElementById("formMessage");

        formMessage.innerHTML = `
            <div class="alert alert-success">
                Thanks, ${name}! Your message has been sent.
            </div>
        `;

        contactForm.reset();

    });

}
