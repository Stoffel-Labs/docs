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
  var capturedExposurePaths = {};

  function maybeCaptureExposure() {
    var path = window.location.pathname;
    if (capturedExposurePaths[path]) {
      return;
    }
    if (!window.posthog || typeof window.posthog.capture !== "function") {
      return;
    }

    capturedExposurePaths[path] = true;
    window.posthog.capture("docs_nav_group_label_exposure", {
      test_name: TEST_NAME,
      variant: variant,
      group_label: label,
      path: path
    });
  }

  function getRewriteRoots() {
    var roots = Array.prototype.slice.call(document.querySelectorAll("nav, main"));
    return roots.length ? roots : [document.body];
  }

  function rewriteDocumentTitle() {
    labels.forEach(function (existingLabel) {
      if (document.title.indexOf(existingLabel) !== -1) {
        document.title = document.title.replace(existingLabel, label);
      }
    });
  }

  function rewriteLabel() {
    var didRewrite = false;
    rewriteDocumentTitle();
    getRewriteRoots().forEach(function (root) {
      var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
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
    });

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
    } else {
      maybeCaptureExposure();
    }
  }, 500);
})();
