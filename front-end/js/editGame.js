
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

        postRequestParams("edit_game", params, populateGameForm, handleError);
    }

    function populateGameForm(data) {
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
            noGameChangeMessage();
                //change button labels to Go back and Cancel
        MODAL_CONFIRM_BUTTON.textContent = "Go Back";
        MODAL_CONFIRM_BUTTON.removeEventListener("click", submitChanges);
        MODAL_CONFIRM_BUTTON.addEventListener("click", closeModal); // remove any old event listener
        }
        else {
            const CONFIRMATION_MESSAGE = `
            <p>Please confirm the following changes for video game: <strong>${VIDEO_GAME_ID.value}</strong></p>
           
            <ul>
              ${changes.map(change => `<li>${change}</li>`).join('')}
            </ul>`;
    
            MODAL_BODY.innerHTML = CONFIRMATION_MESSAGE;
    
            //change back button labels to Confirm and Cancel
            MODAL_CONFIRM_BUTTON.textContent = "Confirm";
            MODAL_CONFIRM_BUTTON.removeEventListener("click", closeModal);
            MODAL_CONFIRM_BUTTON.addEventListener("click", submitChanges);
        }
            MODAL.style.display = "block";
    }
    function closeModal() {
        MODAL.style.display = "none";
        MODAL_BODY.innerHTML = ""; // Clear modal content
        MODAL.querySelector(".modal-header").textContent = "Confirm Changes"; // Reset the modal header to its default
        MODAL_CONFIRM_BUTTON.textContent = "Confirm"; // Reset confirm button text
        MODAL_CANCEL_BUTTON.style.display = "block"; // Ensure the cancel button is displayed
    }
    MODAL_CANCEL_BUTTON.addEventListener("click", closeModal);
    MODAL_CONFIRM_BUTTON.addEventListener("click", submitChanges);    

    function submitChanges() {
        let currData = {
            VideoGameID: VIDEO_GAME_ID.value,
            Title: TITLE_INPUT.value.trim(),
            Publisher: PUBLISHER_INPUT.value.trim(),
            Year: YEAR_INPUT.value.trim(),
            Inventory: INVENTORY_INPUT.value.trim(),
            Genre: GENRE_INPUT.value.trim()
        };

        //compare current data with original data
        const noChangesMade = Object.keys(currData).every(key => currData[key] === originalData[key]);

        if (noChangesMade) {
            noGameChangeMessage(); // display no change message
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
    function noGameChangeMessage() {
            MODAL_BODY.innerHTML = `<p>No changes detected.</p>`;
            MODAL.querySelector(".modal-header").textContent = "Change Error";
    }

    function successModal(){
        MODAL.style.display="block";
        SUCCESS_MESSAGE.textContent = "Changes saved successfully!";
    }
    CLOSE_SUCCESS_MODAL.addEventListener("click", () => {
        SUCCESS_MODAL.style.display = "none";
    });
    window,addEventListener("click", (event) => {
        if (event.target === SUCCESS_MODAL) {
            SUCCESS_MODAL.style.display = "none";
        }
    });
function dryRunData(data) {
    if (data && !data.error) {
        successModal();

    // Update originalData and form fields
        originalData = {
            VideoGameID: data[0]["VideoGameID"] || originalData.VideoGameID,
            Title: data[0]["Title"] || originalData.Title,
            Publisher: data[0]["Publisher"] || originalData.Publisher,
            Year: data[0]["Year"] || originalData.Year,
            Inventory: data[0]["Inventory"] || originalData.Inventory,
            Genre: data[0]["Genre"] || originalData.Genre
        };

        VIDEO_GAME_ID.value = originalData.VideoGameID;
        TITLE_INPUT.value = originalData.Title;
        PUBLISHER_INPUT.value = originalData.Publisher;
        YEAR_INPUT.value = originalData.Year;
        INVENTORY_INPUT.value = originalData.Inventory;
        GENRE_INPUT.value = originalData.Genre;
    }
    else{
        RESPONSE.TextContent = `Error: ${data.error}`;
        RESPONSE.className = "error";
    }
}
    
    
function handleError(error) {
    alert(`Error: ${error.error || "Unknown error occurred"}`);
}

