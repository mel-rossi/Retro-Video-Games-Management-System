function bodyOnLoad(){
    
}

function searchCustomer(){
    postRequestParams("search_member", {'input': ''}, temp);
}

function temp(data){
    console.log(data);
}