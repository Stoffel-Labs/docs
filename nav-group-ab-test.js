(function () {
  var TEST_NAME = "backend_nav_group_name";
  var STORAGE_KEY = "stoffel:" + TEST_NAME;
  var CONTROL_LABEL = "MPC Backends";
  var VARIANT_LABEL = "Privacy Backends";
  var labels = [CONTROL_LABEL, VARIANT_LABEL];

  function getVariant() {
    try {
      var existing = window.localStorage && window.localStorage.getItem(STORAGE_KEY);
      if (existing === "mpc_backends" || existing === "privacy_backends") {
        return existing;
      }
      var next = Math.random() < 0.5 ? "mpc_backends" : "privacy_backends";
      if (window.localStorage) {
        window.localStorage.setItem(STORAGE_KEY, next);
      }
      return next;
    } catch (_) {
      return Math.random() < 0.5 ? "mpc_backends" : "privacy_backends";
    }
  }

  var variant = getVariant();
  var label = variant === "privacy_backends" ? VARIANT_LABEL : CONTROL_LABEL;
  var lastExposurePath = null;

  function maybeCaptureExposure() {
    var path = window.location.pathname;
    if (lastExposurePath === path) {
      return;
    }
    lastExposurePath = path;

    if (window.posthog && typeof window.posthog.capture === "function") {
      window.posthog.capture("docs_nav_group_label_exposure", {
        test_name: TEST_NAME,
        variant: variant,
        group_label: label,
        path: path
      });
    }
  }

  function rewriteLabel() {
    var didRewrite = false;
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    var node;
    while ((node = walker.nextNode())) {
      var text = node.nodeValue && node.nodeValue.trim();
      if (labels.indexOf(text) !== -1 && node.nodeValue !== label) {
        node.nodeValue = node.nodeValue.replace(text, label);
        didRewrite = true;
      } else if (text === label) {
        didRewrite = true;
      }
    }

    if (didRewrite) {
      maybeCaptureExposure();
    }
  }

  function scheduleRewrite() {
    window.requestAnimationFrame(rewriteLabel);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", scheduleRewrite);
  } else {
    scheduleRewrite();
  }

  var observer = new MutationObserver(scheduleRewrite);
  observer.observe(document.documentElement, {
    childList: true,
    subtree: true,
    characterData: true
  });

  var lastPath = window.location.pathname;
  window.setInterval(function () {
    if (window.location.pathname !== lastPath) {
      lastPath = window.location.pathname;
      scheduleRewrite();
    }
  }, 500);
})();
