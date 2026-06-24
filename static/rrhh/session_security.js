(function () {
  const config = window.RRHH_SECURITY || {};
  const timeoutSeconds = Number(config.idleTimeoutSeconds || 1800);
  const loginUrl = config.loginUrl || "/login/";
  const logoutUrl = config.logoutUrl || "/logout/";
  const lastActivityKey = "elCarmenRrhh:lastActivity";
  const logoutKey = "elCarmenRrhh:logoutAt";
  const warningKey = "elCarmenRrhh:timeoutWarningShown";
  const timeoutMs = timeoutSeconds * 1000;
  const warningMs = Math.min(120000, Math.max(30000, timeoutMs / 5));
  let isLoggingOut = false;

  function now() {
    return Date.now();
  }

  function setLastActivity() {
    localStorage.setItem(lastActivityKey, String(now()));
    localStorage.removeItem(warningKey);
  }

  function getLastActivity() {
    const stored = Number(localStorage.getItem(lastActivityKey));
    if (!stored) {
      setLastActivity();
      return now();
    }
    return stored;
  }

  function broadcastLogout() {
    localStorage.setItem(logoutKey, String(now()));
  }

  function goToLogin() {
    if (window.location.pathname !== loginUrl) {
      window.location.href = loginUrl;
    }
  }

  function logoutEverywhere(reason) {
    if (isLoggingOut) {
      return;
    }
    isLoggingOut = true;
    broadcastLogout();
    const separator = logoutUrl.indexOf("?") === -1 ? "?" : "&";
    window.location.href = logoutUrl + separator + "motivo=" + encodeURIComponent(reason || "manual");
  }

  function checkIdleTimeout() {
    const elapsed = now() - getLastActivity();
    if (elapsed >= timeoutMs) {
      logoutEverywhere("inactividad");
      return;
    }

    if (elapsed >= timeoutMs - warningMs && !localStorage.getItem(warningKey)) {
      localStorage.setItem(warningKey, "1");
      const minutes = Math.max(1, Math.ceil((timeoutMs - elapsed) / 60000));
      if (window.bootstrap && document.getElementById("sessionWarningToast")) {
        document.getElementById("sessionWarningText").textContent =
          "La sesion se cerrara por inactividad en aproximadamente " + minutes + " minuto(s).";
        window.bootstrap.Toast.getOrCreateInstance(document.getElementById("sessionWarningToast")).show();
      }
    }
  }

  ["click", "keydown", "mousemove", "scroll", "touchstart"].forEach(function (eventName) {
    window.addEventListener(eventName, setLastActivity, { passive: true });
  });

  document.addEventListener("click", function (event) {
    const logoutLink = event.target.closest("[data-global-logout]");
    if (!logoutLink) {
      return;
    }
    event.preventDefault();
    logoutEverywhere("manual");
  });

  window.addEventListener("storage", function (event) {
    if (event.key === logoutKey && event.newValue) {
      goToLogin();
    }
  });

  setLastActivity();
  window.setInterval(checkIdleTimeout, 10000);
})();
