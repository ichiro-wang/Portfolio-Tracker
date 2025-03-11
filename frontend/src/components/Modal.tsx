import {
  cloneElement,
  createContext,
  ReactElement,
  ReactNode,
  Ref,
  useContext,
  useState,
} from "react";
import { createPortal } from "react-dom";
import { useOutsideClick } from "../hooks/useOutsideClick";

interface ContextProps {
  openName: string;
  open: (name: string) => void;
  close: () => void;
}

const ModalContext = createContext<ContextProps | undefined>(undefined);

interface ModalProps {
  children: ReactNode;
}

// modal that can have several windows
// openName is the name of the Window we want to open
const Modal = ({ children }: ModalProps) => {
  const [openName, setOpenName] = useState<string>("");

  const open = (name: string) => setOpenName(name);
  const close = () => setOpenName("");

  return (
    <ModalContext.Provider value={{ openName, open, close }}>
      {children}
    </ModalContext.Provider>
  );
};

interface OpenProps {
  openName: string;
  children: ReactElement<{ onClick: () => void }>;
}
// children should be a Button
// openName is the name of the window we want to open
const Open = ({ openName, children }: OpenProps) => {
  const context = useContext(ModalContext);
  if (!context) throw new Error("Modal Open used outside Modal");

  const onClick = () => context.open(openName);
  return cloneElement(children, { onClick });
};

interface WindowProps {
  name: string;
  children: ReactElement<{ onCloseModal: () => void }>;
}

const Window = ({ name, children }: WindowProps) => {
  const context = useContext(ModalContext);
  if (!context) throw new Error("Modal Open used outside Modal");

  const { openName, close } = context;
  const { ref } = useOutsideClick(close);

  if (name !== openName) return null;

  return createPortal(
    <div className="fixed inset-0 z-50 flex h-screen w-full items-center justify-center bg-black/50 backdrop-blur-sm transition-all duration-500">
      <div
        ref={ref as Ref<HTMLDivElement>}
        className="rounded-lg bg-white p-8 shadow-lg transition-all duration-500"
      >
        <div>{cloneElement(children, { onCloseModal: close })}</div>
      </div>
    </div>,
    document.body,
  );
};

Modal.Open = Open;
Modal.Window = Window;

export default Modal;
