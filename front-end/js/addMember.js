window.onload = function () {
    const FIRST_NAME_INPUT = document.getElementById("first-name");
    const LAST_NAME_INPUT = document.getElementById("last-name");
    const PHONE_NUMBER_INPUT = document.getElementById("phone-number");
    const EMAIL_INPUT = document.getElementById("email");
    const SUBMIT_BUTTON = document.getElementById("add-member-button");
    const RESPONSE = document.getElementById("response-message");

    // Modal elements
    const MODAL = document.getElementById("custom-modal");
    const MODAL_BODY = document.querySelector("#custom-modal .modal-body");
    const MODAL_CONFIRM_BUTTON = document.querySelector("#custom-modal .confirm-button");
    const MODAL_CANCEL_BUTTON = document.querySelector("#custom-modal .cancel-button");
    const SUCCESS_MODAL = document.getElementById("success-modal");
    const SUCCESS_MESSAGE = document.getElementById("success-message");
    const CLOSE_SUCCESS_MODAL = document.getElementById("close-success-modal");

    if (SUBMIT_BUTTON) {
        SUBMIT_BUTTON.addEventListener("click", validateAndOpenModal);
    } else {
        console.error("Submit button not found");
    }

    function validateAndOpenModal(event) {
        event.preventDefault(); // Prevent form submission

        if (!FIRST_NAME_INPUT.value.trim() ||
            !LAST_NAME_INPUT.value.trim() ||
            !PHONE_NUMBER_INPUT.value.trim() ||
            !EMAIL_INPUT.value.trim()) {
            showEmptyFieldsMessage();
            return;
        }

        // Populate modal with entered details
        MODAL_BODY.innerHTML = `
            <p>Please confirm the following details for the new member:</p>
            <ul>
                <li>First Name: ${FIRST_NAME_INPUT.value.trim()}</li>
                <li>Last Name: ${LAST_NAME_INPUT.value.trim()}</li>
                <li>Phone Number: ${PHONE_NUMBER_INPUT.value.trim()}</li>
                <li>Email: ${EMAIL_INPUT.value.trim()}</li>
            </ul>
        `;
        MODAL.style.display = "block";

        MODAL_CONFIRM_BUTTON.replaceWith(MODAL_CONFIRM_BUTTON.cloneNode(true)); // Reset listeners
        document.querySelector("#custom-modal .confirm-button").addEventListener("click", submitForm);

        MODAL_CANCEL_BUTTON.replaceWith(MODAL_CANCEL_BUTTON.cloneNode(true)); // Reset listeners
        document.querySelector("#custom-modal .cancel-button").addEventListener("click", closeModal);
    }

    function submitForm() {
        let formData = {
            FirstName: FIRST_NAME_INPUT.value.trim(),
            LastName: LAST_NAME_INPUT.value.trim(),
            PhoneNumber: PHONE_NUMBER_INPUT.value.trim(),
            Email: EMAIL_INPUT.value.trim(),
            Confirm: "confirmed"
        };

        postRequestParams("add_member", formData, handleResponse, handleError);
        closeModal();
    }

    function handleResponse(data) {
        if (data["Registration Added"]) {
            SUCCESS_MODAL.style.display = "block";
        } else {
            handleError(data);
        }
    }

    function closeModal() {
        MODAL.style.display = "none";
        MODAL_BODY.innerHTML = ""; // Clear modal content
    }

    function showEmptyFieldsMessage() {
        MODAL_BODY.innerHTML = `
            <p style="color: red;">Please fill in all required fields before submitting.</p>
        `;
        MODAL.style.display = "block";
    }

    function handleError(error) {
        RESPONSE.textContent = `Error: ${error.error || "Unknown error occurred"}`;
        RESPONSE.className = "error";
    }

    CLOSE_SUCCESS_MODAL.addEventListener("click", () => {
        SUCCESS_MODAL.style.display = "none";
    });

    window.addEventListener("click", (event) => {
        if (event.target === MODAL) closeModal();
        if (event.target === SUCCESS_MODAL) SUCCESS_MODAL.style.display = "none";
    });
};