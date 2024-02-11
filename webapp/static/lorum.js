const SHOW_DONATION_BANNER_AFTER_N_MORE = 3;
const HIDE_CONTROL_FOR_SECS = 10;

const lorum = (function () {
  const my = {};

  function formatLorum(loremData) {
    let text = "";
    let i;
    let j;
    let nextSpace = false;
    for (i = 0; i < loremData.length; ++i) {
      const sentence = loremData[i];
      for (j = 0; j < sentence.length; ++j) {
        const token = sentence[j];
        const noSpace = token[3];
        const spaceLeft = nextSpace && noSpace !== "left";
        nextSpace = noSpace !== "right";
        if (spaceLeft) {
          text += " ";
        }
        text += token[0];
      }
    }
    return text;
  }

  function generate(withInitSentence) {
    const deferred = $.Deferred();
    let url = "/generate/";
    if (withInitSentence) {
      url += "init/";
    }
    $.ajax(url).then(function (data) {
      const text = formatLorum(data);
      deferred.resolve(text);
    });
    return deferred.promise();
  }

  my.addGeneratedTextToTarget = function (trg_spec, withInitSentence) {
    const trg = $(trg_spec);
    const deferred = $.Deferred();
    generate(withInitSentence).then(function (text) {
      trg.append("<p>" + text + "</p>");
      deferred.resolve();
    });
    return deferred.promise();
  };

  my.highlightLastPara = function (parent_spec) {
    const para = parent_spec + " p:last-child";
    setTimeout(function () {
      $(para).addClass("highlighted");
    }, 0);
    window.scrollTo(0, document.body.scrollHeight);
    setTimeout(function () {
      $(para).removeClass("highlighted");
    }, 500);
  };

  let numMoreClicked = 0;

  my.handleMore = (trg_spec) => {
    ++numMoreClicked;
    smartlook("track", "more", {
      numMoreClicked,
    });
    if ((numMoreClicked + 1) % SHOW_DONATION_BANNER_AFTER_N_MORE == 0) {
      showDonationBanner(trg_spec);
    } else {
      lorum.addGeneratedTextToTarget(trg_spec, false).then(function () {
        lorum.highlightLastPara(trg_spec);
      });
    }
  };

  let donationBannerOrd = 0;

  function showDonationBanner(trg_spec) {
    smartlook("target", "show_donation_banner", {});
    hideControlTemporarily();
    const bannerId = `donation-banner-clone-${donationBannerOrd}`;
    const clone = $("#donation-banner-master").clone().prop("id", bannerId);
    const target = $(trg_spec);
    target.append(clone);
    $(`#${bannerId} .donation-button`).click(() => {
      smartlook("target", "donation_clicked", {
        bannerOrd: donationBannerOrd,
      });
    });
    ++donationBannerOrd;
    window.scrollTo(0, document.body.scrollHeight);
  }

  function hideControlTemporarily() {
    $("#control").hide(0);
    $("#progress").show();
    setTimeout(() => {
      $("#progress").hide();
      $("#control").show();
      window.scrollTo(0, document.body.scrollHeight);
    }, HIDE_CONTROL_FOR_SECS * 1000);
  }

  return my;
})();

var lorumNav = (function () {
  const my = {};
  let openSectionId = null;

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
    const toggleHandler = function (event) {
      collapseOpenSection();
      openSection($(item).attr("data-section"));
    };
    $(item).click(toggleHandler);
    $(item).addClass("collapsible-header-closed");
  }

  function collapseOpenSection() {
    if (openSectionId) {
      collapseSection(openSectionId);
    }
    $(".collapsible-close-button").hide();
  }

  my.init = function () {
    $(".collapsible-section").hide();
    $(".collapsible-header li").each(bindCollapsible);
    $(".collapsible-close-button").click(collapseOpenSection);
  };

  return my;
})();

$(function () {
  smartlook("track", "init");
  lorumNav.init();
  const target = "#lorumtext";
  $("#more").click(function () {
    lorum.handleMore(target);
  });
  lorum.addGeneratedTextToTarget(target, true);
});
