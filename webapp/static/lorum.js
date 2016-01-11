var lorum = (function() {
    var my = {};

    function formatToken(token) {
        return '<span title="' + token[1] + "/" + token[2] + '">' + token[0] + '</span>';
    }

    function formatLorum(loremData) {
        var text = "";
        var i;
        var j;
        var nextSpace = false;
        for (i = 0; i < loremData.length; ++i) {
            var sentence = loremData[i];
            for (j = 0; j < sentence.length; ++j) {
                var token = sentence[j];
                var noSpace = token[3];
                var spaceLeft = nextSpace && noSpace !== "left";
                nextSpace = noSpace !== "right";
                if (spaceLeft) {
                    text += " ";
                }
                text += formatToken(token);
            }
        }
        return text;
    }

    my.generate = function() {
        $.ajax("/generate/").done(function(data) {
            var text = formatLorum(data);
            $("#lorumtext").html(text);
        });
    }
    return my;
})();

$(function() {
    lorum.generate();
});
