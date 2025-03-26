document.addEventListener("DOMContentLoaded", function () {
    let categoryField = document.querySelector("#id_category");
    let subcategoryField = document.querySelector("#id_sub_category");

    function updateSubcategories() {
        let categoryId = categoryField.value;
        fetch(`/core/get_subcategories/?category_id=${categoryId}`)
            .then(response => response.json())
            .then(data => {
                subcategoryField.innerHTML = "";
                data.forEach(subcategory => {
                    let option = document.createElement("option");
                    option.value = subcategory.id;
                    option.textContent = subcategory.name;
                    subcategoryField.appendChild(option);
                });
            });
    }

    categoryField.addEventListener("change", updateSubcategories);
});
