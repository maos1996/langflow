import { useEffect } from "react";
import { EDIT_TEXT_MODAL_TITLE } from "../../constants/constants";
import { TypeModal } from "../../constants/enums";
import GenericModal from "../../modals/genericModal";
import { TextAreaComponentType } from "../../types/components";
import IconComponent from "../genericIconComponent";
import { Button } from "../ui/button";
import { Input } from "../ui/input";

export default function TextAreaComponent({
  value,
  onChange,
  disabled,
  editNode = false,
  id = "",
}: TextAreaComponentType): JSX.Element {
  // Clear text area
  useEffect(() => {
    if (disabled && value !== "") {
      onChange("", true);
    }
  }, [disabled]);

  return (
    <div className={"flex w-full items-center " + (disabled ? "" : "")}>
      <div className="flex w-full items-center gap-3" data-testid={"div-" + id}>
        <Input
          id={id}
          data-testid={id}
          value={value}
          disabled={disabled}
          className={editNode ? "input-edit-node w-full" : "w-full"}
          placeholder={"Type something..."}
          onChange={(event) => {
            onChange(event.target.value);
          }}
        />
        <div className="flex items-center">
          <GenericModal
            type={TypeModal.TEXT}
            buttonText="Finish Editing"
            modalTitle={EDIT_TEXT_MODAL_TITLE}
            value={value}
            setValue={(value: string) => {
              onChange(value);
            }}
            disabled={disabled}
          >
            {!editNode && (
              <Button unstyled>
                <IconComponent
                  strokeWidth={1.5}
                  id={id}
                  name="ExternalLink"
                  className={
                    "icons-parameters-comp shrink-0" +
                    (disabled ? " text-ring" : " hover:text-accent-foreground")
                  }
                />
              </Button>
            )}
          </GenericModal>
        </div>
      </div>
    </div>
  );
}
