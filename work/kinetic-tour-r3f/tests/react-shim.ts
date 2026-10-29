// Real ESM shim so the transpiled app entry can import React through a file:
// URL without depending on Node's CommonJS named-export detection. React ships
// as CJS; importing { lazy } directly from its entry is not guaranteed to
// resolve, and a silent interop failure would look like a broken test.
//
// If the app entry starts importing another React export, add it here: the
// harness fails loudly rather than guessing.
import React from "react";

export default React;

export const {
  Component,
  Suspense,
  lazy,
  useCallback,
  useEffect,
  useRef,
  useState,
} = React;
