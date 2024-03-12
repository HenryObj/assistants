import React from "react";
import { Link } from "react-router-dom";
import { updateAssistant } from "../redux/assistantSlice";

const History = ({
  title,
  data,
  setAssistant,
  setThreadId,
  getAllMessages,
  threadId,
}) => {
  return (
    <div className="grid gap-1 cursor-pointer">
      <span className="text-sm text-gray-100 cursor-auto">{title}</span>
      {data?.map((item, index) => (
        <Link to={"/"} key={index}>
          <div
            className={
              threadId == item?.thread_id
                ? "bg-[#343541] py-1 px-2 rounded-lg hover:bg-[#343541] hover:py-1 hover:px-2 hover:rounded-lg"
                : "hover:bg-[#343541] hover:py-1 hover:px-2 hover:rounded-lg py-1 px-2"
            }
            onClick={() => {
              setAssistant(updateAssistant(item.assistant_id));
              setThreadId(item.thread_id);
              getAllMessages(item.thread_id);
            }}
          >
            <span key={index} className="text-[14px]">
              {item.first_words}
            </span>
          </div>
        </Link>
      ))}
    </div>
  );
};

export default History;
