var lorum = (function() {
    var my = {};

    function formatToken(token) {
        return '<span>' + token[0] + '</span>';
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

var lorumNav = (function() {
    var my = {};
    var openSectionId = null;
    
    function collapseSection(section) {
        openSectionId = null;
        $(".collapsible-header li[data-section='" + section + "']")
            .removeClass("collapsible-header-open")
            .addClass("collapsible-header-closed");
        $(".collapsible-section[data-section='" + section + "']").hide("fast");
        $(".collapsible-close-button").hide("fast");
    }

    function openSection(section) {
        openSectionId = section;
        $(".collapsible-header li[data-section='" + section + "']")
            .removeClass("collapsible-header-closed")
            .addClass("collapsible-header-open");
        $(".collapsible-section[data-section='" + section + "']").show("fast");
        $(".collapsible-close-button").show("fast");
    }

    function bindCollapsible(index, item) {
        var toggleHandler = function(event) {
            collapseOpenSection();
            openSection($(item).attr("data-section"));
        };
        $(item).click(toggleHandler);
    }

    function collapseOpenSection() {
        if (openSectionId) {
            collapseSection(openSectionId);
        }
        $(".collapsible-close-button").hide();
    }

    my.init = function() {
        $(".collapsible-section").hide();
        $(".collapsible-header li").each(bindCollapsible);
        $(".collapsible-close-button").click(collapseOpenSection)
    };

    return my;
})();

$(function() {
    lorumNav.init();
    var target = "#lorumtext";
    $("#more").click(function() {
        lorum.addGeneratedTextToTarget(target, false).then(function() {
            lorum.highlightLastPara(target);
        });
    });
    lorum.addGeneratedTextToTarget(target, true);
});
