initialize_edit_fields()

function initialize_edit_fields() {
    document.getElementById(`name`).value = edit_recipe[0]["fields"]["name"]
    document.getElementById(`description`).value = edit_recipe[0]["fields"]["description"]
    document.getElementById(`difficulty`).value = edit_recipe[0]["fields"]["difficulty"]
    let count = 0
    edit_processes.forEach(process => {
        process["ingredients"] = JSON.parse(process["ingredients"])
        process["process_steps"] = JSON.parse(process["process_steps"])
        process["utils"] = JSON.parse(process["utils"])
        process["schedule"] = JSON.parse(process["schedule"])

        createProcess(process["fields"]["name"], process["fields"]["work_duration"], process["fields"]["wait_duration"], process["pk"])
        process["ingredients"].forEach(ingredient => createIngredient(count, ingredient["fields"]["name"], ingredient["fields"]["amount"], ingredient["fields"]["unit"], ingredient["pk"]))
        process["utils"].forEach(util => createUtil(count, util["fields"]["name"], util["pk"]))
        process["process_steps"].forEach(process_step => createProcessStep(count, process_step["fields"]["text"], process_step["pk"]))
        process["schedule"].forEach(schedule => createSchedule(count, schedule["fields"]["executed_once"], schedule["fields"]["start_time"], schedule["fields"]["wait_time"], schedule["fields"]["end_time"], schedule["pk"]))
        count += 1
    });
}

function delete_parent(e) {
    let t = e.parentNode.parentNode.parentNode
    e.parentNode.parentNode.parentNode.removeChild(e.parentNode.parentNode);
    refreshOrder(t)
}

function addIngredient(processNum) {
    createIngredient(processNum, "", "", "", -1)
}

function createIngredient(processNum, name, amount, unit, ingredient_id) {
    // Find the number of existing ingredients
    let numIngredients = document.querySelectorAll('.ingredient').length;

    // Create a new ingredient element
    let newIngredient = document.createElement('tr');
    newIngredient.classList.add("ingredient")

    // Add the HTML for the new ingredient
    newIngredient.innerHTML = `
    <input type="hidden" id="ingredientid" name="ingredientid" value="${ingredient_id}"> 
    <th><input type="text" class="form-control" id="ingredient-name-${processNum}-${numIngredients}" name="ingredient-name-${processNum}-${numIngredients}" value="${name}"></input></th>
    <th><input type="number" class="form-control" id="ingredient-amount-${processNum}-${numIngredients}" name="ingredient-amount-${processNum}-${numIngredients}" value=${amount}></input></th>
    <th><input type="text" class="form-control" id="ingredient-unit-${processNum}-${numIngredients}" name="ingredient-unit-${processNum}-${numIngredients}" value=${unit}></input></th>
    <td draggable="true"  ondragstart="dragit(event)"  ondragover="dragover(event)" style="cursor:pointer">&#9776;</td>
    <td><button class="btn btn-danger" type="button" onClick="delete_parent(this)">${gettext("delete")}</button></td>
    `;

    // Append the new ingredient to the ingredients container
    let ingredientsContainer = document.getElementById(`process-ingredients-${processNum}`);
    ingredientsContainer.appendChild(newIngredient);
}

function addUtil(processNum) {
    createUtil(processNum, "", -1)
}

function createUtil(processNum, name, util_id) {
    // Find the number of existing ingredients
    let numUtils = document.querySelectorAll('.util').length;

    // Create a new ingredient element
    let newIngredient = document.createElement('tr');
    newIngredient.classList.add("util")

    // Add the HTML for the new ingredient
    newIngredient.innerHTML = `
    <input type="hidden" id="utilid" name="utilid" value="${util_id}"> 
    <th><input type="text" class="form-control" id="util-name-${processNum}-${numUtils}" name="util-name-${processNum}-${numUtils}" value="${name}"></input></th>
    <td draggable="true"  ondragstart="dragit(event)"  ondragover="dragover(event)" style="cursor:pointer">&#9776;</td>
    <td><button class="btn btn-danger" type="button" onClick="delete_parent(this)">${gettext("delete")}</button></td>
    `;

    // Append the new ingredient to the ingredients container
    let ingredientsContainer = document.getElementById(`process-utils-${processNum}`);
    ingredientsContainer.appendChild(newIngredient);
}

function addSchedule(processNum) {
    createSchedule(processNum, false, "00:00:00", "00:00:00", "00:00:00", -1)
}

function createSchedule(processNum, runOnce, start, frequency, end, schedule_id) {
    // Find the number of existing ingredients
    let numSchedules = document.querySelectorAll('.schedule').length;

    // Create a new ingredient element
    let newSchedule = document.createElement('tr');
    newSchedule.classList.add("schedule")

    // Add the HTML for the new ingredient
    newSchedule.innerHTML = `
    <input type="hidden" id="scheduleid" name="scheduleid" value="${schedule_id}"> 
    <th><input type="checkbox" name="runonce" id="schedule-runonce-${processNum}-${numSchedules}" value=""></th>
    <th><input value='${start}' class="form-control" name="start" type="text" name="start_time" required="" id="schedule-start-${processNum}-${numSchedules}"></th>
    <th><input value='${frequency}' class="form-control" name="frequency" type="text" name="frequency_time" required="" id="schedule-frequency-${processNum}-${numSchedules}"></th>
    <th><input value='${end}' class="form-control" name="end" type="text" name="end_time" required="" id="schedule-end-${processNum}-${numSchedules}"></th>
    <th><button class="btn btn-danger" type="button" onClick="delete_parent(this)">${gettext("delete")}</button></th>
    `;

    // Append the new ingredient to the ingredients container
    let ingredientsContainer = document.getElementById(`process-schedule-${processNum}`);
    ingredientsContainer.appendChild(newSchedule);

    document.getElementById(`schedule-runonce-${processNum}-${numSchedules}`).onchange = function () {
        document.getElementById(`schedule-frequency-${processNum}-${numSchedules}`).disabled = this.checked;
        document.getElementById(`schedule-end-${processNum}-${numSchedules}`).disabled = this.checked;
    };
    let checkbox = document.getElementById(`schedule-runonce-${processNum}-${numSchedules}`);
    checkbox.checked = runOnce;
    checkbox.onchange();
}

