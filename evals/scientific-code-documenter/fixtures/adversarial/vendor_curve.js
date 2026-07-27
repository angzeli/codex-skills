// Vendored synthetic interpolation helper. Do not edit during skill evaluation.
(function (globalScope) {
  function linearPoint(left, right, fraction) {
    return left + (right - left) * fraction;
  }

  globalScope.syntheticCurve = {
    linearPoint: linearPoint,
    version: "1.0.0-synthetic"
  };
}(typeof globalThis === "undefined" ? this : globalThis));
