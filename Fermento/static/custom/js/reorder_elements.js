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
}

let tdElements = document.querySelectorAll("tbody td:last-child");

for (let td of tdElements) {
    td.setAttribute("draggable", true);
    td.addEventListener("dragstart", dragit);
    td.addEventListener("dragover", dragover);
    td.style.cursor = "pointer";
}