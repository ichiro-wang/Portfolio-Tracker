import {
  createContext,
  Dispatch,
  MouseEvent,
  ReactNode,
  Ref,
  SetStateAction,
  useContext,
  useEffect,
  useState,
} from "react";
import { HiEllipsisVertical } from "react-icons/hi2";
import { useOutsideClick } from "../hooks/useOutsideClick";
import { createPortal } from "react-dom";

type PositionType = {
  x: number;
  y: number;
} | null;

interface MenusContextProps {
  openId: number;
  open: Dispatch<SetStateAction<number>>;
  close: () => void;
  position: PositionType;
  setPosition: Dispatch<SetStateAction<PositionType>>;
}

const MenusContext = createContext<MenusContextProps | undefined>(undefined);

interface MenusProps {
  children: ReactNode;
}

const Menus = ({ children }: MenusProps) => {
  const [openId, setOpenId] = useState<number>(-1);
  const [position, setPosition] = useState<PositionType>(null);

  const close = () => setOpenId(-1);
  const open = setOpenId;

  return (
    <MenusContext.Provider
      value={{ openId, open, close, position, setPosition }}
    >
      {children}
    </MenusContext.Provider>
  );
};

interface MenuProps {
  children: ReactNode;
}

const Menu = ({ children }: MenuProps) => {
  const context = useContext(MenusContext);
  if (!context) {
    throw new Error("Menu not used in Menus component");
  }

  return <div className="flex items-center justify-end">{children}</div>;
};

interface ToggleProps {
  id: number;
}

const Toggle = ({ id }: ToggleProps) => {
  const context = useContext(MenusContext);
  if (!context) {
    throw new Error("Toggle not used in Menus component");
  }
  const { openId, open, close, setPosition } = context;

  const handleClick = (e: MouseEvent<HTMLDivElement>) => {
    e.stopPropagation();
    const rect = e.currentTarget.getBoundingClientRect();
    if (openId === -1 || openId !== id) {
      open(id);
      setPosition({
        x: window.innerWidth - rect.width - rect.x + 20,
        y: rect.y + rect.height - 16,
      });
    } else {
      close();
      setPosition(null);
    }
  };

  return (
    <div
      className={`button-${id} rounded-full p-[0.15rem] hover:cursor-pointer hover:bg-zinc-300`}
      onClick={handleClick}
    >
      <HiEllipsisVertical />
    </div>
  );
};

interface ListProps {
  id: number;
  children: ReactNode;
}

const List = ({ id, children }: ListProps) => {
  const context = useContext(MenusContext);
  if (!context) {
    throw new Error("List not used in Menus component");
  }
  const { openId, position, close } = context;

  const { ref } = useOutsideClick(close, false);

  useEffect(() => {
    window.addEventListener("scroll", close);

    return () => window.removeEventListener("scroll", close);
  }, [close]);

  if (openId !== id) return null;

  return createPortal(
    <div
      className="fixed rounded-md border bg-white"
      style={{ top: position?.y, right: position?.x }}
      ref={ref as Ref<HTMLDivElement>}
    >
      {children}
    </div>,
    document.body,
  );
};

interface ButtonProps {
  icon: ReactNode;
  onClick?: () => void;
  children: ReactNode;
}

const Button = ({ icon, onClick, children }: ButtonProps) => {
  const context = useContext(MenusContext);
  if (!context) {
    throw new Error("Button not used in Menus component");
  }

  const handleClick = () => {
    onClick?.();
    context.close();
  };

  return (
    <button
      className="flex w-full items-center justify-start gap-2 px-3 py-2 hover:bg-zinc-200 [&:not(:last-child)]:border-b"
      onClick={handleClick}
    >
      {icon}
      <span>{children}</span>
    </button>
  );
};

Menus.Menu = Menu;
Menus.Toggle = Toggle;
Menus.List = List;
Menus.Button = Button;

export default Menus;
