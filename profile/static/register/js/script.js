        function saveForm(event) {
            event.preventDefault();
            document.getElementById("submitButton").click();
        }
        document.getElementById("commit-register").addEventListener("click", saveForm);
