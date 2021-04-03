$("#loading").hide();
$("a").on("click", () => {
    let counter: number = 0;
    $("#loading").fadeIn("fast");
    let ellipsis = () => {
        let counterSwitch = (counter: number) => ({
            0: () => {$("#msg").html("Making API Requests and Contacting the Database. This may take a while.")},
            1: () => {$("#msg").html("Making API Requests and Contacting the Database. This may take a while..")},
            2: () => {$("#msg").html("Making API Requests and Contacting the Database. This may take a while...")}
        })[counter]();
        counterSwitch(counter);
        0 == counter ? counter++ : 1 == counter ? counter++ : counter = 0;
    };
    ellipsis();
    setInterval(ellipsis, 1000);
});
$(window).on("load", () => {
    $("#loading").hide()
});

let selectedMode: string = $("#mode_selector").find("option:selected").attr("value");
let selectedStat: string = $("#stat_selector").find("option:selected").attr("value");
let submitBtn: JQuery<HTMLElement> = $("#submit");
$("#mode_selector").on("change", () => {
    selectedMode = $("#mode_selector").find("option:selected").attr("value");
});
$("#stat_selector").on("change", () => {
    selectedStat = $("#stat_selector").find("option:selected").attr("value");
});
submitBtn.on("click", () => {
    window.location.replace(`${window.location.origin}/leaderboards/${selectedMode}/${selectedStat}`)
})