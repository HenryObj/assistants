import React, { useEffect, useState } from "react";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import {
  DialogActions,
  DialogContent,
  FormControlLabel,
  IconButton,
  Radio,
  RadioGroup,
} from "@mui/material";
import Snackbar from "@mui/material/Snackbar";
import MuiAlert from "@mui/material/Alert";
import EnhancedTable from "./ModalTable";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { updateAssistant } from "../redux/assistantSlice";

const NewIcon = (props) => (
  <svg
    {...props}
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      d="M19 9.5L12 16.5L5 9.5"
      stroke="white"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

const Alert = React.forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

const SelectAssistantComponet = ({
  assistantSelected,
  dispatch,
  assistantList,
  setAllMessageList,
  getLastThreadId,
  fetchData,
}) => {
  const [openDialog, setOpenDialog] = useState(false);
  const [step, setStep] = useState(1);
  const [newAssistantName, setNewAssistantName] = useState("");
  const [instruction, setInstruction] = useState("");
  const [selectedValue, setSelectedValue] = useState("gpt-3.5-turbo-1106");
  const [selectedObjects, setSelectedObjects] = useState([]);
  const [newAssistant, setNewAssistant] = useState("");
  const [isValid, setIsValid] = useState(false);
  const [toast, setToast] = useState({
    open: false,
    type: "",
    message: "",
  });
  const [open, setOpen] = React.useState(false);

  const navigate = useNavigate();

  const handleClose = (event, reason) => {
    if (reason === "clickaway") {
      return;
    }
    setToast({
      open: false,
      type: "",
      message: "",
    });
  };

  const handleCheckboxChange = (event) => {
    setSelectedValue(event.target.value);
  };

  const handleChange = (event) => {
    navigate("/");
    dispatch(updateAssistant(event.target.value));
    if (event.target.value) {
      getLastThreadId(event.target.value);
    }
    setAllMessageList([]);
  };

  const handleCreateNewAssistant = () => {
    setOpenDialog(true);
    setStep(1);
  };

  const handleDialogClose = () => {
    setOpenDialog(false);
    setNewAssistantName("");
    setInstruction("");
  };

  const handleSubmit = (data) => {
    if (!newAssistantName.trim() || !instruction.trim()) {
      setToast({
        open: true,
        type: "error",
        message: "Please fill out all required fields.",
      });
      return;
    }
    axios
      .post(`${import.meta.env.VITE_API_URL}create-assistant`, {
        user_id: 1,
        assistant_name: newAssistantName,
        instructions: instruction,
        gpt_model: selectedValue,
      })
      .then((response) => {
        fetchData();
        setNewAssistant(response.data.data);
        setIsValid(false);
        if (data == "close") {
          handleDialogClose();
        }
        if (data == "next") {
          setStep(2);
        }
        setToast({
          open: true,
          type: "success",
          message: "Assistant created successfully",
        });
      })
      .catch((error) => {
        handleDialogClose();
        setToast({
          open: true,
          type: "error",
          message: error.message,
        });
      });
  };

  const handleAttachFile = () => {
    if (!newAssistantName.trim()) {
      setToast({
        open: true,
        type: "error",
        message: "Please create assitant first",
      });
      return;
    }
    const fileIds = selectedObjects?.map((item) => item?.file_id);
    axios
      .post(
        `${
          import.meta.env.VITE_API_URL
        }attach-files-to-assistant?assistant_id=${newAssistant}`,
        fileIds
      )
      .then((response) => {
        handleDialogClose();
        setToast({
          open: true,
          type: "success",
          message: "File attached successfully",
        });
      })
      .catch((error) => {
        handleDialogClose();
      });
  };

  const checkValidation = () => {
    if (newAssistantName && instruction) {
      setIsValid(true);
    }
  };

  return (
    <div>
      <Snackbar
        open={toast.open}
        autoHideDuration={2000}
        onClose={handleClose}
        anchorOrigin={{ vertical: "top", horizontal: "right" }}
      >
        <Alert onClose={handleClose} severity={toast.type}>
          {toast.message}
        </Alert>
      </Snackbar>
      <Select
        fullWidth
        id="demo-simple-select"
        value={assistantSelected ? assistantSelected : 0}
        defaultValue=""
        onChange={handleChange}
        IconComponent={NewIcon}
        sx={{
          color: "#ffffff",
          fontFamily: "inter",
          fontSize: "18px",
          paddingLeft: 2,
          "& .MuiSelect-icon": { top: 18, right: 20 },
          borderRadius: "10px",
          boxShadow: "none",
          ".MuiOutlinedInput-notchedOutline": { border: 0 },
          "&.MuiOutlinedInput-root:hover .MuiOutlinedInput-notchedOutline": {
            border: 0,
          },
          "&.MuiOutlinedInput-root.Mui-focused .MuiOutlinedInput-notchedOutline":
            {
              border: 0,
            },
        }}
      >
        {assistantList?.map((item, index) => (
          <MenuItem key={index} value={item.id}>
            {item.name}
          </MenuItem>
        ))}

        <MenuItem value={0} onClick={handleCreateNewAssistant}>
          <div className="flex">
            <span className="mr-2">Create new assistant </span>
            <svg
              width={24}
              height={24}
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M8 12H16"
                stroke="white"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M12 16V8"
                stroke="white"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M9 22H15C20 22 22 20 22 15V9C22 4 20 2 15 2H9C4 2 2 4 2 9V15C2 20 4 22 9 22Z"
                stroke="white"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </div>
        </MenuItem>
      </Select>

      {/* Dialog for adding new assistant */}
      <Dialog
        open={openDialog}
        onClose={handleDialogClose}
        maxWidth={"md"}
        fullWidth
        sx={{
          position: "absolute",
          top: 0,
          left: 300,
          backgroundColor: "transparent",
          "& .MuiDialog-container .css-rnmm7m-MuiPaper-root-MuiDialog-paper": {
            borderRadius: "15px",
          },
        }}
      >
        <div>
          <DialogTitle
            sx={{ m: 0, p: 2 }}
            id="customized-dialog-title"
            className="flex justify-between"
          >
            <div className="flex gap-8 items-center font-DM_Sans">
              <span className="text-lg font-bold">New Assistant</span>
              <span
                onClick={() => setStep(1)}
                className={
                  step == 1
                    ? "text-base rounded-lg font-medium text-[#fff] bg-[#00ACCB] p-2 px-4 cursor-pointer"
                    : "cursor-pointer text-base rounded-lg font-semibold text-[#111] p-2 px-4"
                }
              >
                General
              </span>
              <svg
                width={16}
                height={16}
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M8.91001 20.67C8.72001 20.67 8.53001 20.6 8.38001 20.45C8.09001 20.16 8.09001 19.68 8.38001 19.39L14.9 12.87C15.38 12.39 15.38 11.61 14.9 11.13L8.38001 4.61002C8.09001 4.32002 8.09001 3.84002 8.38001 3.55002C8.67001 3.26002 9.15001 3.26002 9.44001 3.55002L15.96 10.07C16.47 10.58 16.76 11.27 16.76 12C16.76 12.73 16.48 13.42 15.96 13.93L9.44001 20.45C9.29001 20.59 9.10001 20.67 8.91001 20.67Z"
                  fill="#171717"
                />
              </svg>
              <span
                onClick={() => newAssistantName && setStep(2)}
                className={
                  step == 2
                    ? "cursor-pointer text-base font-bold text-[#fff] bg-[#00ACCB] p-2 px-4 rounded-lg "
                    : "cursor-pointer text-base font-bold"
                }
              >
                Attach files
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
          {step == 1 && (
            <DialogContent className="grid gap-8 font-inter">
              <div className="flex gap-2 items-center">
                <label className="min-w-[80px]">Name</label>
                <div className="w-full">
                  <input
                    id="question"
                    name="question"
                    type="text"
                    autoComplete="question"
                    value={newAssistantName}
                    maxLength={30}
                    onChange={(e) => {
                      setNewAssistantName(e.target.value);
                      checkValidation();
                    }}
                    placeholder="Enter assistant name"
                    className="w-full text-base font-medium rounded-[10px] border-0 p-2 pr-10 text-gray-100 shadow-sm ring-1 ring-inset ring-gray-100 placeholder:text-gray-100"
                  />
                  {/* <p className="text-[red]">{error?.message}</p> */}
                </div>
              </div>
              <div className="flex items-center gap-12">
                <div>Model</div>
                <RadioGroup
                  value={selectedValue}
                  onChange={handleCheckboxChange}
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
                  id="prompt"
                  name="prompt"
                  type="text"
                  autoComplete="prompt"
                  rows={6}
                  value={instruction}
                  placeholder="Please type here .."
                  onChange={(e) => {
                    setInstruction(e.target.value);
                    checkValidation();
                  }}
                  className="w-full mt-5 text-base font-medium rounded-[10px] border-0 p-3 pr-10 text-gray-100 shadow-sm ring-1 ring-inset ring-gray-100 placeholder:text-gray-100"
                />
              </div>
            </DialogContent>
          )}
          {step == 2 && (
            <DialogContent className="grid gap-2">
              <EnhancedTable
                selectedObjects={selectedObjects}
                setSelectedObjects={setSelectedObjects}
              />
            </DialogContent>
          )}
          <DialogActions>
            {step == 1 ? (
              <>
                <button
                  onClick={() => handleSubmit("close")}
                  className="py-1 px-2 my-2 rounded-lg border mr-4 text-white text-sm bg-button-hover-green hover:bg-[#52D1A9] font-inter"
                >
                  Save and close
                </button>
                <button
                  onClick={() => {
                    handleSubmit("next");
                  }}
                  className={
                    "py-1 px-2 mr-4 rounded-lg border text-white text-sm bg-button-hover-green hover:bg-[#52D1A9] font-inter"
                  }
                >
                  Attach files
                </button>
              </>
            ) : (
              <button
                onClick={handleAttachFile}
                className="py-1 px-2 my-2 rounded-lg border mr-4 text-[#A9ACB4] text-sm hover:bg-button-hover-green hover:text-white font-inter"
              >
                Save
              </button>
            )}
          </DialogActions>
        </div>
      </Dialog>
    </div>
  );
};

export default SelectAssistantComponet;
