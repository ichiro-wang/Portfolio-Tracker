import { useEffect, useRef } from "react";

export const useOutsideClick = (
  handler: () => void,
  listenCapture: boolean = true,
) => {
  const ref = useRef<HTMLElement | null>(null);

  useEffect(() => {
    const handleClick = (e: MouseEvent) => {
      if (!ref.current || ref.current?.contains(e.target as Node)) return;
      handler();
    };

    document.addEventListener("click", handleClick, listenCapture);

    return () => document.removeEventListener("click", handleClick);
  }, [handler, listenCapture]);

  return { ref };
};
