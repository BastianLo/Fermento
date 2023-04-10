let shadow;

function dragit(event) {
    shadow = event.target.parentNode;
}

function dragover(e) {
    let children = Array.from(e.target.parentNode.parentNode.children);
    if (children.indexOf(e.target.parentNode) > children.indexOf(shadow))
        e.target.parentNode.after(shadow);
    else
        e.target.parentNode.before(shadow);

    let tableBody = e.target.parentNode.parentNode
    // Get all the rows in the table body
    const rows = tableBody.querySelectorAll('tr.process-step');
    // Loop through all the rows and update their first column with the new index
    rows.forEach((row, index) => {
        // Get the first column cell of the row
        const firstCol = row.querySelector('td:first-child');
        console.log(firstCol)
        // Update the text content of the first column with the new index
        firstCol.textContent = index + 1;
    });

}

let tdElements = document.querySelectorAll("tbody td:last-child");

for (let td of tdElements) {
    td.setAttribute("draggable", true);
    td.addEventListener("dragstart", dragit);
    td.addEventListener("dragover", dragover);
    td.style.cursor = "pointer";
}