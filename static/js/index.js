dismissers = document.querySelectorAll(".dismisser");
dismissers.forEach(dismisser => {
    dismisser.addEventListener("click", function (event) {
        dismisser.parentElement.style.display = "none";
    })
})