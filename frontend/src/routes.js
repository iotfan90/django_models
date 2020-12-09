import LoginPage from "./containers/Login";
import RegisterPage from "./containers/Login/Register";
import EditProfile from "./containers/profile";
import IDTables from "./containers/IDs";
import EntityTables from "./containers/Entities";
import ModelTables from "./containers/Models";
import AccountTables from "./containers/Accounts";
import JournalTables from "./containers/Journals";
import PlanTables from "./containers/Plans";
import TransIDTables from "./containers/TransIDs";

const routes = [
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
    component: EntityTables
  },
  {
    path: "/models",
    access: "common",
    name: "COAModels",
    show: "true",
    icon: "pe-7s-users",
    component: ModelTables
  },
  {
    path: "/accounts",
    access: "common",
    name: "Accounts",
    show: "true",
    icon: "pe-7s-users",
    component: AccountTables
  },
  {
    path: "/journals",
    access: "common",
    name: "Journals",
    show: "true",
    icon: "pe-7s-users",
    component: JournalTables
  },
  {
    path: "/plans",
    access: "common",
    name: "Plans",
    show: "true",
    icon: "pe-7s-users",
    component: PlanTables
  },
  {
    path: "/trans-ids",
    access: "common",
    name: "Trans IDs",
    show: "true",
    icon: "pe-7s-users",
    component: TransIDTables
  },
];
export default routes;
