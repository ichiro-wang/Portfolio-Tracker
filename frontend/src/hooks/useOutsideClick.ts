import { useEffect, useRef } from "react";

export const useOutsideClick = (
  handler: () => void,
  listenCapture: boolean = true,
) => {
  const ref = useRef<HTMLElement | null>(null);

  useEffect(() => {
    // click outside modal
    const handleClick = (e: MouseEvent) => {
      if (!ref.current || ref.current?.contains(e.target as Node)) return;
      handler();
    };

    // user presses escape
    const handleEsc = (e: globalThis.KeyboardEvent) => {
      if (e.key === "Escape") {
        handler();
      }
    };

    document.addEventListener("click", handleClick, listenCapture);
    document.addEventListener("keydown", handleEsc);

    return () => {
      document.removeEventListener("click", handleClick);
      document.removeEventListener("keydown", handleEsc);
    };
  }, [handler, listenCapture]);

  return { ref };
};
