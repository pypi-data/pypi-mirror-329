// utilities.ts

const backendUrl = 'http://localhost:8000';
// Function to handle HTTP fetch requests with retries
async function fetchWithRetries(url, options, maxRetries = 50) {
    let retries = 0;
    while (retries < maxRetries) {
        try {
            const response = await fetch(url, options);
            if (response.ok) return response;
            else throw new Error(`Failed to fetch: ${response.status}`);
        } catch (error) {
            console.error(`Attempt ${retries + 1}:`, error);
            await new Promise(resolve => setTimeout(resolve, 1000));
            retries++;
        }
    }
    throw new Error('Max retry attempts exceeded');
}

// Function to create and trigger a download of a Blob
function createDownloadLink(blob, filename) {
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    URL.revokeObjectURL(url);
    document.body.removeChild(link);
}

// Function to start a workflow
async function startWorkflow(workflowName, guiEnabled) {
    const startButton = document.getElementById('start-workflow');
    startButton.disabled = true;
    const url = backendUrl + `/launch-workflow/?workflow_name=${workflowName}&force_reload=false&gui=${guiEnabled}`;
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'accept': 'application/json' }
        });

        if (!response.ok) throw new Error('Failed to start workflow');
        alert(`Workflow started${guiEnabled ? ' with' : ' without'} GUI`);

        let countdown = 5;
        const countdownInterval = setInterval(() => {
            countdown--;
            startButton.textContent = `Workflow is starting... (${countdown})`;
            if (countdown <= 0) {
                clearInterval(countdownInterval);
                startButton.disabled = false;
                startButton.textContent = 'Start Workflow';
                document.getElementById('stop-workflow').style.display = 'inline-block';
            }
        }, 1000);
    } catch (error) {
        console.error('Error starting workflow:', error);
        alert('Failed to start workflow');
        startButton.disabled = false;
        startButton.textContent = 'Start Workflow';
    }
}

// Function to retrieve content (JSON/Files) by uniqueId
async function retrieveContent(returnMode, uniqueId, file_id = null) {
    try {
        console.log("returnMode:", returnMode);
        console.log("uniqueId:", uniqueId);
        // Construct URL with query parameters for uniqueId, returnMode, and optionally filename
        let url = `http://localhost:8000/retrieve-outputs/`;
        url += `${uniqueId}?return_mode=${returnMode}`;
        if (file_id) {
            url += `&file_id=${file_id}`; // Use '&' to add additional query parameter
        }

        const response = await fetchWithRetries(url, {
            method: 'GET',
            headers: { 'accept': 'application/json' }
        });

        // Process response based on return mode
        if (returnMode === 'json') {
            const jsonData = await response.json();
            return jsonData;
        } else if (returnMode === 'html') {
            const htmlData = await response.text();
            return htmlData;
        } else {
            const blob = await response.blob();
            return blob;
        }
    } catch (error) {
        console.error(`Error retrieving content${uniqueId ? ` for uniqueId ${uniqueId}` : ''}:`, error);
        alert('Failed to retrieve content.');
    }
}

async function uploadFilesAndInputs(
    fileIds = [],            // Optional, with default empty array
    workflowId,              // Mandatory
    openingMethods = [],     // Optional, with default empty array
    expectedNbOutputs,       // Mandatory
    files = [],              // Optional, with default empty array
    textInputsId = [],       // Optional, with default empty array
    textInputsValue = [],    // Optional, with default empty array
    timeoutLimit = 0         // Optional, with default value of 0
) {
    // console.log("fileIds:", fileIds);
    // console.log("workflowId:", workflowId);
    // console.log("openingMethods:", openingMethods);
    // console.log("expectedNbOutputs:", expectedNbOutputs);
    // console.log("files:", files);
    // console.log("textInputsId:", textInputsId);
    // console.log("textInputsValue:", textInputsValue);
    // Construct the base URL, including necessary query parameters
    let url = backendUrl + `/upload-files/?workflow_id=${workflowId}&expected_nb_outputs=${expectedNbOutputs}`;

    if (timeoutLimit > 0) {
        url += `&timeout_limit=${timeoutLimit}`;
    }

    const formData = new FormData();

    // Append each file individually, allowing the backend to handle them as uploads
    files.forEach(file => {
        formData.append("files", file, file.name);
    });

    formData.append("file_ids", JSON.stringify(fileIds));
    formData.append("opening_methods", JSON.stringify(openingMethods));

    formData.append("text_inputs_id", JSON.stringify(textInputsId));
    formData.append("text_inputs_value", JSON.stringify(textInputsValue));

    try {
        const response = await fetch(url, {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const result = await response.json();
            console.log("Files uploaded successfully!");
            return result.unique_id;
        } else {
            const errorText = await response.text();
            console.error("Error uploading files, response status:", response.status, "Error message:", errorText);
        }
    } catch (error) {
        console.error("Error occurred during file upload:", error);
    }
}


// Function to stop a workflow
async function stopWorkflow(workflowName) {
    try {
        const response = await fetch(`http://localhost:8000/stop-workflow/?workflow_id=${workflowName}`, {
            method: 'POST',
            headers: { 'accept': 'application/json' }
        });

        if (response.ok) {
            alert('Workflow stopped');
            document.getElementById('stop-workflow').style.display = 'none';
        } else {
            alert('Failed to stop workflow');
        }
    } catch (error) {
        console.error('Error stopping workflow:', error);
    }
}
