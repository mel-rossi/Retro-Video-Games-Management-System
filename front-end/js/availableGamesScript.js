function searchGames(){
    let searchOption = "all";
    let searchInput = "";

    $.ajax({        
        type: "POST",
        url: "../../search.py",
        data: JSON.stringify({
            option: searchOption,
            input: searchInput            
        }),
        success: function(response) {
            console.log(response);
        },
        error: function(err){
            console.error('Error in grabbing games:', err);
        }
    })
}