function delete_parent(e) {
    var t = e.parentNode.parentNode.parentNode
    e.parentNode.parentNode.parentNode.removeChild(e.parentNode.parentNode);
    refreshOrder(t)
}

function addIngredient(processNum) {
    // Find the number of existing ingredients
    var numIngredients = document.querySelectorAll('.ingredient').length;
    var numProcessSteps = document.querySelectorAll(`#process-steps-${processNum} .process-step`).length;

    // Create a new ingredient element
    var newIngredient = document.createElement('tr');
    newIngredient.classList.add("ingredient")

    // Add the HTML for the new ingredient
    newIngredient.innerHTML = `
    <th><input type="text" class="form-control" id="ingredient-name-${processNum}-${numIngredients}" name="ingredient-name-${processNum}-${numIngredients}"></input></th>
    <th><input type="number" class="form-control" id="ingredient-amount-${processNum}-${numIngredients}" name="ingredient-amount-${processNum}-${numIngredients}"></input></th>
    <th><input type="text" class="form-control" id="ingredient-unit-${processNum}-${numIngredients}" name="ingredient-unit-${processNum}-${numIngredients}"></input></th>
    <td draggable="true"  ondragstart="dragit(event)"  ondragover="dragover(event)" style="cursor:pointer">&#9776;</td>
    <td><button class="btn btn-danger" type="button" onClick="delete_parent(this)">${gettext("delete")}</button></td>
    `;

    // Append the new ingredient to the ingredients container
    var ingredientsContainer = document.getElementById(`process-ingredients-${processNum}`);
    ingredientsContainer.appendChild(newIngredient);
}
function addUtil(processNum) {
    // Find the number of existing ingredients
    var numUtils = document.querySelectorAll('.util').length;
    var numProcessSteps = document.querySelectorAll(`#process-steps-${processNum} .process-step`).length;

    // Create a new ingredient element
    var newIngredient = document.createElement('tr');
    newIngredient.classList.add("util")

    // Add the HTML for the new ingredient
    newIngredient.innerHTML = `
    <th><input type="text" class="form-control" id="util-name-${processNum}-${numUtils}" name="util-name-${processNum}-${numUtils}"></input></th>
    <td draggable="true"  ondragstart="dragit(event)"  ondragover="dragover(event)" style="cursor:pointer">&#9776;</td>
    <td><button class="btn btn-danger" type="button" onClick="delete_parent(this)">${gettext("delete")}</button></td>
    `;

    // Append the new ingredient to the ingredients container
    var ingredientsContainer = document.getElementById(`process-utils-${processNum}`);
    ingredientsContainer.appendChild(newIngredient);
}

function addSchedule(processNum) {
    // Find the number of existing ingredients
    var numSchedules = document.querySelectorAll('.schedule').length;

    // Create a new ingredient element
    var newSchedule = document.createElement('tr');
    newSchedule.classList.add("schedule")

    // Add the HTML for the new ingredient
    newSchedule.innerHTML = `
    <th><input type="checkbox" name="runonce" id="schedule-runonce-${processNum}-${numSchedules}" value=""></th>
    <th><input class="form-control" name="start" type="text" name="start_time" value="00:00" required="" id="schedule-start-${processNum}-${numSchedules}"></th>
    <th><input class="form-control" name="frequency" type="text" name="frequency_time" value="00:00" required="" id="schedule-frequency-${processNum}-${numSchedules}"></th>
    <th><input class="form-control" name="end" type="text" name="end_time" value="00:00" required="" id="schedule-end-${processNum}-${numSchedules}"></th>
    <th><button class="btn btn-danger" type="button" onClick="delete_parent(this)">${gettext("delete")}</button></th>
    `;

    // Append the new ingredient to the ingredients container
    var ingredientsContainer = document.getElementById(`process-schedule-${processNum}`);
    ingredientsContainer.appendChild(newSchedule);
}

