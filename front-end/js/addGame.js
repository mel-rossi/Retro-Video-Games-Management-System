
async function submitForm() {
    const title = document.getElementById('title').value;
    const publisher = document.getElementById('publisher').value;
    const year = document.getElementById('year').value;
    const inventory = document.getElementById('inventory').value;
    const genre = document.getElementById('genre').value;

    const formData = {
        Title: title,
        Publisher: publisher,
        Year: year,
        Inventory: inventory,
        Genre: genre
    };

    // Initial Dry Run (Validation)
    const dryRunResponse = await fetch('http://yourserver.com/add_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    });

    const dryRunData = await dryRunResponse.json();

    // Check if confirmation is needed
    if (dryRunData.message && dryRunData.message === "Please confirm the details") {
        document.getElementById('confirmationMessage').innerHTML = `
            <p>Please confirm the details:</p>
            <ul>
                <li>Title: ${dryRunData['Title Entered']}</li>
                <li>Publisher: ${dryRunData['Publisher Entered']}</li>
                <li>Year: ${dryRunData['Year Entered']}</li>
                <li>Inventory: ${dryRunData['Inventory Entered']}</li>
                <li>Genre: ${dryRunData['Genre(s) Entered']}</li>
            </ul>
            <button onclick="confirmSubmission()">Confirm</button>
        `;
    } else {
        // Show error messages
        document.getElementById('confirmationMessage').innerHTML = `<p style="color: red;">${dryRunData.error}</p>`;
    }
}

async function confirmSubmission() {
    const formData = {
        Title: document.getElementById('title').value,
        Publisher: document.getElementById('publisher').value,
        Year: document.getElementById('year').value,
        Inventory: document.getElementById('inventory').value,
        Genre: document.getElementById('genre').value,
        Confirm: 'confirmed'
    };

    const confirmResponse = await fetch('http://yourserver.com/add_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    });

    const confirmData = await confirmResponse.json();

    if (confirmData['Registration Added']) {
        document.getElementById('confirmationMessage').innerHTML = `
            <p>Game successfully added:</p>
            <ul>
                <li>Title: ${confirmData['Registration Added'][0].Title}</li>
                <li>Publisher: ${confirmData['Registration Added'][0].Publisher}</li>
                <li>Year: ${confirmData['Registration Added'][0].Year}</li>
                <li>Inventory: ${confirmData['Registration Added'][0].Inventory}</li>
                <li>Genre: ${confirmData['Registration Added'][0].Genre}</li>
            </ul>
        `;
    } else {
        document.getElementById('confirmationMessage').innerHTML = `<p style="color: red;">Error: ${confirmData.error}</p>`;
    }
}
