import 'jquery'

function update_ballot_form(raceform) {
    let children = $(raceform.children(".ballot")).children()
    let slugs = [];
    let preview = "";
    for (let i=0; i<children.length; i++){
        slugs[i] = $(children[i]).attr('candidate-slug');
        preview += $(children[i]).children('.candidate-name').text() + "<br/>";
    }
    raceform.children(".preview").html(preview);
    raceform.children("input").val(slugs.join(","));
}

function setup_race_selector() {
    //fixme: Replace candidates selector to initialize this properly for multiple races
    $('.raceform .candidates .candidate').on("click", function (sender) {

        if ($(sender.target).parent().attr('class') === "candidate" && !sender.target.classList.contains("control")) {
            var raceform = $(sender.target).closest(".raceform");
            $(sender.target).parent().detach().appendTo(raceform.children(".ballot"));
            update_ballot_form(raceform);
        }
        return false;
    });

    $('.candidate a.remove').on("click", function (sender) {
        var raceform = $(sender.target).closest(".raceform");
        $(sender.target).parent().detach().appendTo(raceform.children(".candidates"));
        update_ballot_form(raceform);
        return false;
    });

    $('.candidate a.moveup').on("click", function (sender) {
        var raceform = $(sender.target).closest(".raceform");
        let previous = $(sender.target).parent().prev();
        $(sender.target).parent().detach().insertBefore(previous);
        update_ballot_form(raceform);
        return false;
    });

    $('.candidate a.movedown').on("click", function (sender) {
       var raceform = $(sender.target).closest(".raceform");
       let next = $(sender.target).parent().next();
       $(sender.target).parent().detach().insertAfter(next);
       update_ballot_form(raceform);
       return false;
    });

}

setup_race_selector();
window.setup_race_selector = setup_race_selector;
