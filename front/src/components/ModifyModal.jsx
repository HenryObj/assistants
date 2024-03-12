import {
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControlLabel,
  Radio,
  RadioGroup,
} from "@mui/material";
import React, { useEffect } from "react";
import EnhancedTable from "./ModalTable";
import { useState } from "react";
import axios from "axios";

const ModifyModal = ({
  openDialog,
  setOpenDialog,
  modifyModalData,
  assistant,
  fetchData,
  setLoading,
  loading,
  setToast,
}) => {
  const [assistantData, setAssistantData] = useState({
    name: "",
    model: "",
    instructions: "",
  });
  // const [loading, setLoading] = useState(false);
  const [selectedObjects, setSelectedObjects] = useState([]);
  const [assistantAttachFileList, setAssistantAttachFileList] = useState([]);

  useEffect(() => {
    const fetchAssistantData = async () => {
      setLoading(true);
      try {
        const response = await axios.get(
          `${
            import.meta.env.VITE_API_URL
          }get-assistant-details?assistant_id=${assistant}`
        );
        setAssistantData(response.data.data);
        setLoading(false);
      } catch (error) {
        setLoading(false);
        console.error("Error fetching data:", error);
      }
    };

    // Call the fetch function
    fetchAssistantData();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    // Update the data state with the changed value
    setAssistantData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleDialogClose = () => {
    setOpenDialog(false);
  };

  const handleSubmit = () => {
    if (modifyModalData == "Modify Parameter") {
      axios
        .post(`${import.meta.env.VITE_API_URL}edit-assistant`, {
          user_id: 1,
          assistant_id: assistant,
          name: assistantData.name,
          model: assistantData.model,
          instructions: assistantData.instructions,
        })
        .then((response) => {
          handleDialogClose();
          fetchData();
        })
        .catch((error) => {
          handleDialogClose();
        });
    }

    if (modifyModalData == "Modify Attachment") {
      if (selectedObjects?.length > 20) {
        setToast({
          open: true,
          type: "error",
          message: "Maximum 20 file you attach",
        });
        return;
      }
      setLoading(true);
      const attachFileList = selectedObjects
        ?.filter(
          (modifiedFile) =>
            !assistantAttachFileList?.some(
              (assistantFile) =>
                (assistantFile?.id || assistantFile?.file_id) ===
                (modifiedFile?.file_id || modifiedFile?.id)
            )
        )
        .map((file) => file?.file_id || file?.id);

      const detachFileList = assistantAttachFileList
        ?.filter(
          (assistantFile) =>
            !selectedObjects?.some(
              (modifiedFile) =>
                (modifiedFile?.file_id || modifiedFile?.id) ===
                (assistantFile?.id || assistantFile?.file_id)
            )
        )
        .map((file) => file?.file_id || file?.id);

      axios
        .post(`${import.meta.env.VITE_API_URL}modify-assistant-files`, {
          assistant_id: assistant,
          attach_file_ids: attachFileList ? attachFileList : [],
          detach_file_ids: detachFileList ? detachFileList : [],
        })
        .then((response) => {
          setLoading(false);
          handleDialogClose();
        })
        .catch((error) => {
          console.log(error);
          setLoading(false);
          handleDialogClose();
        });
    }
  };
  return (
    <div>
      <Dialog
        open={openDialog}
        onClose={handleDialogClose}
        maxWidth={"md"}
        fullWidth
        sx={{
          position: "absolute",
          top: 0,
          left: 300,
          fontFamily: "Inter",
        }}
      >
        <div>
          {loading && (
            <div className="absolute top-2/4 right-2/4 translate-x-[-50%] translate-y-[-50%] z-50">
              <CircularProgress />
            </div>
          )}

          <DialogTitle
            sx={{ m: 0, p: 2 }}
            id="customized-dialog-title"
            className="flex justify-between"
          >
            <div className="flex gap-2 items-center">
              <span className="text-xl font-bold font-DM_Sans">
                {modifyModalData}
              </span>
            </div>
            <div onClick={handleDialogClose} className="cursor-pointer">
              <svg
                width={25}
                height={25}
                viewBox="0 0 41 37"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M29.8958 10.0208L11.1042 26.9791M11.1042 10.0208L29.8958 26.9791"
                  stroke="#A9ACB4"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                />
              </svg>
            </div>
          </DialogTitle>
          {modifyModalData == "Modify Parameter" && (
            <DialogContent className="grid gap-8">
              <div className="flex gap-2 items-center">
                <label className="min-w-[80px]">Edit Name</label>
                <input
                  id="name"
                  name="name"
                  type="text"
                  autoComplete="name"
                  value={assistantData?.name}
                  placeholder="Enter assistant name"
                  onChange={handleInputChange}
                  className="w-full text-base font-medium rounded-[10px] border-0 p-2 pr-10 text-gray-100 shadow-sm ring-1 ring-inset ring-gray-100 placeholder:text-gray-100"
                />
              </div>
              <div className="flex items-center gap-12">
                <div>Model</div>
                <RadioGroup
                  value={assistantData?.model}
                  name="model"
                  onChange={handleInputChange}
                >
                  <div className="flex">
                    <FormControlLabel
                      value="gpt-3.5-turbo-1106"
                      control={<Radio />}
                      label="GPT 3.5"
                    />
                    <FormControlLabel
                      value="gpt-4-1106-preview"
                      control={<Radio />}
                      label="GPT 4"
                    />
                  </div>
                </RadioGroup>
              </div>
              <div>
                <span>Instructions</span>
                <textarea
                  id="instructions"
                  name="instructions"
                  type="text"
                  autoComplete="instructions"
                  rows={6}
                  value={assistantData?.instructions}
                  placeholder="Please type here .."
                  onChange={handleInputChange}
                  className="w-full mt-5 text-base font-medium rounded-[10px] border-0 p-3 pr-10 text-gray-100 shadow-sm ring-1 ring-inset ring-gray-100 placeholder:text-gray-100"
                />
              </div>
            </DialogContent>
          )}
          {modifyModalData == "Modify Attachment" && (
            <>
              <DialogContent className="grid gap-2">
                <EnhancedTable
                  setToast={setToast}
                  assistant={assistant}
                  selectedObjects={selectedObjects}
                  setSelectedObjects={setSelectedObjects}
                  setAssistantAttachFileList={setAssistantAttachFileList}
                />
              </DialogContent>
            </>
          )}
          <DialogActions>
            <button
              onClick={handleSubmit}
              className="py-1 px-2 my-2 rounded-lg border mr-4text-sm bg-button-hover-green hover:bg-[#52D1A9] text-white"
            >
              Save
            </button>
          </DialogActions>
        </div>
      </Dialog>
    </div>
  );
};

export default ModifyModal;
