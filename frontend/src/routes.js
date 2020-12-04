import LoginPage from "./containers/Login";
// import PhoneVerification from "./containers/Login/PhoneVerification";
import RegisterPage from "./containers/Login/Register";
import ContactUs from "./containers/Contact";
// import Dashboard from "./containers/Dashboard";
import EditProfile from "./containers/profile";
import UserTables from "./containers/Users";
import TaskTables from "./containers/Tasks";
import IDTables from "./containers/IDs";

const routes = [

  // {
  //   path: "/contact",
  //   access: "common",
  //   name: "Support",
  //   show: "true",
  //   icon: "pe-7s-info",
  //   component: ContactUs
  // },
  // {
  //   path: "/dashboard",
  //   access: "common",
  //   name: "Dashboard",
  //   show: "true",
  //   icon: "pe-7s-info",
  //   component: Dashboard
  // },
  {
    path: "/login",
    access: "auth",
    name: "Login Page",
    icon: "pe-7s-info",
    component: LoginPage
  },
  {
    path: "/register",
    access: "auth",
    name: "Register Page",
    icon: "pe-7s-info",
    component: RegisterPage
  },
  {
    path: "/edit_profile",
    access: "common",
    name: "EDIT PROFILE",
    show: "false",
    icon: "pe-7s-info",
    component: EditProfile
  },
  // {
  //   path: "/users",
  //   access: "common",
  //   name: "USERS",
  //   show: "true",
  //   icon: "pe-7s-users",
  //   component: UserTables
  // },
  {
    path: "/id",
    access: "common",
    name: "ID",
    show: "true",
    icon: "pe-7s-users",
    component: IDTables
  },
  {
    path: "/entities",
    access: "common",
    name: "Entities",
    show: "true",
    icon: "pe-7s-users",
    component: TaskTables
  },
  {
    path: "/models",
    access: "common",
    name: "COAModels",
    show: "true",
    icon: "pe-7s-users",
    component: TaskTables
  },
  {
    path: "/accounts",
    access: "common",
    name: "Accounts",
    show: "true",
    icon: "pe-7s-users",
    component: TaskTables
  },
  {
    path: "/journals",
    access: "common",
    name: "Journals",
    show: "true",
    icon: "pe-7s-users",
    component: TaskTables
  },
  {
    path: "/plans",
    access: "common",
    name: "Plans",
    show: "true",
    icon: "pe-7s-users",
    component: TaskTables
  },
];
export default routes;
