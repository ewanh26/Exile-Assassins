$("#loading").hide();
$("a").on("click", () => {
    let counter = 0;
    $("#loading").fadeIn("fast");
    let ellipsis = () => {
        let counterSwitch = (counter) => ({
            0: () => { $("#msg").html("Making API Requests and Contacting the Database. This may take a while."); },
            1: () => { $("#msg").html("Making API Requests and Contacting the Database. This may take a while.."); },
            2: () => { $("#msg").html("Making API Requests and Contacting the Database. This may take a while..."); }
        })[counter]();
        counterSwitch(counter);
        0 == counter ? counter++ : 1 == counter ? counter++ : counter = 0;
    };
    ellipsis();
    setInterval(ellipsis, 1000);
});
$(window).on("load", () => {
    $("#loading").hide();
});
let selectedMode = $("#mode_selector").find("option:selected").attr("value");
let selectedStat = $("#stat_selector").find("option:selected").attr("value");
let submitBtn = $("#submit");
$("#mode_selector").on("change", () => {
    selectedMode = $("#mode_selector").find("option:selected").attr("value");
});
$("#stat_selector").on("change", () => {
    selectedStat = $("#stat_selector").find("option:selected").attr("value");
});
submitBtn.on("click", () => {
    window.location.replace(`${window.location.origin}/leaderboards/${selectedMode}/${selectedStat}`);
});
//# sourceMappingURL=base.js.map