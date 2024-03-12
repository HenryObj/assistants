import * as React from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import { useState } from "react";
import { useEffect } from "react";
import axios from "axios";

const columns = [
  { id: "selected", label: "Selected", maxWidth: "70px", align: "center" },
  { id: "file_name", label: "Name" },
  { id: "kind", label: "Kind" },
  { id: "date", label: "Date Added" },
];

function createData(selected, name, kind, date) {
  return { selected, name, kind, date };
}

export default function StickyHeadTable({
  selectedObjects,
  setSelectedObjects,
  assistant,
  setAssistantAttachFileList,
  setToast
}) {
  const [tableData, setTableData] = useState([]);
  const fetchData = async () => {
    try {
      const response = await axios.get(
        `${import.meta.env.VITE_API_URL}get-files`
      );
      setTableData(response.data.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const fetchAssistantAttachmentData = async () => {
    try {
      const response = await axios.get(
        `${
          import.meta.env.VITE_API_URL
        }assistant-file-list?assistant_id=${assistant}`
      );
      setSelectedObjects(response.data.data);
      setAssistantAttachFileList(response.data.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    fetchData();
    if (assistant) {
      fetchAssistantAttachmentData();
    }
  }, []);

  const handleCheckboxClick = (row) => {
    // Check if the row is already in the selectedObjects array
    const isSelected = selectedObjects?.some(
      (selectedFile) =>
        (selectedFile?.file_id || selectedFile?.id) === row?.file_id
    );
    // If the row is selected, remove it from the array; otherwise, add it
    if (isSelected) {
      setSelectedObjects((prevSelectedObjects) =>
        prevSelectedObjects?.filter(
          (selectedRow) =>
            (selectedRow?.id || selectedRow?.file_id) !== row?.file_id
        )
      );
    } else {
      setSelectedObjects((prevSelectedObjects) => [
        ...(prevSelectedObjects ?? []),
        row,
      ]);
    }
  };
  return (
    <>
      <div className="flex gap-16 bg-attach-header-background-blue rounded-3xl p-1 px-8 font-inter">
        <div className="flex items-center gap-2">
          <svg
            width={16}
            height={16}
            viewBox="0 0 16 16"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M5.92617 4.02073C4.04092 5.97583 4.45232 9.22039 6.61184 10.6577C6.683 10.7051 6.77766 10.6957 6.83878 10.6358C7.29342 10.1906 7.67802 9.75928 8.01479 9.21077C8.06631 9.12685 8.03427 9.01795 7.94782 8.97101C7.61843 8.79214 7.29066 8.45675 7.10615 8.10247L7.10593 8.10259C6.8849 7.66144 6.80964 7.16692 6.92666 6.6562C6.92679 6.65623 6.92691 6.65626 6.92704 6.65626C7.06169 6.0024 7.76202 5.39416 8.29691 4.83165C8.29578 4.83127 8.29469 4.83086 8.29357 4.83049L10.2976 2.78028C11.0963 1.96325 12.41 1.95651 13.2169 2.76533C14.032 3.56582 14.0455 4.88921 13.2469 5.70621L12.033 6.95741C11.9768 7.01532 11.9586 7.0998 11.9849 7.17616C12.2644 7.98856 12.3331 9.13406 12.1458 9.9995C12.1406 10.0237 12.1704 10.0396 12.1877 10.0219L14.7712 7.37885C16.4217 5.69045 16.4077 2.94151 14.7401 1.27009C13.0384 -0.435635 10.2679 -0.421439 8.58366 1.30159L5.93652 4.00963C5.93302 4.01333 5.9297 4.01709 5.92617 4.02073Z"
              fill="black"
            />
            <path
              d="M10.7558 11.0299C10.7558 11.03 10.7557 11.0301 10.7557 11.0302C10.7573 11.0295 10.7589 11.0289 10.7605 11.0281C11.2878 10.0618 11.3916 8.95342 11.1445 7.87297L11.1433 7.87413L11.1421 7.8736C10.9075 6.9113 10.2637 5.95573 9.38931 5.36739C9.31409 5.31678 9.19395 5.32264 9.12351 5.37974C8.6806 5.73869 8.24707 6.19899 7.96101 6.78639C7.91609 6.87861 7.94973 6.98939 8.03826 7.0409C8.37025 7.23409 8.67007 7.51693 8.87081 7.89243L8.87112 7.89222C9.02756 8.15748 9.18172 8.6608 9.08187 9.2016C9.08181 9.2016 9.08171 9.2016 9.08165 9.2016C8.98848 9.91861 8.26611 10.5763 7.69186 11.1689L7.69214 11.1692C7.25502 11.6173 6.14382 12.7527 5.69888 13.2083C4.90025 14.0253 3.57994 14.0388 2.76483 13.2383C1.94973 12.4379 1.93626 11.1145 2.73488 10.2975L3.95238 9.04251C4.00756 8.98563 4.02632 8.90297 4.00177 8.82754C3.73144 7.99616 3.65738 6.87648 3.82801 6.01201C3.83276 5.98791 3.80319 5.97252 3.78602 5.99007L1.24133 8.59333C-0.426008 10.2991 -0.411877 13.0762 1.27279 14.7648C2.97446 16.4359 5.73086 16.4077 7.39814 14.7021C7.97736 14.0526 10.4568 11.7517 10.7558 11.0299Z"
              fill="black"
            />
          </svg>
          <span className="font-semibold">Attach</span>
        </div>
        <div className="flex items-center gap-2 font-semibold">
          <span>{selectedObjects?.length ? selectedObjects?.length : 0}</span>
          <span>/ 20 attached</span>
        </div>
      </div>
      <TableContainer sx={{ maxHeight: "50vh" }} className="custom-scrollbar">
        <Table stickyHeader aria-label="sticky table">
          <TableHead>
            <TableRow>
              {columns.map((column, index) => (
                <TableCell
                  key={index}
                  align={column.align}
                  style={{
                    minWidth: column.minWidth,
                    maxWidth: column.maxWidth,
                    fontFamily: "Inter",
                  }}
                >
                  {column.label}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {tableData.map((row, index) => {
              return (
                <TableRow hover role="checkbox" tabIndex={-1} key={index}>
                  {columns.map((column, index) => {
                    const value = row[column.id];
                    return (
                      <TableCell
                        key={index}
                        align={column.align}
                        sx={{
                          fontFamily: "Inter",
                          paddingY: 1,
                        }}
                      >
                        {column.id == "file_name" ? (
                          <div className="flex gap-3 items-center">
                            <svg
                              width="25"
                              height="26"
                              viewBox="0 0 25 26"
                              fill="none"
                              xmlns="http://www.w3.org/2000/svg"
                            >
                              <path
                                d="M7.89941 15.7153V11.8298C7.89941 7.07705 11.5447 3.17574 16.1919 2.76921L23.0005 9.68334V15.7153C23.0005 19.8853 19.62 23.2658 15.45 23.2658C11.2799 23.2658 7.89941 19.8853 7.89941 15.7153Z"
                                fill="#EEF1F7"
                                stroke="#CBD0DC"
                                strokeWidth="4"
                              />
                              <rect
                                y="11.5737"
                                width="16.8539"
                                height="9.98378"
                                rx="4.99189"
                                fill="#D82042"
                              />
                              <path
                                d="M2.79297 18.9903V14.2189H4.46779C4.83334 14.2189 5.13619 14.2864 5.37632 14.4216C5.61645 14.5567 5.79617 14.7415 5.91547 14.9761C6.03478 15.209 6.09443 15.4715 6.09443 15.7635C6.09443 16.0571 6.03401 16.3211 5.91318 16.5557C5.79388 16.7887 5.6134 16.9735 5.37173 17.1102C5.1316 17.2453 4.82952 17.3129 4.46549 17.3129H3.31377V16.7025H4.40125C4.63221 16.7025 4.81958 16.6621 4.96335 16.5813C5.10713 16.499 5.21266 16.3872 5.27996 16.2458C5.34726 16.1045 5.38091 15.9437 5.38091 15.7635C5.38091 15.5834 5.34726 15.4234 5.27996 15.2836C5.21266 15.1438 5.10636 15.0343 4.96106 14.9551C4.81728 14.8759 4.62762 14.8363 4.39208 14.8363H3.5019V18.9903H2.79297Z"
                                fill="white"
                              />
                              <path
                                d="M8.44663 18.9903H6.92553V14.2189H8.49481C8.9552 14.2189 9.35058 14.3144 9.68095 14.5054C10.0113 14.6949 10.2645 14.9675 10.4404 15.3232C10.6178 15.6773 10.7065 16.1021 10.7065 16.5976C10.7065 17.0946 10.617 17.5218 10.4381 17.879C10.2606 18.2363 10.0037 18.5112 9.66719 18.7038C9.33069 18.8948 8.92384 18.9903 8.44663 18.9903ZM7.63446 18.3613H8.40763C8.76554 18.3613 9.06303 18.2929 9.3001 18.1563C9.53718 18.018 9.7146 17.8184 9.83237 17.5575C9.95015 17.295 10.009 16.975 10.009 16.5976C10.009 16.2233 9.95015 15.9057 9.83237 15.6447C9.71613 15.3838 9.54253 15.1857 9.31157 15.0506C9.08062 14.9155 8.79383 14.8479 8.45122 14.8479H7.63446V18.3613Z"
                                fill="white"
                              />
                              <path
                                d="M11.5881 18.9903V14.2189H14.5018V14.8386H12.297V16.2924H14.293V16.9098H12.297V18.9903H11.5881Z"
                                fill="white"
                              />
                            </svg>
                            <span>{value}</span>
                          </div>
                        ) : column.id == "selected" ? (
                          <>
                            <input
                              type="checkbox"
                              // checked={selectedObjects?.includes(row)}
                              checked={
                                selectedObjects?.some(
                                  (selectedFile) =>
                                    selectedFile?.id === row?.file_id
                                ) || selectedObjects?.includes(row)
                              }
                              onChange={() => handleCheckboxClick(row)}
                            />{" "}
                          </>
                        ) : column.id == "kind" ? (
                          <>PDF Document</>
                        ) : column.id == "date" ? (
                          <>
                              {row.formatted_date}
                          </>
                        ) : (
                          value
                        )}
                      </TableCell>
                    );
                  })}
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>
    </>
  );
}