function addProcess() {
    // Find the number of existing processes
    var numProcesses = document.querySelectorAll('.process').length;

    // Create a new process element
    var newProcess = document.createElement('div');
    newProcess.className = 'process';

    // Add the HTML for the new process
    newProcess.innerHTML = `
    <div class="card">
        <label for="process-name-${numProcesses}">${gettext("name")}</label>
        <input type="text" class="form-control" id="process-name-${numProcesses}" name="process-name-${numProcesses}">

        <h3>${gettext("processSteps")}</h3>

        <table class="table sortable">
            <thead>
                <tr>
                    <th></th>
                    <th style="width:90%">${gettext("description")}</th>
                    <th></th>
                    <th></th>
                </tr>
            </thead>
            <tbody class="process-step-body" id="process-steps-${numProcesses}">
            </tbody>
        </table>
        <br/>
        <button class="btn btn-primary" type="button" onclick="addProcessStep(${numProcesses})">${gettext("addProcessStep")}</button>
        <br/><br/><br/>
        <h3>${gettext("ingredients")}</h3>
        <table class="table sortable">
            <thead>
                <tr>
                    <th>${gettext("name")}</th>
                    <th>${gettext("amount")}</th>
                    <th>${gettext("unit")}</th>
                </tr>
            </thead>
            <tbody id="process-ingredients-${numProcesses}">
            </tbody>
        </table>
        <br/>
        <button class="btn btn-primary" type="button" onclick="addIngredient(${numProcesses})">${gettext("addIngredient")}</button>
        <br/><br/><br/>

        <h3>${gettext("utils")}</h3>
        <table class="table sortable">
            <thead>
                <tr>
                    <th>${gettext("name")}</th>
                </tr>
            </thead>
            <tbody id="process-utils-${numProcesses}">
            </tbody>
        </table>
        <br/>
        <button class="btn btn-primary" type="button" onclick="addUtil(${numProcesses})">${gettext("addUtil")}</button>
        <br/><br/><br/>

        <h3>${gettext("schedules")}</h3>
        <div class="table-responsive">
            <table style="width: 100%" class="table sortable table-responsive">
                <thead>
                    <tr>
                        <th>${gettext("runOnce")}</th>
                        <th>${gettext("startTime")}</th>
                        <th>${gettext("frequency")}</th>
                        <th>${gettext("endTime")}</th>
                    </tr>
                </thead>
                <tbody id="process-schedule-${numProcesses}">
                </tbody>
            </table>
        </div>
        <br/>
        <button class="btn btn-primary" type="button" onclick="addSchedule(${numProcesses})">${gettext("addSchedule")}</button>

        <br/><br/><br/><br/>
        <button class="btn btn-danger" type="button" onClick="delete_parent(this)">${gettext("delete")}</button>
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
        <td><button class="btn btn-danger" type="button" onClick="delete_parent(this)">${gettext("delete")}</button></td>
        `;

    // Append the new process step to the process steps container for this process
    var processStepsContainer = document.getElementById(`process-steps-${processNum}`);
    processStepsContainer.appendChild(newProcessStep);
}

function createRecipe() {
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
        const processIngredientElements = processElements[i].querySelectorAll(".ingredient");
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

        const processUtils = [];
        const processUtilElements = processElements[i].querySelectorAll(".util");
        console.log(processUtilElements)
        for (let i = 0; i < processUtilElements.length; i++) {
            const utilName = processUtilElements[i].querySelector(
                'input[name^="util-name"]'
            ).value;

            processUtils.push({
                name: utilName,
            });
        }

        const processSchedules = [];
        const processScheduleElements = processElements[i].querySelectorAll(".schedule");
        console.log(processScheduleElements)
        for (let i = 0; i < processScheduleElements.length; i++) {
            const scheduleRunOnce = processScheduleElements[i].querySelector(
                'input[name^="runonce"]'
            ).checked;
            const scheduleStart = processScheduleElements[i].querySelector(
                'input[name^="start"]'
            ).value;
            const scheduleFrequency = processScheduleElements[i].querySelector(
                'input[name^="frequency"]'
            ).value;
            const scheduleEnd = processScheduleElements[i].querySelector(
                'input[name^="end"]'
            ).value;

            processSchedules.push({
                runOnce: scheduleRunOnce,
                start: scheduleStart,
                frequency: scheduleFrequency,
                end: scheduleEnd
            });
        }

        processes.push({
            name: processName,
            steps: processSteps,
            ingredients: processIngredients,
            schedules: processSchedules,
            utils: processUtils
        });
    }

    // add processes to formData
    formData.append("processes", JSON.stringify(processes));

    // send form data to server
    fetch("", {
            method: "POST",
            body: formData,
        })
        .then((response) => response.json())
        .then((data) => {
            form.reset();
            window.location.href = data["recipe_id"];
        })
        .catch((error) => {
            console.error(error);
            alert("Error creating recipe!");
        });
}