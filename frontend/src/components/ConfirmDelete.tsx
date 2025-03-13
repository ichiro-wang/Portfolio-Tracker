import Button from "./Button";
import Spinner from "./Spinner";

interface Props {
  resourceName?: string;
  onClick: () => void;
  disabled?: boolean;
  onCloseModal?: () => void;
}

const ConfirmDelete = ({
  resourceName = "resource",
  onClick,
  disabled,
  onCloseModal,
}: Props) => {
  return (
    <>
      <h1 className="mb-3 text-2xl font-semibold">Confirm Delete</h1>
      <p>Are you sure you want to delete this {resourceName}</p>
      <div className="mt-3 flex justify-end gap-2">
        {onCloseModal ? (
          <Button
            className="border border-black bg-white hover:bg-black hover:text-white"
            onClick={onCloseModal}
          >
            Cancel
          </Button>
        ) : null}

        <Button
          onClick={() => {
            onClick();
            onCloseModal?.();
          }}
          disabled={disabled}
        >
          {disabled ? <Spinner /> : "Confirm"}
        </Button>
      </div>
    </>
  );
};

export default ConfirmDelete;
