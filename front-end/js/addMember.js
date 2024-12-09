
window.onload = function() {
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

    if(SUBMIT_BUTTON){
    SUBMIT_BUTTON.addEventListener("click", openModal);
    }
    else{
        console.log("Submit button not found");
    }

    function openModal(event) {
        event.preventDefault(); // prevent form submission

        // check if any of the required fields are empty
        if (!FIRST_NAME_INPUT.value.trim() || 
            !LAST_NAME_INPUT.value.trim() || 
            !PHONE_NUMBER_INPUT.value.trim()|| 
            !EMAIL_INPUT.value.trim()) {

            emptyFieldsMessage();
            MODAL.style.display = "block";
            return;
        }
        // show the entered details
        const ENTERED_DETAILS= `
        <p>Please confirm the following details for the new member:</p>
        <ul>
            <li>First Name: ${FIRST_NAME_INPUT.value.trim() || "[Not Provided]"} </li>
            <li>Last Name: ${LAST_NAME_INPUT.value.trim() || "[Not Provided]"} </li>
            <li>Phone Number: ${PHONE_NUMBER_INPUT.value.trim() || "[Not Provided]"} </li>
            <li>Email: ${EMAIL_INPUT.value.trim() || "[Not Provided]"} </li>
        </ul> `;

       // MODAL.querySelector(".modal-header").textContent = "Confirm Details";
        MODAL_BODY.innerHTML = ENTERED_DETAILS;
        MODAL.style.display = "block";
        MODAL_CONFIRM_BUTTON.textContent = "Confirm";
        MODAL_CONFIRM_BUTTON.removeEventListener("click", handleSubmit); // remove any old event listener
        MODAL_CONFIRM_BUTTON.addEventListener("click", handleSubmit);
    }

    function closeModal() {
        MODAL.style.display = "none";
        MODAL_CONFIRM_BUTTON.removeEventListener("click", handleSubmit);
        MODAL_CONFIRM_BUTTON.addEventListener("click", openModal);
    }
        MODAL_CANCEL_BUTTON.addEventListener("click", closeModal);

    function handleSubmit() {
        const NEW_MEMBER_DATA = {
            FirstName: FIRST_NAME_INPUT.value.trim(),
            LastName: LAST_NAME_INPUT.value.trim(),
            PhoneNumber: PHONE_NUMBER_INPUT.value.trim(),
            Email: EMAIL_INPUT.value.trim()
        };

        let params ={
            Confirm: 'confirmed',
            FirstName: NEW_MEMBER_DATA.FirstName,
            LastName: NEW_MEMBER_DATA.LastName,
            PhoneNumber: NEW_MEMBER_DATA.PhoneNumber,
            Email: NEW_MEMBER_DATA.Email

        };

        console.log("Submitting new member data:", NEW_MEMBER_DATA);

        postRequestParams("add_member", params, handleResponse, () =>{});

        closeModal();//close modal after successful submission
    }

    function emptyFieldsMessage(){
        MODAL_BODY.innerHTML = `
        <p>Please fill in all required fields.</p>
    `;
        MODAL.querySelector(".modal-header").textContent = "Field Error";
        //change button labels to Go back and Cancel
        MODAL_CONFIRM_BUTTON.textContent = "Go Back";
        MODAL_CONFIRM_BUTTON.removeEventListener("click", handleSubmit);
        MODAL_CONFIRM_BUTTON.addEventListener("click", closeModal); // remove any old event listener
        }
        MODAL.querySelector(".modal-header").textContent = "Confirm Member";


    function handleResponse(data) {
        console.log("Response:", data);
        if (data && !data.error) {
            showSuccessModal();
        } else {
            RESPONSE.textContent = `Error: ${data.error}`;
            RESPONSE.className = "error";
        }
    }

    function showSuccessModal() {
        SUCCESS_MODAL.style.display = "block";
        SUCCESS_MESSAGE.textContent = "Member added successfully.";
    }

    CLOSE_SUCCESS_MODAL.addEventListener("click", () => {
        SUCCESS_MODAL.style.display = "none";
    });

    window.addEventListener("click", (event) => {
        if (event.target == SUCCESS_MODAL) {
            SUCCESS_MODAL.style.display = "none";
        }
    });
}

