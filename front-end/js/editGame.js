
    const EDIT_GAME_CONTAINER = document.getElementById("edit-game-container");
    const VIDEO_GAME_ID = document.getElementById("video-game-id");
    const TITLE_INPUT = document.getElementById("title");
    const PUBLISHER_INPUT = document.getElementById("publisher");
    const YEAR_INPUT = document.getElementById("year");
    const INVENTORY_INPUT = document.getElementById("inventory");
    const GENRE_INPUT = document.getElementById("genre");
    const EDIT_BUTTON = document.getElementById("edit-game-button");

    // Modal elements
    const MODAL = document.getElementById("custom-modal");
    const MODAL_BODY = document.querySelector("#custom-modal .modal-body");
    const MODAL_CONFIRM_BUTTON = document.querySelector(".confirm-button");
    const MODAL_CANCEL_BUTTON = document.querySelector(".cancel-button");
    const SUCCESS_MODAL = document.getElementById("success-modal");
    const SUCCESS_MESSAGE = document.getElementById("success-message");
    const CLOSE_SUCCESS_MODAL = document.getElementById("close-success-modal");

    let originalData = {};
        // autopopulate form with video game details on load
    window.onload = autopopulateForm;

    function autopopulateForm() {
        let videoGameID = EDIT_GAME_CONTAINER.getAttribute("data-video-game-id");
        let params = { VideoGameID: videoGameID };

        postRequestParams("edit_game", params, populateForm, handleError);
    }

    function populateForm(data) {
        if (!data["Video Game Details Requested"] || data["Video Game Details Requested"].length === 0) {
            console.error("No game details found in response.");
            return;
        }
        const game = data["Video Game Details Requested"][0];

        VIDEO_GAME_ID.value = game['VideoGameID']||"";
        TITLE_INPUT.value = game['Title']||"";
        PUBLISHER_INPUT.value = game['Publisher']||"";
        YEAR_INPUT.value = game['Year']||"";
        INVENTORY_INPUT.value = game['Inventory']||"";
        GENRE_INPUT.value = game['Genre']||"";

        // Store the original data
        originalData = {
            VideoGameID: game['VideoGameID'],
            Title: game['Title'],
            Publisher: game['Publisher'],
            Year: game['Year'],
            Inventory: game['Inventory'],
            Genre: game['Genre']
        };
    }
    EDIT_BUTTON.addEventListener("click", validateAndOpenModal);
    function validateAndOpenModal(event) {
        event.preventDefault();
    
        if (!originalData.VideoGameID) {
            alert("Game details not loaded. Please refresh the page.");
            return;
        }
    
        const changes = [];
        if (TITLE_INPUT.value.trim() !== (originalData.Title || "")) {
            changes.push(`Title: ${TITLE_INPUT.value.trim()}`);
        }
        if (PUBLISHER_INPUT.value.trim() !== (originalData.Publisher || "")) {
            changes.push(`Publisher: ${PUBLISHER_INPUT.value.trim()}`);
        }
        if (YEAR_INPUT.value.trim() !== (originalData.Year ? originalData.Year.toString() : "")) {
            changes.push(`Year: ${YEAR_INPUT.value.trim()}`);
        }
        if (INVENTORY_INPUT.value.trim() !== (originalData.Inventory ? originalData.Inventory.toString() : "")) {
            changes.push(`Inventory: ${INVENTORY_INPUT.value.trim()}`);
        }
        if (GENRE_INPUT.value.trim() !== (originalData.Genre || "")) {
            changes.push(`Genre: ${GENRE_INPUT.value.trim()}`);
        }
    
        if (changes.length === 0) {
            MODAL_BODY.innerHTML = "<p>No changes detected.</p>";
            MODAL_CONFIRM_BUTTON.textContent = "Go Back";
            MODAL_CONFIRM_BUTTON.replaceWith(MODAL_CONFIRM_BUTTON.cloneNode(true)); // Reset listeners
            document.querySelector(".confirm-button").addEventListener("click", closeModal);
        } else {
            MODAL_BODY.innerHTML = `
                <p>Confirm the following changes:</p>
                <ul>${changes.map(change => `<li>${change}</li>`).join("")}</ul>
            `;
            MODAL_CONFIRM_BUTTON.textContent = "Confirm";
            MODAL_CONFIRM_BUTTON.replaceWith(MODAL_CONFIRM_BUTTON.cloneNode(true)); // Reset listeners
            document.querySelector(".confirm-button").addEventListener("click", submitChanges);
        }
    
        MODAL.style.display = "block";
    }
    

    function submitChanges() {
        let currentData = {
            VideoGameID: VIDEO_GAME_ID.value,
            Title: TITLE_INPUT.value.trim(),
            Publisher: PUBLISHER_INPUT.value.trim(),
            Year: YEAR_INPUT.value.trim(),
            Inventory: INVENTORY_INPUT.value.trim(),
            Genre: GENRE_INPUT.value.trim()
        };

        const noChange = Object.keys(currentData).every(key => currentData[key] === originalData[key]);

        if (noChange) {
            noGameChangeMessage();
            return;
        }

        //proceed with submitting data
        let params = {
            VideoGameID: VIDEO_GAME_ID.value,
            Request: "verified",
            Title: TITLE_INPUT.value.trim() || null,
            Publisher: PUBLISHER_INPUT.value.trim() || null,
            Year: YEAR_INPUT.value.trim() || null,
            Inventory: INVENTORY_INPUT.value.trim() || null,
            Genre: GENRE_INPUT.value.trim() || null
        };

        postRequestParams("edit_game", params, dryRunData, handleError);
        closeModal();
    }

    function dryRunData(data) {
        if (data.message === "Please confirm the details"){
            console.log("Dry run successful:", data);
            handleFinalConfirmation();
        }
        else{
            handleError(data);
        }
    }

    function handleFinalConfirmation() {
        const params = {
            Confirm: "confirmed",
            VideoGameID: originalData.VideoGameID,
            Title: TITLE_INPUT.value.trim() || null,
            Publisher: PUBLISHER_INPUT.value.trim() || null,
            Year: YEAR_INPUT.value.trim() || null,
            Inventory: INVENTORY_INPUT.value.trim() || null,
            Genre: GENRE_INPUT.value.trim() || null
        };
    
        postRequestParams("edit_game", params, handleConfirmResponse, handleError);
    }
    function handleConfirmResponse(data) {
        if (data && data.length > 0) {
            SUCCESS_MESSAGE.innerHTML = "<p>Video Game updated successfully!</p>";
            SUCCESS_MODAL.style.display = "block";
    
            // Update original data
            const updatedGame = data[0];
            originalData = {
                VideoGameID: updatedGame["VideoGameID"],
                Title: updatedGame["Title"],
                Publisher: updatedGame["Publisher"],
                Year: updatedGame["Year"],
                Inventory: updatedGame["Inventory"],
                Genre: updatedGame["Genre"]
            };
    
            // Update form fields
            VIDEO_GAME_ID.value = updatedGame["VideoGameID"];
            TITLE_INPUT.value = updatedGame["Title"];
            PUBLISHER_INPUT.value = updatedGame["Publisher"];
            YEAR_INPUT.value = updatedGame["Year"];
            INVENTORY_INPUT.value = updatedGame["Inventory"];
            GENRE_INPUT.value = updatedGame["Genre"];
        } else {
            handleError(data);
        }
    }
    
    function handleError(error) {
        alert(`Error: ${error.error || "Unknown error occurred"}`);
    }

    function closeModal() {
        MODAL.style.display = "none";
    }

    CLOSE_SUCCESS_MODAL.addEventListener("click", () => {
        SUCCESS_MODAL.style.display = "none";
    });



