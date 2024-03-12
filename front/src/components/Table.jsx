import React, { useEffect, useState } from "react";
import Paper from "@mui/material/Paper";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TablePagination from "@mui/material/TablePagination";
import TableRow from "@mui/material/TableRow";
import axios from "axios";

const columns = [
  { id: "file_name", label: "Name" },
  { id: "kind", label: "Kind" },
  { id: "date", label: "Date Added" },
  { id: "action", label: "" },
];

function createData(name, kind, date, action) {
  return { name, kind, date, action };
}

export default function StickyHeadTable({
  totalSpace,
  setLoading,
  setUsedSpace,
  setUsedSpaceMB,
}) {
  // const [loading, setLoading] = useState(false)
  const [tableData, setTableData] = useState([]);
  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await axios.get(
        `${import.meta.env.VITE_API_URL}get-files`
      );
      setTableData(response.data.data);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching data:", error);
      setLoading(false);
    }
  };

  const getFileSize = async () => {
    try {
      const response = await axios.get(
        `${import.meta.env.VITE_API_URL}total-file-size?client_id=1`
      );
      setUsedSpaceMB(response.data.data[0][0]);
      const totalSpaceMB = totalSpace * 1024;
      const percentage = (response.data.data[0][0] / totalSpaceMB) * 100;
      setUsedSpace(Math.round(percentage * 100) / 100);
    } catch (error) {
      console.error(error);
    }
  };
  useEffect(() => {
    fetchData();
    getFileSize();
  }, []);

  const handleDelete = async (id) => {
    setLoading(true);
    try {
      const response = await axios.delete(
        `${import.meta.env.VITE_API_URL}delete-file?file_id=${id}`
      );
      setLoading(false);
      fetchData();
    } catch (error) {
      setLoading(false);
      fetchData();
      console.error("Error delete file data:", error);
    }
  };
  return (
    <Paper sx={{ width: "100%", overflow: "hidden" }}>
      <TableContainer sx={{ maxHeight: "70vh" }} className="pdf_list custom-scrollbar">
        <Table stickyHeader aria-label="sticky table">
          <TableHead>
            <TableRow>
              {columns.map((column) => (
                <TableCell
                  key={column.id}
                  align={column.align}
                  style={{ minWidth: column.minWidth, fontFamily: "Inter" }}
                >
                  {column.label}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {tableData.map((row,index) => {
              return (
                <TableRow hover role="checkbox" tabIndex={-1} key={index}>
                  {columns.map((column,index) => {
                    const value = row[column.id];
                    return (
                      <TableCell
                        key={index}
                        align={column.align}
                        sx={{
                          fontFamily: "Inter",
                        }}
                      >
                        {column.id == "file_name" ? (
                          <div className="flex gap-3 items-center">
                            {" "}
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
                        ) : column.id == "kind" ? (
                          "PDF Document"
                        ) : column.id == "date" ? (
                          <>
                              {row.formatted_date}
                          </>
                        ) : column.id == "action" ? (
                          <div
                            className="cursor-pointer"
                            onClick={() => handleDelete(row.file_id)}
                          >
                            <svg
                              width={20}
                              height={20}
                              viewBox="0 0 20 20"
                              fill="none"
                              xmlns="http://www.w3.org/2000/svg"
                            >
                              <path
                                d="M17.5 4.98332C14.725 4.70832 11.9333 4.56665 9.15 4.56665C7.5 4.56665 5.85 4.64998 4.2 4.81665L2.5 4.98332"
                                stroke="#A9ACB4"
                                strokeWidth="1.5"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                              />
                              <path
                                d="M7.08301 4.14163L7.26634 3.04996C7.39967 2.25829 7.49967 1.66663 8.90801 1.66663H11.0913C12.4997 1.66663 12.608 2.29163 12.733 3.05829L12.9163 4.14163"
                                stroke="#A9ACB4"
                                strokeWidth="1.5"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                              />
                              <path
                                d="M15.7087 7.6167L15.167 16.0084C15.0753 17.3167 15.0003 18.3334 12.6753 18.3334H7.32533C5.00033 18.3334 4.92533 17.3167 4.83366 16.0084L4.29199 7.6167"
                                stroke="#A9ACB4"
                                strokeWidth="1.5"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                              />
                              <path
                                d="M8.6084 13.75H11.3834"
                                stroke="#A9ACB4"
                                strokeWidth="1.5"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                              />
                              <path
                                d="M7.91699 10.4166H12.0837"
                                stroke="#A9ACB4"
                                strokeWidth="1.5"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                              />
                            </svg>
                          </div>
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
    </Paper>
  );
}
