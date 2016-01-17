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

    function generate(withInitSentence) {
        var deferred = $.Deferred();
        var url = "/generate/";
        if (withInitSentence) {
            url += "init/";
        }
        $.ajax(url).then(function(data) {
            var text = formatLorum(data);
            deferred.resolve(text);
        });
        return deferred.promise();
    }

    my.addGeneratedTextToTarget = function(trg_spec, withInitSentence) {
        var trg = $(trg_spec);
        var deferred = $.Deferred();
        generate(withInitSentence).then(function(text) {
            trg.append("<p>" + text + "</p>");
            deferred.resolve();
        });
        return deferred.promise();
    };

    my.highlightLastPara = function(parent_spec) {
        var para = parent_spec + " p:last-child";
        setTimeout(function() {
            $(para).addClass("highlighted");
        }, 0);
        window.scrollTo(0, document.body.scrollHeight);
        setTimeout(function() {
            $(para).removeClass("highlighted");
        }, 500);
    }

    return my;
})();

$(function() {
    var target = "#lorumtext";
    $("#more").click(function() {
        lorum.addGeneratedTextToTarget(target, false).then(function() {
            lorum.highlightLastPara(target);
        });
    });
    lorum.addGeneratedTextToTarget(target, true);
});