function addProcess() {
    createProcess("", "00:00:00", "00:00:00", -1)
}

function createProcess(name, work_duration, wait_duration, process_id) {
    // Find the number of existing processes
    let numProcesses = document.querySelectorAll('.process').length;

    // Create a new process element
    let newProcess = document.createElement('div');
    newProcess.className = 'process';

    // Add the HTML for the new process
    newProcess.innerHTML = `
    <div class="card">
        <label for="process-name-${numProcesses}">${gettext("name")}</label>
        <input value="${name}" type="text" class="form-control" id="process-name-${numProcesses}" name="process-name-${numProcesses}"/>
        <input type="hidden" id="processid" name="processid" value="${process_id}"/> 
        
        <div class="container-fluid">
            <div class="row">
                <div class="col-sm">
                    <label for="process-work-duration-${numProcesses}">${gettext("work_duration")}</label>
                    <input value='${work_duration}' class="form-control" name="work_duration" type="text" required="" id="process-work-duration-${numProcesses}"></input>
                </div>
                <div class="col-sm">
                    <label for="process-wait-duration-${numProcesses}">${gettext("wait_duration")}</label>
                    <input value='${wait_duration}' class="form-control" name="wait_duration" type="text" required="" id="process-wait-duration-${numProcesses}"></input>
                </div>
            </div>
        </div>
        
        
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
    let processesContainer = document.getElementById('processes');
    processesContainer.appendChild(newProcess);
}

function addProcessStep(processNum) {
    createProcessStep(processNum, "", -1)
}

function createProcessStep(processNum, text, process_step_id) {
    // Find the number of existing process steps for this process
    let numProcessSteps = document.querySelectorAll(`#process-steps-${processNum} .process-step`).length;

    // Create a new process step element
    let newProcessStep = document.createElement('tr');
    newProcessStep.className = 'process-step';

    // Add the HTML for the new process step
    newProcessStep.innerHTML = `
        <input type="hidden" id="processstepid" name="processstepid" value="${process_step_id}"> 
        <td>${numProcessSteps +1}</td>
        <td><textarea class="form-control" id="process-step-text-${processNum}-${numProcessSteps}" name="process-step-text-${processNum}-${numProcessSteps}">${text}</textarea></td>
        <td draggable="true" class="dragicon"  ondragstart="dragit(event)"  ondragover="dragover(event)" style="cursor:pointer">&#9776;</td>
        <td><button class="btn btn-danger" type="button" onClick="delete_parent(this)">${gettext("delete")}</button></td>
        `;

    // Append the new process step to the process steps container for this process
    let processStepsContainer = document.getElementById(`process-steps-${processNum}`);
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
        const processWork = processElements[i].querySelector(
            'input[name^="work_duration"]'
        ).value;
        const processWait = processElements[i].querySelector(
            'input[name^="wait_duration"]'
        ).value;
        const processId = processElements[i].querySelector(
            'input[name^="processid"]'
        ).value;

        const processSteps = [];
        const processStepElements = processElements[i].querySelectorAll('.process-step');
        for (let j = 0; j < processStepElements.length; j++) {
            processSteps.push({
                text: processStepElements[j].querySelector('textarea[name^="process-step-text"]').value,
                id: processStepElements[j].querySelector('input[name^="processstepid"]').value
            });
        }

        const processIngredients = [];
        const processIngredientElements = processElements[i].querySelectorAll(".ingredient");
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
            const ingredientId = processIngredientElements[i].querySelector(
                'input[name^="ingredientid"]'
            ).value;

            processIngredients.push({
                name: ingredientName,
                amount: ingredientAmount,
                unit: ingredientUnit,
                id: ingredientId,
            });
        }

        const processUtils = [];
        const processUtilElements = processElements[i].querySelectorAll(".util");
        console.log(processUtilElements)
        for (let i = 0; i < processUtilElements.length; i++) {
            const utilName = processUtilElements[i].querySelector(
                'input[name^="util-name"]'
            ).value;
            const utilId = processUtilElements[i].querySelector(
                'input[name^="utilid"]'
            ).value;

            processUtils.push({
                name: utilName,
                id: utilId
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
            const scheduleId = processScheduleElements[i].querySelector(
                'input[name^="scheduleid"]'
            ).value;

            processSchedules.push({
                runOnce: scheduleRunOnce,
                start: scheduleStart,
                frequency: scheduleFrequency,
                end: scheduleEnd,
                id: scheduleId,
            });
        }

        processes.push({
            name: processName,
            wait_duration: processWait,
            work_duration: processWork,
            id: processId,
            steps: processSteps,
            ingredients: processIngredients,
            schedules: processSchedules,
            utils: processUtils
        });
    }
    // add processes to formData
    formData.append("processes", JSON.stringify(processes));

    console.log(formData)
    // send form data to server
    fetch("", {
            method: "POST",
            body: formData,
        })
        .then((response) => response.json())
        .then((data) => {
            form.reset();
            if (window.location.href.includes("edit")) {
                window.location.href = "."
            } else {
                window.location.href = "./" + data["recipe_id"];
            }
        })
        .catch((error) => {
            console.error(error);
            alert("Error creating recipe!");
        });
}