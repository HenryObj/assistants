import React, { useEffect, useState } from "react";
import logo from "../../assets/image/logo.webp";
import History from "../../components/History";
import Message from "../../components/Message";
import SelectAssistantComponet from "../../components/SelectAssistantComponet";
import StickyHeadTable from "../../components/Table";
import LinearProgress, {
  linearProgressClasses,
} from "@mui/material/LinearProgress";
import { styled } from "@mui/material/styles";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import ModifyModal from "../../components/ModifyModal";
import { FaRegFileWord, FaRegStopCircle } from "react-icons/fa";
import { FaRegFilePdf } from "react-icons/fa";
import { FaRegFileExcel } from "react-icons/fa";
import axios from "axios";
import Snackbar from "@mui/material/Snackbar";
import MuiAlert from "@mui/material/Alert";
import Loading from "../../components/Loading";
import { Link, useLocation } from "react-router-dom";
import { CircularProgress } from "@mui/material";
import { useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import { updateAssistant } from "../../redux/assistantSlice";

const Alert = React.forwardRef(function Alert(props, ref) {
  return (
    <MuiAlert
      elevation={6}
      ref={ref}
      variant="filled"
      sx={{
        fontFamily: "Inter",
      }}
      {...props}
    />
  );
});

const BorderLinearProgress = styled(LinearProgress)(({ theme }) => ({
  height: 15,
  border: "1px solid #A9ACB4",
  borderRadius: 15,
  [`&.${linearProgressClasses.colorPrimary}`]: {
    backgroundColor: "#fff",
  },
  [`& .${linearProgressClasses.bar}`]: {
    borderRadius: 5,
    backgroundColor: "#A9ACB4",
  },
}));

const Home = () => {
  const [question, setQuestion] = useState("");
  const [clientDetail, setClientDetail] = useState("");
  const [uploadFile, setUploadFile] = useState(false);
  const [uploadedFileList, setUploadedFileList] = useState([]);
  const [threadList, setThreadList] = useState([]);
  const [allMessageList, setAllMessageList] = useState([]);
  const [assistantList, setAssistantList] = useState([]);
  const [anchorEl, setAnchorEl] = React.useState(null);
  const [modifyModalData, setModifyModalData] = React.useState(null);
  const [openDialog, setOpenDialog] = React.useState(false);
  const [threadId, setThreadId] = React.useState(null);
  const [gptLoading, setGptLoading] = useState(false);
  const [loading, setLoading] = useState(false);
  const [fileStatus, setFileStatus] = useState("");
  const [usedSpace, setUsedSpace] = useState(0); // in MB
  const [totalSpace, setTotalSpace] = useState(100);
  const [usedSpaceMB, setUsedSpaceMB] = useState(0);
  const [isHovered, setIsHovered] = useState(false);
  const [newChatHovered, setNewChatHovered] = useState(false);
  const [apiCalling, setApiCalling] = useState(false);

  const [toast, setToast] = useState({
    open: false,
    type: "",
    message: "",
  });
  const location = useLocation();
  const chatContainerRef = useRef(null);

  const dispatch = useDispatch();
  const assistantSelected = useSelector(updateAssistant).payload.assistant;

  const open = Boolean(anchorEl);
  const handleClick = (event) => {
    if (assistantSelected) {
      setAnchorEl(event.currentTarget);
    } else {
      setToast({
        open: true,
        type: "error",
        message: "Please select assistant",
      });
    }
  };
  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleNewChat = (data) => {
    setAllMessageList([]);
    setThreadId("");
    getThreadList();
  };

  const onMessageSend = () => {
    if (apiCalling) {
      setToast({
        open: true,
        type: "error",
        message: "Please wait for response",
      });
      return;
    }
    if (!assistantSelected) {
      setToast({
        open: true,
        type: "error",
        message: "Please select assistant",
      });
      return;
    }

    if (!question.trim()) {
      setToast({
        open: true,
        type: "error",
        message: "Please enter your question",
      });
      return;
    }
    setApiCalling(true);
    const newMessage = {
      role: "user",
      content: question,
    };
    // Using functional update to ensure the latest state
    setAllMessageList((prevMessages) => {
      if (!prevMessages?.length) {
        // If prevMessages is blank, return a new array with only the newMessage
        return [newMessage];
      }
      // If prevMessages is not blank, concatenate it with the newMessage
      return [...prevMessages, newMessage];
    });
    setGptLoading(true);
    axios
      .post(`${import.meta.env.VITE_API_URL}ask-question`, {
        user_id: "1",
        question: question,
        thread_id: threadId,
        assistant_id: assistantSelected,
      })
      .then((response) => {
        setGptLoading(false);
        setThreadId(response.data.data.thread_id);
        const assistantMessage = {
          role: assistantList?.find((item) => item.id === assistantSelected)
            ?.name,
          content: response.data.data.response[0].message,
        };
        // Using functional update to ensure the latest state
        setAllMessageList((prevMessages) => [
          ...prevMessages,
          assistantMessage,
        ]);
        setApiCalling(false);
      })
      .catch((error) => {
        setGptLoading(false);
        setApiCalling(false);
        // console.log(error);
        // setToast({
        //   open: true,
        //   type: "error",
        //   message: error.message,
        // });
      });
    setQuestion("");
  };

  const fetchData = async () => {
    // debugger;
    setLoading(true);
    try {
      const response = await axios.get(
        `${import.meta.env.VITE_API_URL}assistant-list?client_id=1`
      );

      setAssistantList(response.data?.data?.assistant_details);
      setLoading(false);
      if (assistantSelected) {
        getLastThreadId(assistantSelected);
      } else {
        const selectedAssistantId =
          response.data.data?.assistant_details[
            response.data.data?.assistant_details.length - 1
          ]?.id;
        dispatch(updateAssistant(selectedAssistantId));
        if (selectedAssistantId) {
          await getLastThreadId(selectedAssistantId);
        }
      }
      // if (response.data.data?.assistant_details?.length > 0) {
      //   if (assistant == "") {
      //     const selectedAssistantId =
      //       response.data.data?.assistant_details[
      //         response.data.data?.assistant_details.length - 1
      //       ]?.id;
      //     setAssistant(selectedAssistantId);
      //     if (selectedAssistantId) {
      //       await getLastThreadId(selectedAssistantId);
      //     }
      //   } else {
      //     await getLastThreadId(assistant ? assistant : selectedAssistantId);
      //   }
      // }
    } catch (error) {
      setLoading(false);
    }
  };

  const getThreadList = async () => {
    setLoading(true);
    try {
      const response = await axios.get(
        `${
          import.meta.env.VITE_API_URL
        }get-threads-by-date-with-first-words?user_id=1`
      );
      setThreadList(response.data?.data);
      setLoading(false);
    } catch (error) {
      setLoading(false);
      console.error(error);
    }
  };

  const getClientDetail = async () => {
    setLoading(true);
    try {
      const response = await axios.get(
        `${import.meta.env.VITE_API_URL}get-client-data?client_id=1`
      );
      setClientDetail(response.data?.data);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    getClientDetail();
    fetchData();
    getThreadList();
  }, []); // Empty dependency array to run the effect only once on mount

  const getLastThreadId = async (data) => {
    setLoading(true);
    try {
      const response = await axios.get(
        `${import.meta.env.VITE_API_URL}get-last-thread-id?assistant_id=${data}`
      );
      if (response.data.data) {
        setThreadId(response.data.data[0]);
        getAllMessages(response.data.data);
      } else {
        setThreadId("");
        setLoading(false);
      }
    } catch (error) {
      console.error(error);
      setLoading(false);
      setThreadId("");
    }
  };

  const getAllMessages = (threadid) => {
    setLoading(true);
    axios
      .get(
        `${
          import.meta.env.VITE_API_URL
        }get-all-message-of-thread?thread_id=${threadid}`
      )
      .then((response) => {
        setLoading(false);
        setAllMessageList(response.data.data);
      })
      .catch((error) => {
        setLoading(false);
        setAllMessageList([]);
      });

    setQuestion("");
  };

  const handleSnackClose = (event, reason) => {
    if (reason == "clickaway") {
      return;
    }
    setToast({
      open: false,
      type: "",
      message: "",
    });
  };

  const handleFileInput = (event) => {
    const files = event.target.files;
    handleUploadFile(files);
  };

  const handleUploadFile = async (files) => {
    const formData = new FormData();
    // debugger;
    // Create an array to store file information
    const newFiles = Array.from(files).map((file) => ({
      file_name: file.name,
      file_type: file.type,
      file_size: file.size,
    }));

    // Update uploadedFileList with the newFiles array
    setUploadedFileList((prevSelectedObjects) => [
      ...prevSelectedObjects,
      ...newFiles,
    ]);
    setFileStatus("Uploading");

    // Append each file to FormData
    Array.from(files).forEach((file, index) => {
      formData.append(`files`, file);
    });

    try {
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL}upload-multiple-files?client_id=1`,
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      if (response.data.status == "error") {
        setFileStatus("error");
      } else {
        setFileStatus("Completed");
      }
    } catch (error) {
      setFileStatus("error");
      console.error(error);
    }
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const files = event.dataTransfer.files;
    handleUploadFile(files);
  };

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  }, [gptLoading]);

  return (
    <div className="flex font-inter">
      {loading && (
        <div className="center z-50">
          <CircularProgress />
        </div>
      )}
      <Snackbar
        open={toast.open}
        autoHideDuration={2000}
        onClose={handleSnackClose}
        anchorOrigin={{ vertical: "top", horizontal: "right" }}
      >
        <Alert onClose={handleSnackClose} severity={toast.type}>
          {toast.message}
        </Alert>
      </Snackbar>
      <div className="bg-bg_sidebar-black text-white py-3 w-[360px]">
        <div className="mx-auto px-5">
          <img src={logo} alt="logo" className="obj_fit w-60 h-14 mx-auto" />
        </div>
        <div className="max-h-[87vh] overflow-auto custom-scrollbar">
          <Link to={"/library"}>
            <div
              className={
                location.pathname != "/"
                  ? "mx-5 pl-[10px] pr-[8px] pt-[6px] pb-1 text-lg mt-6 font-medium text-white bg-button-selected-blue rounded-lg cursor-pointer font-DM_Sans"
                  : "mx-5 pl-[10px] pr-[8px] pt-[6px] pb-1 mt-6 text-lg text-white font-medium cursor-pointer font-DM_Sans"
              }
              onClick={() => {
                setUploadFile(false);
              }}
            >
              Library
            </div>
          </Link>
          <div>
            <SelectAssistantComponet
              assistantList={assistantList}
              dispatch={dispatch}
              assistantSelected={assistantSelected}
              setAllMessageList={setAllMessageList}
              getLastThreadId={getLastThreadId}
              fetchData={fetchData}
            />
          </div>
          <div className="grid gap-4 mt-2 px-5">
            <History
              setThreadId={setThreadId}
              threadId={threadId}
              setAssistant={dispatch}
              title="Today"
              data={threadList?.today}
              getAllMessages={getAllMessages}
            />
            <History
              setThreadId={setThreadId}
              setAssistant={dispatch}
              title="Yesterday"
              data={threadList?.yesterday}
              getAllMessages={getAllMessages}
              threadId={threadId}
            />
            <History
              setThreadId={setThreadId}
              setAssistant={dispatch}
              getAllMessages={getAllMessages}
              title="Previous 7 days"
              data={threadList?.previous_7_days}
              threadId={threadId}
            />
            <History
              setThreadId={setThreadId}
              setAssistant={dispatch}
              title="Previous 30 days"
              data={threadList?.previous_30_days}
              getAllMessages={getAllMessages}
              threadId={threadId}
            />
          </div>
        </div>
      </div>
      {location.pathname == "/" && (
        <div className="flex w-full flex-col h-screen gap-1">
          <div className="bg-white p-4 flex justify-between border-b items-center border-b-borders-gray">
            <div
              className="flex gap-2 group items-center cursor-pointer"
              onClick={() => handleNewChat(assistantSelected)}
              onMouseEnter={() => setNewChatHovered(true)}
              onMouseLeave={() => setNewChatHovered(false)}
            >
              {newChatHovered ? (
                <svg
                  width={30}
                  height={30}
                  viewBox="0 0 30 30"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M20 3.99998C19.5926 3.62528 19.0532 3.42747 18.5002 3.44997C17.9471 3.47247 17.4256 3.71343 17.05 4.11998L10.17 11L9 15L13 13.83L19.88 6.99998C20.0888 6.81332 20.2579 6.5866 20.3774 6.33329C20.4968 6.07997 20.5642 5.80524 20.5754 5.5254C20.5866 5.24556 20.5414 4.96632 20.4426 4.70427C20.3437 4.44223 20.1932 4.20272 20 3.99998V3.99998Z"
                    stroke="black"
                    strokeWidth={2}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                  <path
                    d="M12 3H4C3.73478 3 3.48043 3.10536 3.29289 3.29289C3.10536 3.48043 3 3.73478 3 4V20C3 20.2652 3.10536 20.5196 3.29289 20.7071C3.48043 20.8946 3.73478 21 4 21H20C20.2652 21 20.5196 20.8946 20.7071 20.7071C20.8946 20.5196 21 20.2652 21 20V12"
                    stroke="black"
                    strokeWidth={2}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              ) : (
                <svg
                  width={30}
                  height={30}
                  viewBox="0 0 30 30"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <rect width={30} height={30} rx={5} fill="white" />
                  <path
                    d="M20 3.99998C19.5926 3.62528 19.0532 3.42747 18.5002 3.44997C17.9471 3.47247 17.4256 3.71343 17.05 4.11998L10.17 11L9 15L13 13.83L19.88 6.99998C20.0888 6.81332 20.2579 6.5866 20.3774 6.33329C20.4968 6.07997 20.5642 5.80524 20.5754 5.5254C20.5866 5.24556 20.5414 4.96632 20.4426 4.70427C20.3437 4.44223 20.1932 4.20272 20 3.99998V3.99998Z"
                    stroke="#A9ACB4"
                    strokeWidth={2}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                  <path
                    d="M12 3H4C3.73478 3 3.48043 3.10536 3.29289 3.29289C3.10536 3.48043 3 3.73478 3 4V20C3 20.2652 3.10536 20.5196 3.29289 20.7071C3.48043 20.8946 3.73478 21 4 21H20C20.2652 21 20.5196 20.8946 20.7071 20.7071C20.8946 20.5196 21 20.2652 21 20V12"
                    stroke="#A9ACB4"
                    strokeWidth={2}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              )}

              <div className="bg-bg_sidebar-black text-white py-1 px-4 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity">
                New Chat
              </div>
            </div>
            <div
              className={
                anchorEl
                  ? " bg-button-hover-green flex items-center gap-2 p-2 text-white rounded-xl cursor-pointer"
                  : "text-borders-gray flex items-center gap-2 p-2 cursor-pointer"
              }
              aria-controls={open ? "basic-menu" : undefined}
              aria-haspopup="true"
              aria-expanded={open ? "true" : undefined}
              onClick={handleClick}
            >
              <span className="font-medium">
                {
                  assistantList?.find((item) => item.id === assistantSelected)
                    ?.name
                }
              </span>
              <svg
                width={21}
                height={20}
                viewBox="0 0 21 20"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M18.5327 10.975C18.5732 10.6625 18.6002 10.3375 18.6002 10C18.6002 9.6625 18.5732 9.3375 18.5192 9.025L20.8007 7.375C21.0032 7.225 21.0572 6.95 20.9357 6.7375L18.7757 3.275C18.6407 3.05 18.3572 2.975 18.1142 3.05L15.4276 4.05C14.8606 3.65 14.2666 3.325 13.6051 3.075L13.2001 0.425C13.1596 0.175 12.9301 0 12.6601 0H8.33995C8.06994 0 7.85394 0.175 7.81344 0.425L7.40843 3.075C6.74691 3.325 6.1394 3.6625 5.58589 4.05L2.89932 3.05C2.65632 2.9625 2.37281 3.05 2.23781 3.275L0.0777555 6.7375C-0.0572476 6.9625 -0.00324617 7.225 0.212759 7.375L2.49431 9.025C2.44031 9.3375 2.39981 9.675 2.39981 10C2.39981 10.325 2.42681 10.6625 2.48081 10.975L0.199258 12.625C-0.00324649 12.775 -0.0572476 13.05 0.0642552 13.2625L2.22431 16.725C2.35931 16.95 2.64282 17.025 2.88582 16.95L5.57238 15.95C6.1394 16.35 6.73341 16.675 7.39493 16.925L7.79994 19.575C7.85394 19.825 8.06994 20 8.33995 20H12.6601C12.9301 20 13.1596 19.825 13.1866 19.575L13.5916 16.925C14.2531 16.675 14.8606 16.3375 15.4141 15.95L18.1007 16.95C18.3437 17.0375 18.6272 16.95 18.7622 16.725L20.9222 13.2625C21.0572 13.0375 21.0032 12.775 20.7872 12.625L18.5327 10.975ZM10.5 13.75C8.27245 13.75 6.44991 12.0625 6.44991 10C6.44991 7.9375 8.27245 6.25 10.5 6.25C12.7276 6.25 14.5501 7.9375 14.5501 10C14.5501 12.0625 12.7276 13.75 10.5 13.75Z"
                  fill={anchorEl ? "#fff" : "#A9ACB4"}
                />
              </svg>
            </div>
          </div>
          <Menu
            id="basic-menu"
            anchorEl={anchorEl}
            open={open}
            onClose={handleClose}
            MenuListProps={{
              "aria-labelledby": "basic-button",
            }}
            sx={{
              mt: "2px",
              "& .MuiMenu-paper .MuiMenu-list": {
                backgroundColor: "#f5f5f5",
                color: "#111",
              },
              "& .MuiPaper-rounded": {
                borderRadius: "15px",
                backgroundColor: "#f5f5f5",
              },
            }}
          >
            <MenuItem
              onClick={() => {
                setModifyModalData("Modify Parameter");
                setOpenDialog(true);
                handleClose();
              }}
              sx={{
                background: "#f5f5f5",
                "&:hover": {
                  color: "#46BC96 !important",
                  background: "none",
                },
              }}
            >
              Modify Parameters
            </MenuItem>
            <MenuItem
              onClick={() => {
                setModifyModalData("Modify Attachment");
                setOpenDialog(true);
                handleClose();
              }}
              sx={{
                "&:hover": {
                  color: "#46BC96 !important",
                  background: "none",
                },
              }}
            >
              Modify Attachments
            </MenuItem>
          </Menu>

          {/* Dialog for modify assistant */}
          {openDialog && (
            <ModifyModal
              assistant={assistantSelected}
              openDialog={openDialog}
              setOpenDialog={setOpenDialog}
              modifyModalData={modifyModalData}
              setToast={setToast}
              fetchData={fetchData}
              setLoading={setLoading}
              loading={loading}
            />
          )}

          <div
            ref={chatContainerRef}
            className="flex-grow gap-4 flex flex-col overflow-y-auto chat custom-scrollbar py-1 px-10 w-full md:max-w-3xl lg:max-w-[40rem] xl:max-w-[48rem] mx-auto"
          >
            {allMessageList?.map((item, index) => (
              <Message
                data={item}
                key={index}
                assistant={
                  assistantList?.find((item) => item.id === assistantSelected)
                    ?.name
                }
              />
            ))}

            {gptLoading && (
              <div
                className={
                  "flex gap-4 bg-module-background-gray p-4 rounded-lg"
                }
              >
                <div className="w-[32px] h-[32px] rounded-full bg-chat-icon-orange profile_img"></div>
                <div className="flex flex-col">
                  <span className="font-bold">
                    {
                      assistantList?.find(
                        (item) => item.id === assistantSelected
                      )?.name
                    }
                  </span>
                  <Loading />
                </div>
              </div>
            )}

            {(allMessageList?.length === 0 || allMessageList == null) && (
              <span className="text-3xl font-semibold text-borders-gray flex justify-center items-center h-full">
                {" "}
                Ask a question...{" "}
              </span>
            )}
          </div>
          <div className="relative px-10 p-4 w-[770px] mx-auto">
            <input
              id="question"
              name="question"
              type="text"
              autoComplete="question"
              placeholder="Ask a question .."
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(event) => event.key === "Enter" && onMessageSend()}
              value={question}
              className="block w-full text-base font-medium rounded-[10px] border-0 p-3 pr-10 text-gray-100 shadow-sm ring-1 ring-inset ring-[#d9d9e3] placeholder:text-gray-100"
            />
            <div
              className="absolute inset-y-0 right-10 flex items-center pr-3 cursor-pointer"
              onClick={onMessageSend}
            >
              {gptLoading ? (
                <FaRegStopCircle size={25} />
              ) : (
                <svg
                  width={35}
                  height={35}
                  viewBox="0 0 35 35"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M23.6105 2.91663H11.3897C6.08133 2.91663 2.91675 6.08121 2.91675 11.3895V23.5958C2.91675 28.9187 6.08133 32.0833 11.3897 32.0833H23.5959C28.9042 32.0833 32.0688 28.9187 32.0688 23.6104V11.3895C32.0834 6.08121 28.9188 2.91663 23.6105 2.91663ZM24.5292 15.7791C24.1063 16.202 23.4063 16.202 22.9834 15.7791L18.5938 11.3895V26.25C18.5938 26.8479 18.098 27.3437 17.5001 27.3437C16.9022 27.3437 16.4063 26.8479 16.4063 26.25V11.3895L12.0167 15.7791C11.5938 16.202 10.8938 16.202 10.4709 15.7791C10.2522 15.5604 10.1501 15.2833 10.1501 15.0062C10.1501 14.7291 10.2667 14.4375 10.4709 14.2333L16.7272 7.97704C16.9313 7.77288 17.2084 7.65621 17.5001 7.65621C17.7917 7.65621 18.0688 7.77288 18.273 7.97704L24.5292 14.2333C24.9522 14.6562 24.9522 15.3416 24.5292 15.7791Z"
                    fill={question.length > 0 ? "#111" : "#d9d9e3"}
                  />
                </svg>
              )}
            </div>
          </div>
        </div>
      )}

      {location.pathname != "/" && (
        <div className="w-full  flex flex-col h-screen">
          <div className="bg-white p-6 flex justify-between border-b border-b-borders-gray">
            <span>Library</span>
          </div>
          <div className="flex-grow gap-4 flex flex-col px-6 py-3 overflow-auto">
            {uploadFile ? (
              <div className="flex items-center justify-center w-1/2 mx-auto mt-5 flex-col">
                <label
                  htmlFor="dropzone-file"
                  className="flex flex-col items-center justify-center w-full h-48 border-2 border-borders-gray border-dashed rounded-lg cursor-pointer hover:bg-gray-50"
                  onDragOver={(event) => event.preventDefault()}
                  onDrop={handleDrop}
                >
                  <div className="flex flex-col items-center justify-center pt-5 pb-6">
                    <svg
                      className="w-8 h-8 mb-4 text-gray-100"
                      aria-hidden="true"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 20 16"
                    >
                      <path
                        stroke="currentColor"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"
                      />
                    </svg>
                    <p className="mb-2 text-sm">
                      <span className="font-semibold text-gray-100">
                        Choose a file or drag & drop it here
                      </span>
                    </p>
                    <p className="text-xs text-gray-100">
                      Word, PDF, and XLS formats, up to 512MB
                    </p>
                    <div className="border border-borders-gray text-gray-100 text-sm font-medium pt-[4px] pb-[6px] px-6 rounded-xl mt-5">
                      Browse File
                    </div>
                  </div>
                  <input
                    id="dropzone-file"
                    onClick={() => setUploadedFileList([])}
                    onChange={handleFileInput}
                    multiple
                    type="file"
                    className="hidden"
                    accept=".docx, .pdf, .xlsx"
                  />
                </label>
                <div className="w-full mt-4 grid gap-3">
                  {uploadedFileList.map((item, index) => (
                    <div
                      key={index}
                      className="bg-file-upload-background-gray py-2 px-4 rounded-2xl flex justify-between items-center"
                    >
                      <div className="flex gap-6 items-center">
                        {item.file_name?.split(".")[1] == "pdf" && (
                          <FaRegFilePdf size={30} color={"red"} />
                        )}
                        {item.file_name?.split(".")[1] == "docx" && (
                          <FaRegFileWord size={30} color={"blue"} />
                        )}
                        {item.file_name?.split(".")[1] == "xlsx" && (
                          <FaRegFileExcel size={30} color={"green"} />
                        )}
                        <div>
                          <span>
                            {item.file_name?.length > 25
                              ? item.file_name?.substring(0, 25) + "..."
                              : item?.file_name}
                          </span>
                          <div className="flex gap-8 items-center">
                            <span className="text-sm text-borders-gray">
                              {" "}
                              {Math.floor(item?.file_size / 1024)} KB
                            </span>{" "}
                            <div className="text-sm flex gap-2 items-center">
                              {fileStatus == "Uploading" && (
                                <>
                                  <svg
                                    width={25}
                                    height={25}
                                    viewBox="0 0 25 25"
                                    fill="none"
                                    xmlns="http://www.w3.org/2000/svg"
                                  >
                                    <path
                                      d="M12.0371 7.22107C11.4871 7.22107 11.0371 6.77107 11.0371 6.22107V2.22107C11.0371 1.67107 11.4871 1.22107 12.0371 1.22107C12.5871 1.22107 13.0371 1.67107 13.0371 2.22107V6.22107C13.0371 6.77107 12.5871 7.22107 12.0371 7.22107ZM12.0371 23.2211C11.4871 23.2211 11.0371 22.7711 11.0371 22.2211V18.2211C11.0371 17.6711 11.4871 17.2211 12.0371 17.2211C12.5871 17.2211 13.0371 17.6711 13.0371 18.2211V22.2211C13.0371 22.7711 12.5871 23.2211 12.0371 23.2211ZM22.0371 13.2211H18.0371C17.4871 13.2211 17.0371 12.7711 17.0371 12.2211C17.0371 11.6711 17.4871 11.2211 18.0371 11.2211H22.0371C22.5871 11.2211 23.0371 11.6711 23.0371 12.2211C23.0371 12.7711 22.5871 13.2211 22.0371 13.2211ZM6.03711 13.2211H2.03711C1.48711 13.2211 1.03711 12.7711 1.03711 12.2211C1.03711 11.6711 1.48711 11.2211 2.03711 11.2211H6.03711C6.58711 11.2211 7.03711 11.6711 7.03711 12.2211C7.03711 12.7711 6.58711 13.2211 6.03711 13.2211ZM19.1071 20.2911C18.8471 20.2911 18.5971 20.1911 18.3971 20.0011L15.5671 17.1711C15.4745 17.0785 15.4011 16.9686 15.351 16.8476C15.3009 16.7266 15.2751 16.597 15.2751 16.4661C15.2751 16.3351 15.3009 16.2055 15.351 16.0845C15.4011 15.9636 15.4745 15.8537 15.5671 15.7611C15.6597 15.6685 15.7696 15.595 15.8906 15.5449C16.0115 15.4948 16.1412 15.469 16.2721 15.469C16.403 15.469 16.5327 15.4948 16.6537 15.5449C16.7746 15.595 16.8845 15.6685 16.9771 15.7611L19.8071 18.5911C19.9467 18.7307 20.0416 18.9087 20.0798 19.1024C20.1179 19.2961 20.0977 19.4968 20.0216 19.6789C19.9455 19.8611 19.817 20.0166 19.6524 20.1255C19.4878 20.2345 19.2945 20.2922 19.0971 20.2911H19.1071ZM7.79711 8.98107C7.53711 8.98107 7.28711 8.88107 7.08711 8.69107L4.25711 5.86107C4.16453 5.76849 4.09109 5.65858 4.04098 5.53761C3.99088 5.41665 3.96509 5.287 3.96509 5.15607C3.96509 5.02514 3.99088 4.89549 4.04098 4.77453C4.09109 4.65356 4.16453 4.54365 4.25711 4.45107C4.34969 4.35849 4.4596 4.28505 4.58057 4.23494C4.70153 4.18484 4.83118 4.15905 4.96211 4.15905C5.09304 4.15905 5.22269 4.18484 5.34365 4.23494C5.46462 4.28505 5.57453 4.35849 5.66711 4.45107L8.49711 7.28107C8.63666 7.42072 8.73155 7.59869 8.76975 7.79239C8.80795 7.98608 8.78772 8.18676 8.71163 8.36893C8.63555 8.5511 8.50704 8.70656 8.34243 8.81555C8.17782 8.92454 7.98453 8.98215 7.78711 8.98107H7.79711ZM4.96711 20.2911C4.70711 20.2911 4.45711 20.1911 4.25711 20.0011C4.16441 19.9086 4.09086 19.7987 4.04068 19.6777C3.9905 19.5567 3.96467 19.427 3.96467 19.2961C3.96467 19.1651 3.9905 19.0354 4.04068 18.9144C4.09086 18.7935 4.16441 18.6836 4.25711 18.5911L7.08711 15.7611C7.17969 15.6685 7.2896 15.595 7.41057 15.5449C7.53153 15.4948 7.66118 15.469 7.79211 15.469C7.92304 15.469 8.05269 15.4948 8.17365 15.5449C8.29462 15.595 8.40453 15.6685 8.49711 15.7611C8.58969 15.8537 8.66313 15.9636 8.71324 16.0845C8.76334 16.2055 8.78913 16.3351 8.78913 16.4661C8.78913 16.597 8.76334 16.7266 8.71324 16.8476C8.66313 16.9686 8.58969 17.0785 8.49711 17.1711L5.66711 20.0011C5.46711 20.2011 5.21711 20.2911 4.95711 20.2911H4.96711ZM16.2771 8.98107C16.0171 8.98107 15.7671 8.88107 15.5671 8.69107C15.4744 8.59856 15.4009 8.48867 15.3507 8.36769C15.3005 8.24672 15.2747 8.11704 15.2747 7.98607C15.2747 7.8551 15.3005 7.72542 15.3507 7.60444C15.4009 7.48347 15.4744 7.37358 15.5671 7.28107L18.3971 4.45107C18.4897 4.35849 18.5996 4.28505 18.7206 4.23494C18.8415 4.18484 18.9712 4.15905 19.1021 4.15905C19.233 4.15905 19.3627 4.18484 19.4837 4.23494C19.6046 4.28505 19.7145 4.35849 19.8071 4.45107C19.8997 4.54365 19.9731 4.65356 20.0232 4.77453C20.0733 4.89549 20.0991 5.02514 20.0991 5.15607C20.0991 5.287 20.0733 5.41665 20.0232 5.53761C19.9731 5.65858 19.8997 5.76849 19.8071 5.86107L16.9771 8.69107C16.7771 8.89107 16.5271 8.98107 16.2671 8.98107H16.2771Z"
                                      fill="#375EF9"
                                    />
                                  </svg>
                                  {fileStatus}
                                </>
                              )}
                              {fileStatus == "Completed" && (
                                <>
                                  <svg
                                    width={24}
                                    height={25}
                                    viewBox="0 0 24 25"
                                    fill="none"
                                    xmlns="http://www.w3.org/2000/svg"
                                  >
                                    <path
                                      d="M12 2.12524C6.49 2.12524 2 6.61524 2 12.1252C2 17.6352 6.49 22.1252 12 22.1252C17.51 22.1252 22 17.6352 22 12.1252C22 6.61524 17.51 2.12524 12 2.12524ZM16.78 9.82524L11.11 15.4952C10.97 15.6352 10.78 15.7152 10.58 15.7152C10.38 15.7152 10.19 15.6352 10.05 15.4952L7.22 12.6652C6.93 12.3752 6.93 11.8952 7.22 11.6052C7.51 11.3152 7.99 11.3152 8.28 11.6052L10.58 13.9052L15.72 8.76524C16.01 8.47524 16.49 8.47524 16.78 8.76524C17.07 9.05524 17.07 9.52524 16.78 9.82524Z"
                                      fill="#3EBF8F"
                                    />
                                  </svg>
                                  {fileStatus}
                                </>
                              )}
                              {fileStatus == "error" && (
                                <>
                                  <svg
                                    width={25}
                                    height={25}
                                    viewBox="0 0 25 25"
                                    fill="#FF0000"
                                    xmlns="http://www.w3.org/2000/svg"
                                  >
                                    <path
                                      d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z"
                                      stroke="#fff"
                                      strokeWidth="1.5"
                                      strokeLinecap="round"
                                      strokeLinejoin="round"
                                    />
                                    <path
                                      d="M15 9L9 15"
                                      stroke="#fff"
                                      strokeWidth="1.5"
                                      strokeLinecap="round"
                                      strokeLinejoin="round"
                                    />
                                    <path
                                      d="M9 9L15 15"
                                      stroke="#fff"
                                      strokeWidth="1.5"
                                      strokeLinecap="round"
                                      strokeLinejoin="round"
                                    />
                                  </svg>
                                  File already uploaded
                                </>
                              )}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <>
                <div
                  className={`border-2 rounded-lg w-fit py-2 px-4 flex gap-2 cursor-pointer ${
                    isHovered
                      ? "bg-gray-100 border-white"
                      : "bg-white border-borders-gray"
                  } `}
                  onMouseEnter={() => setIsHovered(true)}
                  onMouseLeave={() => setIsHovered(false)}
                  onClick={() => {
                    setUploadFile(true);
                    setUploadedFileList([]);
                  }}
                >
                  <span
                    className={`font-semibold ${
                      isHovered ? "text-white" : "text-borders-gray"
                    }`}
                  >
                    File Upload
                  </span>
                  <svg
                    width={24}
                    height={24}
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                    fill={isHovered ? "#fff" : "#A9ACB4"}
                  >
                    <path
                      d="M21.0169 7.99175C21.4148 8.55833 20.9405 9.25 20.2482 9.25H3C2.44772 9.25 2 8.80228 2 8.25V6.42C2 3.98 3.98 2 6.42 2H8.74C10.37 2 10.88 2.53 11.53 3.4L12.93 5.26C13.24 5.67 13.28 5.72 13.86 5.72H16.65C18.4546 5.72 20.0516 6.61709 21.0169 7.99175Z"
                      fill={isHovered ? "#fff" : "#A9ACB4"}
                    />
                    <path
                      d="M21.9834 11.7463C21.9815 11.1953 21.5343 10.7496 20.9834 10.7497L2.99998 10.75C2.44771 10.75 2 11.1977 2 11.75V16.65C2 19.6 4.4 22 7.35 22H16.65C19.6 22 22 19.6 22 16.65L21.9834 11.7463ZM14.5 16.75H12.81V18.5C12.81 18.91 12.47 19.25 12.06 19.25C11.64 19.25 11.31 18.91 11.31 18.5V16.75H9.5C9.09 16.75 8.75 16.41 8.75 16C8.75 15.59 9.09 15.25 9.5 15.25H11.31V13.5C11.31 13.09 11.64 12.75 12.06 12.75C12.47 12.75 12.81 13.09 12.81 13.5V15.25H14.5C14.91 15.25 15.25 15.59 15.25 16C15.25 16.41 14.91 16.75 14.5 16.75Z"
                      fill={isHovered ? "#fff" : "#A9ACB4"}
                    />
                  </svg>
                </div>
                <StickyHeadTable
                  setLoading={setLoading}
                  setUsedSpace={setUsedSpace}
                  totalSpace={totalSpace}
                  setUsedSpaceMB={setUsedSpaceMB}
                />
              </>
            )}
          </div>
          <div className="w-[200px] pb-6 px-6">
            <BorderLinearProgress variant="determinate" value={usedSpace} />
            <span className="text-[11px] font-medium">
              {usedSpaceMB}MB used out of {totalSpace}GB
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;
