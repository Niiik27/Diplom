        function saveForm(event) {
            event.preventDefault();
            document.getElementById("submitButton").click();
        }
        document.getElementById("saveLink").addEventListener("click", saveForm);
