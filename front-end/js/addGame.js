window.onload = function () {
    // Form inputs
    const TITLE_INPUT = document.getElementById("title");
    const PUBLISHER_INPUT = document.getElementById("publisher");
    const YEAR_INPUT = document.getElementById("year");
    const INVENTORY_INPUT = document.getElementById("inventory");
    const GENRE_INPUT = document.getElementById("genre");
    const SUBMIT_BUTTON = document.getElementById("add-game-button");

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
    
        if (!TITLE_INPUT.value.trim() ||
            !PUBLISHER_INPUT.value.trim() ||
            !YEAR_INPUT.value.trim() ||
            !INVENTORY_INPUT.value.trim() ||
            !GENRE_INPUT.value.trim()) {
            showEmptyFieldsMessage();
            return;
        }
    
        // Reset the modal state if fields are filled
        resetModalState();
    
        // Populate modal with entered details
        MODAL_BODY.innerHTML = `
            <p>Please confirm the following details for the new game:</p>
            <ul>
                <li>Title: ${TITLE_INPUT.value.trim()}</li>
                <li>Publisher: ${PUBLISHER_INPUT.value.trim()}</li>
                <li>Year: ${YEAR_INPUT.value.trim()}</li>
                <li>Inventory: ${INVENTORY_INPUT.value.trim()}</li>
                <li>Genre: ${GENRE_INPUT.value.trim()}</li>
            </ul>
        `;
        MODAL.style.display = "block";
    
        MODAL_CONFIRM_BUTTON.addEventListener("click", submitDryRun);
        MODAL_CANCEL_BUTTON.addEventListener("click", closeModal);
    }
    

    function submitDryRun() {
        const formData = {
            Title: TITLE_INPUT.value.trim(),
            Publisher: PUBLISHER_INPUT.value.trim(),
            Year: YEAR_INPUT.value.trim(),
            Inventory: INVENTORY_INPUT.value.trim(),
            Genre: GENRE_INPUT.value.trim()
        };

        postRequestParams("add_game", formData, handleDryRunResponse, handleError);
    }

    function handleDryRunResponse(data) {
        if (data.message === "Please confirm the details") {
            console.log("Dry run successful:", data);
            submitFinalConfirmation();
        } else {
            handleError(data);
        }
    }
    
    function submitFinalConfirmation() {
        const params = {
            Confirm: "confirmed",
            Title: TITLE_INPUT.value.trim(),
            Publisher: PUBLISHER_INPUT.value.trim(),
            Year: YEAR_INPUT.value.trim(),
            Inventory: INVENTORY_INPUT.value.trim(),
            Genre: GENRE_INPUT.value.trim()
        };
    
        postRequestParams("add_game", params, handleConfirmResponse, handleError);
        closeModal(); // Close the modal after initiating the request
    }



    function handleConfirmResponse(data) {
        if (data["Registration Added"]) {
            const game = data["Registration Added"][0];
            SUCCESS_MESSAGE.innerHTML = `
                <p>Video Game successfully added!</p>
            `;
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
        // Update modal content
        MODAL_BODY.innerHTML = `
            <p style="color: red;">Please fill in all required fields before submitting.</p>
        `;
    
        // Change modal header
        MODAL.querySelector(".modal-header").textContent = "Field Error";
    
        // Hide the cancel button
        MODAL_CANCEL_BUTTON.style.display = "none";
    
        // Change the confirm button to "Go Back"
        MODAL_CONFIRM_BUTTON.textContent = "Go Back";
        MODAL_CONFIRM_BUTTON.replaceWith(MODAL_CONFIRM_BUTTON.cloneNode(true)); // Reset listeners
        const NEW_CONFIRM_BUTTON = document.querySelector("#custom-modal .confirm-button");
        NEW_CONFIRM_BUTTON.addEventListener("click", closeModal);
        
        // Display the modal
        MODAL.style.display = "block";
    }

    function resetModalState() {
        // Reset modal header
        MODAL.querySelector(".modal-header").textContent = "Confirm New Game";
    
        // Show the cancel button
        MODAL_CANCEL_BUTTON.style.display = "block";
    
        // Reset confirm button text and re-bind the correct event listener
        MODAL_CONFIRM_BUTTON.textContent = "Confirm";
        MODAL_CONFIRM_BUTTON.replaceWith(MODAL_CONFIRM_BUTTON.cloneNode(true)); // Reset listeners
        const NEW_CONFIRM_BUTTON = document.querySelector("#custom-modal .confirm-button");
        NEW_CONFIRM_BUTTON.addEventListener("click", submitDryRun);
    }
    
    
    

    function handleError(error) {
        alert(`Error: ${error.error || "Unknown error occurred"}`);
    }

    CLOSE_SUCCESS_MODAL.addEventListener("click", () => {
        SUCCESS_MODAL.style.display = "none";
    });

    window.addEventListener("click", (event) => {
        if (event.target === MODAL) closeModal();
        if (event.target === SUCCESS_MODAL) SUCCESS_MODAL.style.display = "none";
    });
};
