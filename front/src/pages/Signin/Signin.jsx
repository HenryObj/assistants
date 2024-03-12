import React from "react";
import { Link } from "react-router-dom";
import logo from "../../assets/image/logo.webp";

const Signin = () => {
  return (
    <>
      <div className="py-2 text-signup-orange bg-bg_sidebar-black flex justify-center items-center">
        <img
          src={logo}
          alt="logo" className="w-[260px] h-20 obj_fit"          
        />
      </div>
      <div className="border border-borders-gray rounded-xl w-[600px] mx-auto mt-20 mb-10 py-4 font-inter">
        <div className="text-center my-4">
          <span className="text-3xl font-medium mb-4"> Log in </span>
        </div>
        <div className="grid gap-5 text-gray-100 px-10">
          <div className="">
            <label
              htmlFor="email"
              className="block font-normal leading-6 text-gray-100"
            >
              Email address
            </label>
            <div className="mt-2">
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                placeholder="Enter Email Address"
                className="block w-full text-base rounded-[10px] border-0 p-3 text-gray-100 shadow-sm ring-1 ring-inset ring-borders-gray placeholder:text-gray-100"
              />
            </div>
          </div>
          <div className="">
            <div className="flex justify-between">
              <label
                htmlFor="password"
                className="block font-normal leading-6 text-gray-100"
              >
                Password
              </label>
              <div className="flex gap-1 cursor-pointer">
                <svg
                  width={25}
                  height={24}
                  viewBox="0 0 25 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M20.5189 4.88134L19.783 4.14539C19.575 3.9374 19.191 3.96941 18.951 4.25736L16.3908 6.80132C15.2388 6.30538 13.9749 6.06538 12.6468 6.06538C8.6947 6.08132 5.27092 8.38529 3.6228 11.6975C3.52677 11.9055 3.52677 12.1614 3.6228 12.3374C4.39073 13.9054 5.54281 15.2015 6.98281 16.1774L4.88682 18.3054C4.64682 18.5454 4.61481 18.9293 4.77485 19.1374L5.5108 19.8733C5.71879 20.0813 6.10277 20.0493 6.34277 19.7613L20.3907 5.71345C20.6947 5.47358 20.7267 5.08962 20.5187 4.88161L20.5189 4.88134ZM13.4948 9.71322C13.2228 9.6492 12.9349 9.56925 12.6628 9.56925C11.3028 9.56925 10.2149 10.6573 10.2149 12.0172C10.2149 12.2892 10.2789 12.5771 10.3589 12.8492L9.28675 13.9052C8.9668 13.3452 8.79081 12.7211 8.79081 12.0172C8.79081 9.88924 10.5028 8.17722 12.6308 8.17722C13.3349 8.17722 13.9588 8.3532 14.5188 8.67316L13.4948 9.71322Z"
                    fill="#666666"
                    fillOpacity="0.8"
                  />
                  <path
                    d="M21.6714 11.6974C21.1114 10.5774 20.3753 9.56945 19.4634 8.75342L16.4874 11.6974V12.0174C16.4874 14.1454 14.7754 15.8574 12.6474 15.8574H12.3274L10.4395 17.7454C11.1435 17.8893 11.8795 17.9854 12.5995 17.9854C16.5516 17.9854 19.9754 15.6814 21.6235 12.3532C21.7675 12.1292 21.7675 11.9053 21.6714 11.6973L21.6714 11.6974Z"
                    fill="#666666"
                    fillOpacity="0.8"
                  />
                </svg>
                <span>Hide</span>
              </div>{" "}
            </div>
            <div className="mt-2 text-right">
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="password"
                placeholder="Enter your password"
                className="block w-full text-base rounded-[10px] border-0 p-3 text-gray-100 shadow-sm ring-1 ring-inset ring-borders-gray placeholder:text-gray-100"
              />
              <u className="text-end mt-2 text-black">Forgot your password</u>
            </div>
            <div className="mt-2 text-black">
              <input
                id="remember"
                name="remember"
                type="checkbox"
                className="accent-black cursor-pointer"
              />
              <span className="ml-2">Remember me</span>
            </div>
          </div>
          <div className="">
            <Link to={"/"}>
              <button className="w-full p-3 rounded-full bg-signup-orange text-white text-xl">
                Log in
              </button>
            </Link>
          </div>
          <hr className="h-px my-3 bg-borders-gray border-0" />
          <div className="text-center">
            <span className="text-black text-xl font-medium">
              Don’t have an account?
            </span>
            <Link to={"/sign-up"}>
              <button className="my-4 w-full p-3 rounded-full  border text-black text-xl">
                Create an account
              </button>
            </Link>
          </div>
        </div>
      </div>
    </>
  );
};

export default Signin;
