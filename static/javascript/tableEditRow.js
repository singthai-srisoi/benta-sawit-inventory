var table = document.querySelector(".datatable");
var tbody = document.querySelector(".datatable tbody");
// edit table function
let jqtable = new DataTable(table);

function makeRowEditable(row) {
    row.querySelectorAll("td").forEach(function (td) {
        td.contentEditable = true;
    });
}

function makeRowUnEditable(row) {
    row.querySelectorAll("td").forEach(function (td) {
        td.contentEditable = false;
    });
}

function selectText(element) {
    if (document.body.createTextRange) {
        // For Internet Explorer
        const range = document.body.createTextRange();
        range.moveToElementText(element);
        range.select();
    } else if (window.getSelection) {
        // For modern browsers
        const selection = window.getSelection();
        const range = document.createRange();
        range.selectNodeContents(element);
        selection.removeAllRanges();
        selection.addRange(range);
    }
}
function resizeTableColumn(event) {
    const col = event.target;
    const table = col.closest("table");
    const colIndex = Array.from(col.parentNode.children).indexOf(col);

    const drag = (e) => {
        const width = e.clientX - col.getBoundingClientRect().left;
        col.style.width = `${width}px`;
    };

    const stopDrag = () => {
        document.removeEventListener("mousemove", drag);
        document.removeEventListener("mouseup", stopDrag);
    };

    document.addEventListener("mousemove", drag);
    document.addEventListener("mouseup", stopDrag);
}

document.querySelectorAll(".datatable col").forEach((col) => {
    col.addEventListener("mousedown", resizeTableColumn);
});





























