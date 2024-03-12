import React from "react";
import { useState } from "react";
const Message = ({ data, assistant }) => {
  const [isExpanded, setExpanded] = useState(false);
  const maxChars = 250;
  // Truncate the message if it exceeds maxChars characters
  const truncatedMessage =
    data?.content?.length > maxChars
      ? data?.content?.slice(0, maxChars) + "..."
      : data?.content;

  return (
    <>
      <div
        key={data?.id}
        className={
          data.role == "user"
            ? "flex gap-4 p-4"
            : "flex gap-4 bg-module-background-gray p-4 rounded-lg"
        }
      >
        <div>
          {data.role == "user" && (
            <div className="text-[10px] font-medium rounded-full bg-button-selected-blue w-[32px] h-[32px] flex justify-center items-center">
              HO
            </div>
          )}
          {data.role != "user" && (
            <div className="w-[32px] h-[32px] rounded-full bg-chat-icon-orange profile_img"></div>
          )}
        </div>
        <div className="flex flex-col font-DM_Sans text-lg">
          <span className="font-bold">
            {data?.role == "user" ? "User" : assistant}
          </span>
          <span className="text-justify text-chat-font leading-6">
            {isExpanded ? data?.content : truncatedMessage}
          </span>
          {data?.content?.length > maxChars && (
            <button
              className="w-fit underline text-[#0000BF] cursor-pointer focus:outline-none text-left text-sm"
              onClick={() => setExpanded(!isExpanded)}
            >
              {isExpanded ? "see less" : "see more"}
            </button>
          )}
        </div>
      </div>
    </>
  );
};

export default Message;
