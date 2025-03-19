document.addEventListener("DOMContentLoaded", function () {
    const innField = document.querySelector("#id_inn");
    const formFields = document.querySelectorAll(".form-row:not(:has(#id_inn))");

    function hideFields() {
        formFields.forEach(field => field.style.display = "none");
    }

    function showFields() {
        formFields.forEach(field => field.style.display = "");
    }

    function clearFields() {
        document.querySelector("#id_name").value = "";
        document.querySelector("#id_pinfl").value = "";
        document.querySelector("#id_address").value = "";
        document.querySelector("#id_bank_name").value = "";
        document.querySelector("#id_phone").value = "";
        document.querySelector("#id_date_birth").value = "";
    }

    hideFields();

    function fetchCompanyInfo(inn) {
        fetch(`/api/get-company-info/${inn}/`)
            .then(response => {
                if (!response.ok) throw new Error("Ошибка сервера");
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    clearFields()
                    document.querySelector("#id_inn").value = data.CompanyInn || "";
                    document.querySelector("#id_name").value = data.CompanyName || "";
                    document.querySelector("#id_pinfl").value = data.Pinfl || "";
                    document.querySelector("#id_address").value = data.CompanyAddress || "";
                    document.querySelector("#id_phone").value = data.PhoneNumber || "";

                    const bankName = data.Accounts && data.Accounts.length > 0 ? data.Accounts[0].BankName : "";
                    document.querySelector("#id_bank_name").value = bankName;
                    if (data.BirthDate) {
                        document.querySelector("#id_date_birth").value = data.BirthDate;
                    }

                    formFields.forEach(field => field.style.display = "");
                } else {
                    alert(data.error);
                    hideFields();
                    clearFields();
                }
            })
            .catch(error => {
                console.error("Ошибка запроса:", error);
                alert("Ошибка при получении данных. Попробуйте снова.");
                hideFields();
                clearFields();
            });
    }

    innField.addEventListener("input", function () {
        const inn = innField.value.trim();

        if (inn.length === 9 || inn.length === 14) {
            fetchCompanyInfo(inn);
        } else {
            hideFields(); // Полностью очищено -> скрываем
        }
    });

    if (innField.value.trim().length > 0) {
        showFields();
    } else {
        hideFields();
    }
});