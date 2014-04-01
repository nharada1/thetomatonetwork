function runOnLoad() {
    console.log("page ready");
    smallCalendar.render();
    lineChart.render();
}

$(document).ready(runOnLoad);