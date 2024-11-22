//Get the member information
const MEMBER_ID = document.getElementById("data-member-id");
const FIRST_NAME = document.getElementById("first-name").value,
const LAST_NAME = document.getElementById("last-name").value,
const PHONE_NUMBER = document.getElementById("phone-number").value,
const EMAIL = document.getElementById("email").value

//Verify the changes
let verifiedParams = {
    Request: "verified",
    MemberID: MEMBER_ID,
    FirstName: FIRST_NAME,
    LastName: LAST_NAME,
    PhoneNumber: PHONE_NUMBER,
    Email: EMAIL
};
postRequestParams('edit_member', verifiedParams, editMember, ()=>{});


//confirm changes
document.getElementById("confirm-button").addEventListener("click", confirmChanges){
    let confirmParams = {
        Confirm: 'confirmed',
        MemberID: MEMBER_ID,
        FirstName: FIRST_NAME,
        LastName: LAST_NAME,
        PhoneNumber: PHONE_NUMBER,
        Email: EMAIL
    }
    postRequestParams('edit_member', confirmParams, editMember, ()=>{});
}

function editMember(data) {
    if (data.error) {
        alert(data.error);
    } else {
        alert("Member updated successfully");
    }
}