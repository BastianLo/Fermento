function addIngredient(processNum) {
    // Find the number of existing ingredients
    var numIngredients = document.querySelectorAll('.ingredient').length;
    var numProcessSteps = document.querySelectorAll(`#process-steps-${processNum} .process-step`).length;

    // Create a new ingredient element
    var newIngredient = document.createElement('tr');
    //newIngredient.setAttribute("draggable", "true")
    //newIngredient.setAttribute("ondragstart", "dragit(event)")
    //newIngredient.setAttribute("ondragover", "dragover(event)")

    // Add the HTML for the new ingredient
    newIngredient.innerHTML = `
    <th><input type="text" class="form-control" id="ingredient-name-${processNum}-${numIngredients}" name="ingredient-name-${processNum}-${numIngredients}"></input></th>
    <th><input type="number" class="form-control" id="ingredient-amount-${processNum}-${numIngredients}" name="ingredient-amount-${processNum}-${numIngredients}"></input></th>
    <th><input type="text" class="form-control" id="ingredient-unit-${processNum}-${numIngredients}" name="ingredient-unit-${processNum}-${numIngredients}"></input></th>
    <td draggable="true"  ondragstart="dragit(event)"  ondragover="dragover(event)" style="cursor:pointer">&#9776;</td>
    `;

    // Append the new ingredient to the ingredients container
    var ingredientsContainer = document.getElementById(`process-ingredients-${processNum}`);
    ingredientsContainer.appendChild(newIngredient);
}

function addProcess() {
    console.log(gettext('Welcome to my site.'))
    // Find the number of existing processes
    var numProcesses = document.querySelectorAll('.process').length;

    // Create a new process element
    var newProcess = document.createElement('div');
    newProcess.className = 'process';

    // Add the HTML for the new process
    newProcess.innerHTML = `
    <div class="card">
        <label for="process-name-${numProcesses}">Name</label>
        <input type="text" class="form-control" id="process-name-${numProcesses}" name="process-name-${numProcesses}">

        <h3>Process Steps</h3>

        <table id="process-steps-${numProcesses}" class="table sortable">

            <colgroup>
                <col span="1" style="width: 5%;">
                <col span="1" style="width: 90%;">
                <col span="1" style="width: 5%;">
            </colgroup>
            <thead>
                <tr>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody class="process-step-body" id="process-steps-${numProcesses}">
            </tbody>
        </table>
        <br/>
        <button class="btn btn-secondary" type="button" onclick="addProcessStep(${numProcesses})">Add Process Step</button>
        <br/><br/><br/>
        <h3>Ingredients</h3>
        <table class="table sortable">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Amount</th>
                    <th>Unit</th>
                </tr>
            </thead>
            <tbody id="process-ingredients-${numProcesses}">
            </tbody>
        </table>
        <br/>
        <button class="btn btn-secondary" type="button" onclick="addIngredient(${numProcesses})">Add Ingredient</button>
    </div>
    `;

    // Append the new process to the processes container
    var processesContainer = document.getElementById('processes');
    processesContainer.appendChild(newProcess);
}

function addProcessStep(processNum) {
    // Find the number of existing process steps for this process
    var numProcessSteps = document.querySelectorAll(`#process-steps-${processNum} .process-step`).length;

    // Create a new process step element
    var newProcessStep = document.createElement('tr');
    newProcessStep.className = 'process-step';

    // Add the HTML for the new process step
    newProcessStep.innerHTML = `
        <td>${numProcessSteps +1}</td>
        <td><textarea class="form-control" id="process-step-text-${processNum}-${numProcessSteps}" name="process-step-text-${processNum}-${numProcessSteps}"></textarea></td>
        <td draggable="true" class="dragicon"  ondragstart="dragit(event)"  ondragover="dragover(event)" style="cursor:pointer">&#9776;</td>
`;

    // Append the new process step to the process steps container for this process
    var processStepsContainer = document.getElementById(`process-steps-${processNum}`);
    processStepsContainer.appendChild(newProcessStep);
}

function createRecipe() {
    console.log("test")
    const form = document.getElementById("create-recipe-form");
    const formData = new FormData(form);

    const processes = [];

    // get all processes
    const processElements = document.querySelectorAll(".process");
    for (let i = 0; i < processElements.length; i++) {
        const processName = processElements[i].querySelector(
            'input[name^="process-name"]'
        ).value;

        const processSteps = [];
        const processStepElements = processElements[i].querySelectorAll(
            '.process-step textarea[name^="process-step-text"]'
        );
        for (let j = 0; j < processStepElements.length; j++) {
            const processStepText = processStepElements[j].value;
            processSteps.push({
                text: processStepText
            });
        }

        const processIngredients = [];
        const processIngredientElements = document.querySelectorAll(".ingredient");
        console.log(processIngredientElements)
        for (let i = 0; i < processIngredientElements.length; i++) {
            const ingredientName = processIngredientElements[i].querySelector(
                'input[name^="ingredient-name"]'
            ).value;
            const ingredientAmount = processIngredientElements[i].querySelector(
                'input[name^="ingredient-amount"]'
            ).value;
            const ingredientUnit = processIngredientElements[i].querySelector(
                'input[name^="ingredient-unit"]'
            ).value;

            processIngredients.push({
                name: ingredientName,
                amount: ingredientAmount,
                unit: ingredientUnit,
            });
        }

        processes.push({
            name: processName,
            steps: processSteps,
            ingredients: processIngredients
        });
    }

    // add ingredients and processes to formData
    formData.append("ingredients", JSON.stringify(ingredients));
    formData.append("processes", JSON.stringify(processes));

    console.log(formData)
    // send form data to server
    fetch("/create_recipe/", {
            method: "POST",
            body: formData,
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            alert("Recipe created successfully!");
            form.reset();
        })
        .catch((error) => {
            console.error(error);
            alert("Error creating recipe!");
        });
}