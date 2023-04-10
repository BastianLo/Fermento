var _el;

function dragOver(e) {
    if (isBefore(_el, e.target))
        e.target.parentNode.insertBefore(_el, e.target);
    else
        e.target.parentNode.insertBefore(_el, e.target.nextSibling);
}

function dragStart(e) {
    e.dataTransfer.effectAllowed = "move";
    e.dataTransfer.setData("text/plain", null); // Thanks to bqlou for their comment.
    _el = e.target;
}

function isBefore(el1, el2) {
    if (el2.parentNode === el1.parentNode)
        for (var cur = el1.previousSibling; cur && cur.nodeType !== 9; cur = cur.previousSibling)
            if (cur === el2)
                return true;
    return false;
}