const ADD_MEMBER_CONTAINER = document.getElementById("add-member-container");
const FORM = document.getElementById("add-member-form");
const FIRST_NAME_INPUT = document.getElementById("first-name");
const LAST_NAME_INPUT = document.getElementById("last-name");
const PHONE_NUMBER_INPUT = document.getElementById("phone-number");
const EMAIL_INPUT = document.getElementById("email");
const REQUEST_BUTTON = document.getElementById("request-button");
const RESPONSE = document.getElementById("response");

// Modal elements
const MODAL = document.getElementById("custom-modal");
const MODAL_BODY = document.querySelector("#custom-modal .modal-body");
const MODAL_CONFIRM_BUTTON = document.querySelector("#custom-modal .confirm-button");
const MODAL_CANCEL_BUTTON = document.querySelector("#custom-modal .cancel-button");
const SUCCESS_MODAL = document.getElementById("success-modal");
const SUCCESS_MESSAGE = document.getElementById("success-message");
const CLOSE_SUCCESS_MODAL = document.getElementById("close-success-modal");

REQUEST_BUTTON.addEventListener("click", openModal);

function openModal(event) {
    event.preventFefgault(); // prevent form submission

    const ENTERED_DETAILS= `
    <p>Please confirm the following details for the new member:</p>
    <ul>
        <li>First NameL ${FIRST_NAME_INPUT.value.trim() || "[Not Provided]"} </li>
        <li>Last Name: ${LAST_NAME_INPUT.value.trim() || "[Not Provided]"} </li>
        <li>Phone Number: ${PHONE_NUMBER_INPUT.value.trim() || "[Not Provided]"} </li>
        <li>Email: ${EMAIL_INPUT.value.trim() || "[Not Provided]"} </li>
    </ul> `;

    MODAL_BODY.innerHTML = ENTERED_DETAILS;

    MODAL.style.display = "block";

    MODAL_CONFIRM_BUTTON.textContent = "Confirm";
    MODAL_CONFIRM_BUTTON.addEventListener("click", handleSubmit);
}

function closeModal() {
    MODAL.style.display = "none";
    MODAL_CONFIRM_BUTTON.removeEventListener("click", handleSubmit);
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

    postRequestParams("add_member", params, handleResponse, (error) => {
        RESPONSE.textContent = `Error adding member: ${error.Error || "Unknown error"}`;
        RESPONSE.className = "error";
    });
closeModal();//close modal after successful submission
}

function handleResponse(data) {
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
})

window.addEventListener("click", (event) => {
    if (event.target == SUCCESS_MODAL) {
        SUCCESS_MODAL.style.display = "none";
    }
});