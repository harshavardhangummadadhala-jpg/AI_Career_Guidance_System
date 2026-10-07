document.addEventListener("DOMContentLoaded", function () {
    const selects = document.querySelectorAll("select");
    selects.forEach(select => {
        select.addEventListener("change", function () {
            if (this.value) this.style.borderColor = "#5547f5";
        });
    });
});
