import React from "react";
import { useState } from "react";
import { Link } from "react-router-dom";
import logo from "../../assets/image/logo.webp";

const Signup = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  return (
    <>
      <div className="py-2 text-signup-orange bg-bg_sidebar-black flex justify-center items-center">
        <img src={logo} alt="logo" className="w-[260px] h-20 obj_fit" />
      </div>
      <div className="border border-borders-gray rounded-xl w-[650px] mx-auto mt-20 mb-10 py-4 font-inter">
        <div className="text-center my-4">
          <span className="text-3xl font-medium mb-4"> Create an account </span>
          <p>
            Already have an ccount?
            <Link to={"/sign-in"}>
              <u> Log in </u>{" "}
            </Link>
          </p>
        </div>
        <div className="grid gap-5 text-gray-100">
          <div className="px-10">
            <label
              htmlFor="email"
              className="block font-normal leading-6 text-gray-100"
            >
              What’s your email?{" "}
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
          <div className="px-10">
            <div className="flex justify-between">
              <label
                htmlFor="password"
                className="block font-normal leading-6 text-gray-100"
              >
                Create a password{" "}
              </label>
              <div
                className="flex gap-1 cursor-pointer items-center"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? (
                  <svg
                    fill="#666666"
                    height={20}
                    width={20}
                    version="1.1"
                    id="Capa_1"
                    viewBox="0 0 612 612"
                  >
                    <g id="SVGRepo_iconCarrier">
                      {" "}
                      <g>
                        {" "}
                        <g>
                          {" "}
                          <path d="M609.608,315.426c3.19-5.874,3.19-12.979,0-18.853c-58.464-107.643-172.5-180.72-303.607-180.72 S60.857,188.931,2.393,296.573c-3.19,5.874-3.19,12.979,0,18.853C60.858,423.069,174.892,496.147,306,496.147 S551.143,423.069,609.608,315.426z M306,451.855c-80.554,0-145.855-65.302-145.855-145.855S225.446,160.144,306,160.144 S451.856,225.446,451.856,306S386.554,451.855,306,451.855z" />{" "}
                          <path d="M306,231.67c-6.136,0-12.095,0.749-17.798,2.15c5.841,6.76,9.383,15.563,9.383,25.198c0,21.3-17.267,38.568-38.568,38.568 c-9.635,0-18.438-3.541-25.198-9.383c-1.401,5.703-2.15,11.662-2.15,17.798c0,41.052,33.279,74.33,74.33,74.33 s74.33-33.279,74.33-74.33S347.052,231.67,306,231.67z" />{" "}
                        </g>{" "}
                      </g>{" "}
                    </g>
                  </svg>
                ) : (
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
                )}
                <span>{showPassword ? "Show" : "Hide"}</span>
              </div>
            </div>
            <div className="mt-2">
              <input
                id="password"
                name="password"
                type={showPassword ? "text" : "password"}
                autoComplete="password"
                placeholder="Enter your password"
                className="block w-full text-base rounded-[10px] border-0 p-3 text-gray-100 shadow-sm ring-1 ring-inset ring-borders-gray placeholder:text-gray-100"
              />
              <p className="text-sm mt-1">
                Use 8 or more characters with a mix of letters, numbers &
                symbols
              </p>
            </div>
          </div>
          <div className="px-10">
            <div className="justify-between flex">
              <label
                htmlFor="confirmPassword"
                className="block font-normal leading-6 text-gray-100"
              >
                Confirm your password
              </label>
              <div
                className="flex gap-1 cursor-pointer items-center"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              >
                {showConfirmPassword ? (
                  <svg
                    fill="#666666"
                    height={20}
                    width={20}
                    version="1.1"
                    id="Capa_1"
                    viewBox="0 0 612 612"
                  >
                    <g id="SVGRepo_iconCarrier">
                      {" "}
                      <g>
                        {" "}
                        <g>
                          {" "}
                          <path d="M609.608,315.426c3.19-5.874,3.19-12.979,0-18.853c-58.464-107.643-172.5-180.72-303.607-180.72 S60.857,188.931,2.393,296.573c-3.19,5.874-3.19,12.979,0,18.853C60.858,423.069,174.892,496.147,306,496.147 S551.143,423.069,609.608,315.426z M306,451.855c-80.554,0-145.855-65.302-145.855-145.855S225.446,160.144,306,160.144 S451.856,225.446,451.856,306S386.554,451.855,306,451.855z" />{" "}
                          <path d="M306,231.67c-6.136,0-12.095,0.749-17.798,2.15c5.841,6.76,9.383,15.563,9.383,25.198c0,21.3-17.267,38.568-38.568,38.568 c-9.635,0-18.438-3.541-25.198-9.383c-1.401,5.703-2.15,11.662-2.15,17.798c0,41.052,33.279,74.33,74.33,74.33 s74.33-33.279,74.33-74.33S347.052,231.67,306,231.67z" />{" "}
                        </g>{" "}
                      </g>{" "}
                    </g>
                  </svg>
                ) : (
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
                )}
                <span>{showConfirmPassword ? "Show" : "Hide"}</span>
              </div>
            </div>
            <div className="mt-2">
              <input
                id="confirmPassword"
                name="confirmPassword"
                type={showConfirmPassword ? "text" : "password"}
                autoComplete="confirmPassword"
                placeholder="Confirm your password"
                className="block w-full text-base rounded-[10px] border-0 p-3 text-gray-100 shadow-sm ring-1 ring-inset ring-borders-gray placeholder:text-gray-100"
              />
              <p className="text-sm mt-1">
                Use 8 or more characters with a mix of letters, numbers &
                symbols
              </p>
            </div>
          </div>
          <div className="px-10">
            <span className="text-black">
              By creating an account, you agree to the Terms of use and Privacy
              Policy.{" "}
            </span>
            <Link to={"/"}>
              <button className="mt-2 mb-4 w-full p-3 rounded-full bg-signup-orange text-white text-xl">
                Create an account
              </button>
            </Link>
          </div>
        </div>
      </div>
    </>
  );
};

export default Signup;
