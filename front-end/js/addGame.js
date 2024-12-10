window.onload = function () {
    // Form inputs
    const TITLE_INPUT = document.getElementById('title');
    const PUBLISHER_INPUT = document.getElementById('publisher');
    const YEAR_INPUT = document.getElementById('year');
    const INVENTORY_INPUT = document.getElementById('inventory');
    const GENRE_INPUT = document.getElementById('genre');
    const SUBMIT_BUTTON = document.getElementById('add-game-button');

    // Modals
    const MODAL = document.getElementById('custom-modal');
    const MODAL_BODY = document.querySelector("#custom-modal .modal-body");
    const MODAL_CONFIRM_BUTTON = document.querySelector("#custom-modal .confirm-button");
    const MODAL_CANCEL_BUTTON = document.querySelector("#custom-modal .cancel-button");
    const SUCCESS_MODAL = document.getElementById('success-modal');
    const SUCCESS_MESSAGE = document.getElementById('success-message');
    const CLOSE_SUCCESS_MODAL = document.getElementById('close-success-modal');

    // Add event listener to submit button
    if (SUBMIT_BUTTON) {
        SUBMIT_BUTTON.addEventListener('click', validateAndOpenModal);
    } else {
        console.error('Submit button not found.');
    }

    function validateAndOpenModal(event) {
        event.preventDefault(); // Prevent form submission
        MODAL.querySelector('.modal-header').textContent = 'Confirm Game'; // Reset header
        if (!TITLE_INPUT.value.trim() ||
            !PUBLISHER_INPUT.value.trim() ||
            !YEAR_INPUT.value.trim() ||
            !INVENTORY_INPUT.value.trim() ||
            !GENRE_INPUT.value.trim()) {
            showEmptyFieldsMessage();
            MODAL.style.display = 'block';
            return;
        }

        // Populate the modal with details
        const ENTERED_DETAILS = `
            <p>Please confirm the following details for the new game:</p>
            <ul>
                <li>Title: ${TITLE_INPUT.value.trim() || "[Not Provided]"}</li>
                <li>Publisher: ${PUBLISHER_INPUT.value.trim() || "[Not Provided]"}</li>
                <li>Year: ${YEAR_INPUT.value.trim() || "[Not Provided]"}</li>
                <li>Inventory: ${INVENTORY_INPUT.value.trim() || "[Not Provided]"}</li>
                <li>Genre: ${GENRE_INPUT.value.trim() || "[Not Provided]"}</li>
            </ul>
        `;

        MODAL_BODY.innerHTML = ENTERED_DETAILS;
        MODAL.style.display = 'block';

        MODAL_CONFIRM_BUTTON.addEventListener("click", submitForm);
        MODAL_CANCEL_BUTTON.addEventListener("click", closeModal);
        function closeModal() {
            MODAL.style.display = "none";
            MODAL_BODY.innerHTML = ""; //clear modal content
            MODAL_CONFIRM_BUTTON.removeEventListener("click", submitForm);//remove any old event listener
            MODAL_CONFIRM_BUTTON.removeEventListener("click", closeModal);//remove any old event listener
            MODAL_CONFIRM_BUTTON.textContent = "Confirm"; // reset button label
            MODAL_CANCEL_BUTTON.style.display = "block"; //reset cancel button
        }
    }

    function submitForm() {
        const NEW_GAME_DATA = {
            Title: TITLE_INPUT.value.trim(),
            Publisher: PUBLISHER_INPUT.value.trim(),
            Year: YEAR_INPUT.value.trim(),
            Inventory: INVENTORY_INPUT.value.trim(),
            Genre: GENRE_INPUT.value.trim(),
        };

        let params = {
            Confirm: "confirmed",
            Title: NEW_GAME_DATA.Title,
            Publisher: NEW_GAME_DATA.Publisher,
            Year: NEW_GAME_DATA.Year,
            Inventory: NEW_GAME_DATA.Inventory,
            Genre: NEW_GAME_DATA.Genre
        };

        // Send a POST request to the server
        postRequestParams('add_game', params, handleConfirmResponse, handleError);
        
        closeModal();//close the modal

        // Close the modal        
        function closeModal() {
            MODAL.style.display = 'none';    
            MODAL_BODY.innerHTML = "";  // Clear modal content  

        }
    }

    function handleError(data) {
        const errorMessage = data.error || "Unknown error occurred.";
        alert(`Error: ${errorMessage}`);
    }

    function closeModal() {
        MODAL.style.display = 'none';
        MODAL_BODY.innerHTML = ""; // Clear modal content
    }
    function showEmptyFieldsMessage() {
        MODAL_BODY.innerHTML = `
            <p>Please fill in all required fields before submitting.</p>
        `;
        MODAL.style.display = 'block';
        MODAL.querySelector(".modal-header").textContent = "Field Error";
        // hide cancel button
        MODAL_CANCEL_BUTTON.style.display = "none";
    }
        //change button labels to Go back
        MODAL_CONFIRM_BUTTON.textContent = "Go Back";
        MODAL_CONFIRM_BUTTON.removeEventListener("click", submitForm);
        MODAL_CONFIRM_BUTTON.addEventListener("click", closeModal); // remove any old event listener
        }
        MODAL.querySelector(".modal-header").textContent = "Confirm Game";

    function handleConfirmResponse(data) {
        if (data['Registration Added']) {
            SUCCESS_MESSAGE.innerHTML = `
                <p>Game successfully added:</p>
                <ul>
                    <li>Title: ${data['Registration Added'][0].Title}</li>
                    <li>Publisher: ${data['Registration Added'][0].Publisher}</li>
                    <li>Year: ${data['Registration Added'][0].Year}</li>
                    <li>Inventory: ${data['Registration Added'][0].Inventory}</li>
                    <li>Genre: ${data['Registration Added'][0].Genre}</li>
                </ul>
            `;
            SUCCESS_MODAL.style.display = 'block';
        } else {
            handleError(data);
        }
    }
    function successModal() {
        SUCCESS_MODAL.style.display = "block";
        SUCCESS_MESSAGE.textContent = "Video Game added successfully.";
    }
    // Event listener to close success modal
    CLOSE_SUCCESS_MODAL.onclick = () => {
        SUCCESS_MODAL.style.display = 'none';
    };

    // Close modals when clicking outside
    window.onclick = (event) => {
        if (event.target === MODAL) closeModal();
        if (event.target === SUCCESS_MODAL) SUCCESS_MODAL.style.display = 'none';
    };


